"""관찰 유형 분류. 결과 JSON 한 개에서 재현 가능한 관찰만 뽑는다.

각 관찰은 코드, 툴, 근거(응답 일부), 재현 입력, 출처를 가진다.
- 출처(origin): server(서버 코드) | sdk(SDK 기본 동작, 소스 위치 확인) | unknown(위치 미확인)
  P3·P4·P6·I3·E2 는 응답 문구·stderr 스택을 서버 소스와 SDK 소스에서 찾아 가린다(attribution.py).
  툴 응답 내용에서 나온 유형(E1·E3·R·S·H1)은 툴 핸들러가 만든 것이라 server 로 두고, 문구 위치를 찾으면 붙인다.
- 원인(cause): 같은 코드·같은 출처·같은 문구(입력 값·숫자 제거)를 하나의 원인으로 묶는다.
판단이 들어가는 말은 쓰지 않고 "무엇을 보냈고 무엇이 돌아왔는가"만 남긴다.
"""

from __future__ import annotations

import re
from pathlib import Path

from kmcpqa import attribution

# 스펙 문장은 원문 그대로 옮긴다. 이 절은 서술적 설명이며 MUST/SHOULD 같은 규범 키워드가 없다.
SPEC_TOOLS_ERRORS_URL = "https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling"
SPEC_TOOLS_ERRORS_QUOTE = (
    "Tools use two error reporting mechanisms:\n"
    "1. **Protocol Errors**: Standard JSON-RPC errors for issues like:\n"
    "   - Unknown tools\n"
    "   - Malformed requests (requests that fail to satisfy CallToolRequest schema)\n"
    "   - Server errors\n"
    "2. **Tool Execution Errors**: Reported in tool results with `isError: true`:\n"
    "   - API failures\n"
    "   - Input validation errors (e.g., date in wrong format, value out of range)\n"
    "   - Business logic errors"
)
JSONRPC_URL = "https://www.jsonrpc.org/specification#error_object"
JSONRPC_QUOTE = "-32601 | Method not found | The method does not exist / is not available."

BASIS = {
    "tools_errors": (SPEC_TOOLS_ERRORS_URL, "서술적 설명(규범 키워드 없음)"),
    "jsonrpc": (JSONRPC_URL, "JSON-RPC 2.0 오류 코드 표"),
}

# code: (분류, 설명, 근거 키 또는 None)
TAXONOMY: dict[str, tuple[str, str, str | None]] = {
    "I1": ("설치·기동", "고정한 커밋에서 문서의 설치 절차가 실패함", None),
    "I2": ("설치·기동", "자리 표시자 키를 넣어도 initialize 응답이 오지 않음", None),
    "I3": ("설치·기동", "자리 표시자 키로 시작한 뒤 요청 없이 5초 안에 프로세스가 종료됨", None),
    "P1": ("프로토콜", "stdout 에 JSON-RPC 가 아닌 줄을 씀", None),
    "P2": ("프로토콜", "응답이 MCP 2025-11-25 JSON 스키마를 어김", None),
    "P3": ("프로토콜", "알 수 없는 메서드에 -32601 이 아닌 응답(또는 무응답)", "jsonrpc"),
    "P4": ("프로토콜", "알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답", "tools_errors"),
    "P5": ("프로토콜", "tools/call 이 제한 시간 안에 응답하지 않음", None),
    "P6": ("프로토콜", "요청 하나를 받은 뒤 서버가 종료되거나 ping 에 응답하지 않음", None),
    "S1": ("스키마", "inputSchema/outputSchema 가 메타스키마 검증을 통과하지 못함", None),
    "S2": ("스키마", "required 에 properties 에 없는 이름이 있음", None),
    "S3": ("스키마", "outputSchema 를 선언했지만 structuredContent 가 없거나 스키마와 다름", None),
    "S4": ("스키마", "inputSchema 의 properties 가 비어 있는데 런타임은 특정 인자를 요구함", None),
    "R1": ("스키마-런타임 불일치", "선언된 필수 인자를 빼고 호출해도 오류 없이 결과를 돌려줌", None),
    "R2": ("스키마-런타임 불일치", "선언과 다른 타입의 인자로 호출해도 오류 없이 결과를 돌려줌", None),
    "R3": ("스키마-런타임 불일치", "스키마를 만족하는 입력을 스키마에 없는 인자 조건으로 거부함", None),
    "E1": ("오류 처리", "실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출)",
           "tools_errors"),
    "E2": ("오류 처리", "기관 API 실패를 JSON-RPC 내부 오류(-32603)로 응답", "tools_errors"),
    "E3": ("오류 처리", "입력 검증·파싱 오류를 isError 없는 결과로 응답", "tools_errors"),
    "H1": ("오류 처리", "응답 본문에 Python traceback 과 서버 파일 경로가 담김", None),
}

