"""stdio 서버를 Streamable HTTP 로 노출하는 최소 중계기. 공식 conformance 도구가 URL 만 받기 때문에 쓴다.

메시지를 다시 직렬화하지 않고 서버가 stdout 에 쓴 줄을 그대로 HTTP 응답 본문으로 돌려준다.
따라서 conformance 의 wire-schema 검사는 서버가 실제로 보낸 메시지를 본다.
지원 범위: POST 단일 요청(JSON 응답), 알림(202). GET(SSE)·세션 헤더·배치는 지원하지 않는다.
"""

from __future__ import annotations

import asyncio
import json

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from kmcpqa.wire import WireSession


class StdioBridge:
    def __init__(self, session: WireSession, timeout_s: float = 30.0):
        self.session = session
        self.timeout_s = timeout_s
        self.lock = asyncio.Lock()

    async def forward(self, msg: dict) -> str | None:
        """요청이면 같은 id 의 응답 줄(원문)을, 알림이면 None 을 돌려준다."""
        line = json.dumps(msg, ensure_ascii=False)
        if "id" not in msg or "method" not in msg:
            await self.session.send_raw(line)
            return None
        mid = msg["id"]
        start = len(self.session.transcript)
        await self.session.send_raw(line)
        deadline = asyncio.get_running_loop().time() + self.timeout_s
        while asyncio.get_running_loop().time() < deadline:
            for row in self.session.transcript[start:]:
                if row["dir"] != "recv":
                    continue
                try:
                    got = json.loads(row["line"])
                except ValueError:
                    continue
                if isinstance(got, dict) and got.get("id") == mid and ("result" in got or "error" in got):
                    return row["line"]
            if not self.session.alive():
                break
            await asyncio.sleep(0.01)
        return json.dumps({"jsonrpc": "2.0", "id": mid,
                           "error": {"code": -32000, "message": "k-mcp-qa bridge: no response from server"}})

    async def handle(self, request: Request) -> Response:
        if request.method != "POST":
            return Response(status_code=405)
        try:
            msg = await request.json()
        except ValueError:
            return JSONResponse({"jsonrpc": "2.0", "id": None,
                                 "error": {"code": -32700, "message": "Parse error"}}, status_code=400)
        if not isinstance(msg, dict):
            return JSONResponse({"jsonrpc": "2.0", "id": None,
                                 "error": {"code": -32600, "message": "batch not supported by bridge"}},
                                status_code=400)
        async with self.lock:
            raw = await self.forward(msg)
        if raw is None:
            return Response(status_code=202)
        return Response(raw, media_type="application/json")

    def app(self) -> Starlette:
        return Starlette(routes=[Route("/mcp", self.handle, methods=["GET", "POST", "DELETE"])])
