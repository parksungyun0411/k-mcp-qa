"""서버 하나에 공통 시험을 돌린다. 키가 필요 없는 항목만 다룬다.

1. 키 없이 시작: initialize 응답이 오는지, 아니면 종료하는지
2. 자리 표시자 키로 시작: initialize·tools/list·ping 응답과 스펙 스키마 적합성
3. 알 수 없는 메서드, 알 수 없는 툴 이름
4. 툴마다: 스키마 자체 검사, 필수 인자 누락 호출, 잘못된 타입 호출, 스키마를 만족하는 호출(자리 표시자 키)
   응답 분류 → jsonrpc_error | tool_error | ok | timeout | closed, 호출 뒤 프로세스 생존 여부
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from pathlib import Path

from kmcpqa.specschema import check_json_schema, instance_errors, schema_dialect, spec_errors
from kmcpqa.synth import has_required, valid_args, wrong_type_args
from kmcpqa.wire import WireSession

# 성공 응답 본문에 이런 문구가 있으면 "인증 실패를 정상 결과로 돌려줌" 후보로 본다.
AUTH_MARKERS = [
    r"SERVICE_KEY_IS_NOT_REGISTERED", r"SERVICE_KEY", r"returnReasonCode", r"인증키", r"인증 키",
    r"API ?키", r"api[_ ]?key", r"등록되지 않은", r"Unauthorized", r"Forbidden", r"\b401\b", r"\b403\b",
    r"invalid (api )?key", r'"status"\s*:\s*"0(10|11|12|20|901)"', r"KMCPQA_PLACEHOLDER",
]
_AUTH_RE = re.compile("|".join(AUTH_MARKERS), re.IGNORECASE)
# 본문이 오류 보고처럼 보이는지. isError 없이 돌아온 결과에서만 쓴다.
_ERRORISH_RE = re.compile(
    r"Traceback \(most recent call last\)|\berror\b|오류|에러|실패|invalid|validation error|"
    r"Field required|HTTP error|exception|\"success\"\s*:\s*false", re.IGNORECASE)


@dataclass
class ProbeConfig:
    start_timeout_s: float = 30.0
    call_timeout_s: float = 20.0
    pause_s: float = 0.2
    max_tools: int | None = None
    idle_s: float = 5.0
    health_timeout_s: float = 5.0


def text_of(result: dict | None) -> str:
    if not isinstance(result, dict):
        return ""
    parts = [c.get("text", "") for c in result.get("content") or [] if isinstance(c, dict)]
    return "\n".join(p for p in parts if isinstance(p, str))


def classify_call(reply) -> dict:
    out: dict = {"outcome": reply.kind, "elapsed_ms": reply.elapsed_ms}
    if reply.kind == "error":
        out["error_code"] = (reply.error or {}).get("code")
        out["error_message"] = str((reply.error or {}).get("message", ""))[:300]
        m = _AUTH_RE.search(out["error_message"])
        out["auth_marker"] = m.group(0) if m else None
    elif reply.kind == "result":
        result = reply.result
        out["outcome"] = "tool_error" if isinstance(result, dict) and result.get("isError") else "ok"
        text = text_of(result)
        out["text_excerpt"] = text[:300]
        m = _AUTH_RE.search(text)
        out["auth_marker"] = m.group(0) if m else None
        e = _ERRORISH_RE.search(text)
        out["error_marker"] = e.group(0) if e else None
        out["traceback"] = "Traceback (most recent call last)" in text
        out["spec_violations"] = spec_errors("CallToolResult", result)
        out["has_structured"] = isinstance(result, dict) and "structuredContent" in result
    return out


async def _session(argv, cwd, env) -> WireSession:
    s = WireSession(argv, cwd, env)
    await s.start()
    return s


async def start_check(argv, cwd, env, cfg: ProbeConfig, dump_dir: Path) -> dict:
    """키 없는 환경에서 initialize 까지만 해 본다."""
    s = await _session(argv, cwd, env)
    reply = await s.initialize(cfg.start_timeout_s)
    await asyncio.sleep(0.5)
    out = {"initialize": reply.kind, "alive": s.alive(), "returncode": s.returncode,
           "elapsed_ms": reply.elapsed_ms}
    await s.close()
    out["returncode"] = s.returncode if out["returncode"] is None and not out["alive"] else out["returncode"]
    out["stderr_tail"] = s.stderr[-5:]
    s.dump(dump_dir)
    return out


async def full_probe(argv, cwd, env, cfg: ProbeConfig, dump_dir: Path) -> dict:
    res: dict = {"restarts": 0}
    s = await _session(argv, cwd, env)
    init = await s.initialize(cfg.start_timeout_s)
    res["initialize"] = {"outcome": init.kind, "elapsed_ms": init.elapsed_ms}
    if init.kind != "result":
        res["initialize"]["stderr_tail"] = s.stderr[-8:]
        await s.close()
        res["initialize"]["returncode"] = s.returncode
        s.dump(dump_dir)
        return res
    # 요청 없이 잠시 두었을 때 살아 있는지. 시작 직후 백그라운드 작업이 실패해 종료하는 서버를 구분한다.
    await asyncio.sleep(cfg.idle_s)
    res["idle_alive"] = s.alive()
    if not s.alive():
        res["idle_exit"] = {"returncode": s.returncode, "stderr_tail": s.stderr[-40:]}
    ir = init.result or {}
    res["initialize"].update({
        "protocolVersion": ir.get("protocolVersion"), "serverInfo": ir.get("serverInfo"),
        "capabilities": ir.get("capabilities"), "spec_violations": spec_errors("InitializeResult", ir),
    })

    if not s.alive():
        await s.close()
        s.dump(dump_dir / "session_idle")
        res["restarts"] += 1
        s = await _session(argv, cwd, env)
        await s.initialize(cfg.start_timeout_s)
    tools, pages, cursor, list_errors = [], 0, None, []
    while True:
        lr = await s.request("tools/list", {"cursor": cursor} if cursor else {}, cfg.call_timeout_s)
        pages += 1
        if lr.kind != "result":
            list_errors.append(lr.kind)
            break
        list_errors += spec_errors("ListToolsResult", lr.result)
        tools += (lr.result or {}).get("tools") or []
        cursor = (lr.result or {}).get("nextCursor")
        if not cursor or pages > 50:
            break
    res["tools_list"] = {"count": len(tools), "pages": pages, "spec_violations": list_errors[:10],
                         "elapsed_ms": lr.elapsed_ms}

    ping = await s.request("ping", None, cfg.call_timeout_s)
    res["ping"] = {"outcome": ping.kind, "spec_violations":
                   spec_errors("JSONRPCResultResponse", ping.message) if ping.message else []}

    noise: list[str] = []

    async def restart(sess: WireSession) -> WireSession:
        await sess.close()
        noise.extend(sess.stdout_noise)
        sess.dump(dump_dir / f"session{res['restarts']}")
        res["restarts"] += 1
        sess = await _session(argv, cwd, env)
        await sess.initialize(cfg.start_timeout_s)
        return sess

    async def checked(sess: WireSession, method: str, params: dict | None):
        """요청 하나를 보내고, 그 뒤 서버가 살아서 응답하는지 확인한다.
        응답 불능이면 새 프로세스로 바꿔 다음 요청이 앞 요청의 영향을 받지 않게 한다."""
        if not sess.alive():
            sess = await restart(sess)
        before = len(sess.stderr)
        reply = await sess.request(method, params, cfg.call_timeout_s)
        await asyncio.sleep(cfg.pause_s)
        health: dict = {"alive_after": sess.alive()}
        if sess.alive() and reply.kind == "timeout":
            pong = await sess.request("ping", None, cfg.health_timeout_s)
            health["responsive_after"] = pong.kind == "result"
        else:
            health["responsive_after"] = sess.alive()
        health["stderr_delta"] = sess.stderr[before:][-150:]
        if not health["responsive_after"]:
            sess = await restart(sess)
            health["restarted"] = True
        return sess, reply, health

    s, um, h = await checked(s, "kmcpqa/unknown_method", {})
    res["unknown_method"] = {"outcome": um.kind, "error_code": (um.error or {}).get("code"),
                             "error_message": str((um.error or {}).get("message", ""))[:300]} | h

    s, ut, h = await checked(s, "tools/call", {"name": "kmcpqa_no_such_tool", "arguments": {}})
    res["unknown_tool"] = classify_call(ut) | h

    per_tool = []
    for tool in tools[: cfg.max_tools] if cfg.max_tools else tools:
        name = tool.get("name")
        schema = tool.get("inputSchema") or {}
        entry: dict = {
            "name": name,
            "input_dialect": schema_dialect(schema) if isinstance(schema, dict) else None,
            "input_schema_problems": check_json_schema(schema),
            "required": list(schema.get("required") or []) if isinstance(schema, dict) else [],
            "properties": sorted((schema.get("properties") or {}).keys()) if isinstance(schema, dict) else [],
            "output_schema": "outputSchema" in tool,
            "annotations": tool.get("annotations"),
            "probes": {},
        }
        if "outputSchema" in tool:
            entry["output_schema_problems"] = check_json_schema(tool["outputSchema"])
        probes = []
        if isinstance(schema, dict) and has_required(schema):
            probes.append(("missing_required", {}))
        if isinstance(schema, dict) and (wrong := wrong_type_args(schema)):
            probes.append(("wrong_type", wrong))
        if isinstance(schema, dict):
            va = valid_args(schema)
            if va is None:
                entry["probes"]["valid"] = {"outcome": "unsynthesizable"}
            else:
                probes.append(("valid", va))
        for label, args in probes:
            s, reply, h = await checked(s, "tools/call", {"name": name, "arguments": args})
            c = classify_call(reply) | h
            c["args"] = args
            if (label == "valid" and c["outcome"] == "ok" and "outputSchema" in tool
                    and isinstance(reply.result, dict)):
                sc = reply.result.get("structuredContent")
                c["output_mismatch"] = (["structuredContent missing"] if sc is None
                                        else instance_errors(tool["outputSchema"], sc))
            entry["probes"][label] = c
        per_tool.append(entry)
    res["tools"] = per_tool
    noise += s.stdout_noise
    res["stdout_noise"] = {"count": len(noise), "sample": noise[:5]}
    res["server_initiated_messages"] = len(s.server_messages)
    await s.close()
    s.dump(dump_dir)
    return res