_ARG_COMPLAINT = re.compile(
    r"(필수|입력해|입력하|required|missing|must (be|provide|specify)|is not valid|형식|올바르지|"
    r"하나를|one of)", re.IGNORECASE)
_INPUT_ERROR = re.compile(r"(파싱 오류|parse error|JSONDecodeError|Expecting value|validation error|Field required)",
                          re.IGNORECASE)
_SERVER_ORIGIN = {"I1", "P1", "P2", "P5", "S1", "S2", "S3", "S4", "R1", "R2", "R3", "E1", "E3", "H1"}


def _obs(code: str, tool: str | None, evidence: str, args: object = None, **extra) -> dict:
    cat, desc, _ = TAXONOMY[code]
    return {"code": code, "category": cat, "description": desc, "tool": tool,
            "evidence": evidence[:400], "args": args} | extra


def _exc_lines(lines: list[str] | None, n: int = 2) -> str:
    """stderr 에서 예외 이름이 들어간 마지막 줄들(근거로 인용)."""
    hits = [ln.strip() for ln in lines or [] if re.search(r"(Error|Exception|Traceback)", ln)]
    return " | ".join(hits[-n:]) if hits else " | ".join((lines or [])[-n:])


def cause_key(f: dict) -> str:
    """같은 원인으로 묶을 키: 코드 + 출처 + 문구(입력 값·숫자·프로브 이름 제거)."""
    text = re.sub(r"^(missing_required|wrong_type|valid): ", "", f["evidence"])
    for v in attribution.dynamic_values(f.get("args"), [f.get("tool") or ""]):
        if len(v) >= 3:
            text = text.replace(v, "<v>")
    text = re.sub(r"\d+", "<n>", text)[:160]
    return f"{f['code']}|{f.get('origin')}|{text}"


def attribute(f: dict, server_root: Path | None, stderr: list[str] | None = None,
              message: str | None = None) -> dict:
    if server_root is None:
        return f | {"origin": "unknown", "where": []}
    code = f["code"]
    if code in ("P6", "I3") or (code == "P3" and not message):
        a = attribution.from_stderr(stderr or [], server_root)
    elif code == "I2":
        a = attribution.from_stderr(stderr or [], server_root)
        dep = attribution.find(server_root, r"\bmcp(\[cli\])?\s*>=", "server", suffixes={".toml", ".txt"})
        a = {"origin": "server", "where": dep + a["where"], "note": "의존성 선언과 설치된 SDK 의 조합"}
    else:
        dyn = attribution.dynamic_values(f.get("args"), ["kmcpqa_no_such_tool"])
        a = attribution.from_text(message if message is not None else f["evidence"], dyn, server_root)
        if code in _SERVER_ORIGIN:
            a = a | {"origin": "server"}
        if code == "S4" and f.get("tool"):
            decl = attribution.find(server_root, rf"""name:\s*["']{re.escape(f['tool'])}["']""")
            a = a | {"origin": "server", "where": decl + a.get("where", []),
                     "note": "tools/list 의 inputSchema 는 properties 가 비어 있고, 검증은 서버가 등록한 스키마로 "
                             "SDK 가 수행함. 스키마를 JSON Schema 로 바꾸는 과정에서 생겼을 수 있음(확인하지 않음)"}
        if code == "E2":
            handler = attribution.find(server_root, r"setRequestHandler\(\s*CallToolRequestSchema")
            mapping = attribution.find(server_root, r"ErrorCode\.InternalError", "sdk", limit=1)
            if handler and mapping:
                a = a | {"origin": "server", "where": a["where"] + handler + mapping,
                         "note": "서버의 low-level CallTool 핸들러가 던진 예외를 SDK 프로토콜 계층이 "
                                 "-32603 으로 바꿈"}
    return f | {"origin": a["origin"], "where": a.get("where", []), "note": a.get("note")}


