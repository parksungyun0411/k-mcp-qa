"""관찰 하나를 재현한다: 같은 격리 환경에서 서버를 띄우고 요청 하나를 보내 원문 응답을 출력한다.

    python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_company", "arguments": {}}'
    python -m kmcpqa.repro dart-mcp-server kmcpqa/unknown_method '{}'
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from kmcpqa.manifest import load
from kmcpqa.sandbox import Workspace
from kmcpqa.wire import WireSession


async def repro(server_id: str, method: str, params: dict, manifest: Path, workdir: Path,
                timeout_s: float) -> dict:
    servers, _ = load(manifest)
    spec = next(s for s in servers if s.id == server_id)
    ws = Workspace(workdir)
    session = WireSession(ws.wrap(spec, spec.command), ws.cwd(spec), ws.env(spec, "placeholder"))
    await session.start()
    init = await session.initialize()
    reply = await session.request(method, params, timeout_s)
    await asyncio.sleep(0.3)
    alive = session.alive()
    await session.close()
    return {"initialize": init.kind, "reply_kind": reply.kind, "reply": reply.message,
            "alive_after": alive, "stdout_noise": session.stdout_noise, "stderr_tail": session.stderr[-10:]}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("server_id")
    p.add_argument("method")
    p.add_argument("params", help="JSON")
    p.add_argument("--manifest", default="servers.toml")
    p.add_argument("--workdir", default="/tmp/kmcp-work")
    p.add_argument("--timeout", type=float, default=20)
    a = p.parse_args()
    out = asyncio.run(repro(a.server_id, a.method, json.loads(a.params), Path(a.manifest), Path(a.workdir),
                            a.timeout))
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
