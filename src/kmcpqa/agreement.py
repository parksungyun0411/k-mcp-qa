"""MCP 툴 응답과 기관 API 직접 호출 결과가 같은지 본다. 키가 있어야 실측할 수 있다.

직접 호출 클라이언트(kmcpqa/direct/)는 vendor-check-agent 에서 복사했다.
비교 방식: 직접 호출 결과의 필드 값(정규화)이 MCP 응답(structuredContent 또는 text)에 들어 있는지.
MCP 서버마다 응답 형식이 달라 필드 경로를 맞추지 않고 "값이 나타나는가"로 본다. 그래서 값이 짧거나
흔한 필드(예: 코드 "01")는 우연히 일치할 수 있어, 비교 필드는 사업자번호·법인명처럼 구별되는 값으로 고른다.

    python -m kmcpqa.agreement     # servers.toml 의 [[server.agreement]] 를 실행 (키 필요)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path

import httpx

from kmcpqa.direct.dart import DartClient
from kmcpqa.direct.errors import ToolFailure
from kmcpqa.direct.nts import NtsClient
from kmcpqa.manifest import ServerSpec, load
from kmcpqa.probe import text_of
from kmcpqa.sandbox import Workspace
from kmcpqa.wire import WireSession

NTS_BASE = "https://api.odcloud.kr/api/nts-businessman/v1"
DART_BASE = "https://opendart.fss.or.kr/api"


@dataclass(frozen=True)
class Case:
    tool: str
    args: dict
    direct: str  # nts_status | dart_company
    direct_args: dict
    fields: list[str]


def scrub(text: str, keys: dict) -> str:
    """서버가 오류 문구에 요청 URL 을 그대로 넣는 경우가 있어, 기록 전에 키 값을 지운다."""
    for v in keys.values():
        if v:
            text = text.replace(v, "<KEY>")
    return text


def norm(value: object) -> str:
    return "".join(str(value).split()).replace("-", "")


async def direct_record(case: Case, http: httpx.AsyncClient, keys: dict, bases: dict) -> dict:
    if case.direct == "nts_status":
        client = NtsClient(bases.get("nts", NTS_BASE), keys["DATA_GO_KR_SERVICE_KEY"], http)
        bno = case.direct_args["b_no"]
        return (await client.status([bno]))[bno]
    if case.direct == "dart_company":
        client = DartClient(bases.get("dart", DART_BASE), keys["OPENDART_API_KEY"], http)
        return await client.company(case.direct_args["corp_code"]) or {}
    raise ValueError(f"unknown direct call {case.direct}")


def compare(case: Case, record: dict, result: dict | None) -> dict:
    blob = norm(json.dumps(result.get("structuredContent"), ensure_ascii=False)) \
        if isinstance(result, dict) and result.get("structuredContent") is not None else ""
    blob += norm(text_of(result))
    fields = {}
    for f in case.fields:
        v = record.get(f)
        fields[f] = {"direct": v, "found_in_mcp": v is not None and norm(v) in blob}
    agree = all(x["found_in_mcp"] for x in fields.values())
    return {"agree": agree, "fields": fields}


async def run_case(session: WireSession, case: Case, http: httpx.AsyncClient, keys: dict,
                   bases: dict | None = None, timeout_s: float = 30) -> dict:
    out: dict = {"tool": case.tool, "args": case.args, "direct": case.direct}
    try:
        record = await direct_record(case, http, keys, bases or {})
    except ToolFailure as e:
        return out | {"status": "direct_failed", "error": e.error.to_dict()}
    reply = await session.request("tools/call", {"name": case.tool, "arguments": case.args}, timeout_s)
    if reply.kind != "result" or (reply.result or {}).get("isError"):
        error = (reply.error or {}).get("message") if reply.kind == "error" else None
        return out | {"status": "mcp_failed", "reply": reply.kind,
                      "text": scrub(text_of(reply.result)[:300], keys) if reply.result else None,
                      "error": scrub(error.splitlines()[0][:300], keys) if error else None}
    return out | {"status": "compared"} | compare(case, record, reply.result)


def server_env(spec: ServerSpec, ws: Workspace, keys: dict, key_map: dict) -> dict:
    env = ws.env(spec, "none")
    for server_var, our_var in key_map.items():
        env[server_var] = keys[our_var]
    return env


async def _main(args: argparse.Namespace) -> None:
    keys = {k: os.environ.get(k, "") for k in ("DATA_GO_KR_SERVICE_KEY", "OPENDART_API_KEY")}
    servers, _ = load(Path(args.manifest))
    targets = [s for s in servers if s.agreement]
    if not any(keys.values()):
        raise SystemExit("DATA_GO_KR_SERVICE_KEY / OPENDART_API_KEY 가 없어 측정하지 않습니다 (측정 전).")
    ws = Workspace(Path(args.workdir))
    out_dir = Path(args.reports) / "agreement"
    out_dir.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient() as http:
        for spec in targets:
            needed = {v for c in spec.agreement for v in c["key_map"].values()}
            if not all(keys.get(k) for k in needed):
                print(f"[{spec.id}] skip: missing {sorted(needed)}")
                continue
            session = WireSession(ws.wrap(spec, spec.command), ws.cwd(spec),
                                  server_env(spec, ws, keys, spec.agreement[0]["key_map"]))
            await session.start()
            await session.initialize()
            results = []
            for c in spec.agreement:
                case = Case(c["tool"], c["args"], c["direct"], c["direct_args"], c["fields"])
                results.append(await run_case(session, case, http, keys))
            await session.close()
            (out_dir / f"{spec.id}.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))
            print(f"[{spec.id}] {sum(r.get('agree') is True for r in results)}/{len(results)} agree")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", default="servers.toml")
    p.add_argument("--reports", default="reports")
    p.add_argument("--workdir", default="/tmp/kmcp-work")
    asyncio.run(_main(p.parse_args()))


if __name__ == "__main__":
    main()