def findings(record: dict, server_root: Path | None = None) -> list[dict]:
    out: list[dict] = []

    def add(code, tool, evidence, args=None, stderr=None, message=None):
        out.append(attribute(_obs(code, tool, evidence, args), server_root, stderr, message))

    inst = record.get("install") or {}
    if inst and not inst.get("ok"):
        failed = next((s for s in inst.get("steps", []) if s.get("returncode") != 0), {})
        add("I1", None, f"step {failed.get('argv')} exit {failed.get('returncode')}")
        return out
    probe = record.get("probe") or {}
    init = probe.get("initialize") or {}
    if init and init.get("outcome") != "result":
        tail = init.get("stderr_tail") or []
        add("I2", None, f"initialize {init.get('outcome')}, stderr 마지막 줄: {' | '.join(tail[-2:])}",
            stderr=tail)
        return out
    if not probe:
        return out

    idle_exit = probe.get("idle_alive") is False
    if idle_exit:
        ie = probe.get("idle_exit") or {}
        tail = ie.get("stderr_tail") or []
        add("I3", None, f"exit {ie.get('returncode')}: {_exc_lines(tail)}", stderr=tail)
    noise = probe.get("stdout_noise") or {}
    if noise.get("count"):
        add("P1", None, f"{noise['count']} lines, e.g. {noise.get('sample', [''])[0]!r}")
    for where in ("initialize", "tools_list", "ping"):
        v = (probe.get(where) or {}).get("spec_violations") or []
        if v:
            add("P2", None, f"{where}: {v[0]}")

    um = probe.get("unknown_method") or {}
    um_dead = um.get("responsive_after", um.get("alive_after")) is False and not idle_exit
    if um and not (um.get("outcome") == "error" and um.get("error_code") == -32601):
        msg = um.get("error_message") if um.get("outcome") == "error" else None
        add("P3", None, f"method=kmcpqa/unknown_method → {um.get('outcome')} code={um.get('error_code')} "
                        f"{um.get('error_message') or ''}".strip(), {}, um.get("stderr_delta"), msg)
    if um_dead:
        add("P6", None, "method=kmcpqa/unknown_method → 이후 응답 없음/종료. stderr: "
            + _exc_lines(um.get("stderr_delta")), {}, um.get("stderr_delta"))

    ut = probe.get("unknown_tool") or {}
    if ut.get("outcome") in ("tool_error", "ok"):
        add("P4", "kmcpqa_no_such_tool", f"{ut['outcome']}: {ut.get('text_excerpt', '')}", {},
            message=ut.get("text_excerpt", ""))
    if ut.get("responsive_after", ut.get("alive_after")) is False and not idle_exit:
        add("P6", "kmcpqa_no_such_tool", "이후 응답 없음/종료. stderr: "
            + _exc_lines(ut.get("stderr_delta")), {}, ut.get("stderr_delta"))

    for t in probe.get("tools") or []:
        name = t["name"]
        traced = False
        for p in t.get("input_schema_problems") or []:
            add("S2" if p.startswith("required not in") else "S1", name, f"inputSchema {p}")
        for p in t.get("output_schema_problems") or []:
            add("S2" if p.startswith("required not in") else "S1", name, f"outputSchema {p}")
        for label, c in (t.get("probes") or {}).items():
            outcome = c.get("outcome")
            args = c.get("args")
            text = c.get("text_excerpt", "") or c.get("error_message", "") or ""
            if outcome == "timeout":
                add("P5", name, f"{label}: no response in {c.get('elapsed_ms')} ms", args)
            if c.get("responsive_after", c.get("alive_after")) is False and not idle_exit:
                add("P6", name, f"{label} → 이후 응답 없음/종료. stderr: "
                    + _exc_lines(c.get("stderr_delta")), args, c.get("stderr_delta"))
            if outcome == "ok" and c.get("spec_violations"):
                add("P2", name, f"CallToolResult: {c['spec_violations'][0]}", args)
            if c.get("output_mismatch"):
                add("S3", name, f"{c['output_mismatch'][0]}", args)
            if outcome == "error" and c.get("error_code") == -32603:
                add("E2", name, f"{label}: {c.get('error_message')}", args, message=c.get("error_message"))
            if c.get("traceback") and not traced:
                traced = True
                add("H1", name, f"{label}: {text}", args, message=text)
            if label in ("missing_required", "wrong_type") and outcome == "ok":
                if c.get("error_marker"):
                    add("E3", name, f"{label}: {text}", args, message=text)
                else:
                    add("R1" if label == "missing_required" else "R2", name,
                        f"required={t.get('required')} → {text}", args, message=text)
            if label == "valid":
                if outcome == "ok" and (c.get("auth_marker") or c.get("error_marker")):
                    if not c.get("auth_marker") and _INPUT_ERROR.search(text):
                        add("E3", name, f"valid(합성 입력): {text}", args, message=text)
                    else:
                        add("E1", name, f"marker={c.get('auth_marker') or c.get('error_marker')!r}: {text}",
                            args, message=text)
                elif outcome == "tool_error" and not c.get("auth_marker") and _ARG_COMPLAINT.search(text):
                    if t.get("properties") == [] and "properties" in t:
                        add("S4", name, f"properties=[] → {text}", args, message=text)
                    else:
                        add("R3", name, text, args, message=text)
    return out


def group_causes(fs: list[dict]) -> list[dict]:
    """원인별로 묶는다: [{"code", "origin", "where", "count", "example"}]"""
    groups: dict[str, dict] = {}
    for f in fs:
        k = cause_key(f)
        g = groups.setdefault(k, {"code": f["code"], "origin": f.get("origin"), "where": f.get("where"),
                                  "note": f.get("note"), "count": 0, "example": f, "tools": set()})
        g["count"] += 1
        if f.get("tool"):
            g["tools"].add(f["tool"])
    return list(groups.values())
