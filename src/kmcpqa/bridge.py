"""stdio 서버를 Streamable HTTP 로 노출하는 최소 중계기. 공식 conformance 도구가 URL 만 받기 때문에 쓴다.

메시지를 다시 직렬화하지 않고 서버가 stdout 에 쓴 줄을 그대로 HTTP 응답 본문으로 돌려준다.
따라서 conformance 의 wire-schema 검사는 서버가 실제로 보낸 메시지를 본다.
지원 범위: POST 단일 요청(JSON 응답), 알림(202). GET(SSE)·세션 헤더·배치는 지원하지 않는다.

중계기가 스스로 만든 응답은 모두 self.events 에 남긴다. 서버 프로세스가 없어서 생긴 실패와
서버가 실제로 응답한 내용을 보고서에서 구분하기 위해서다.
  server_not_running   요청 전에 이미 프로세스가 종료됨
  server_exited        요청을 기다리는 중 프로세스가 종료됨
  no_response          프로세스는 살아 있으나 제한 시간 안에 응답 없음
"""


from __future__ import annotations

import asyncio
import json

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from kmcpqa.wire import WireSession

BRIDGE_CODE = -32099  # JSON-RPC 서버 오류 예약 범위. 서버가 아니라 중계기가 만든 응답임을 표시


class StdioBridge:
    def __init__(self, session: WireSession, timeout_s: float = 30.0):
        self.session = session
        self.timeout_s = timeout_s
        self.lock = asyncio.Lock()
        self.events: list[dict] = []

    def _bridge_error(self, mid, kind: str) -> str:
        rc = self.session.returncode
        self.events.append({"id": mid, "kind": kind, "returncode": rc})
        message = {"server_not_running": f"k-mcp-qa bridge: server process not running (exit {rc})",
                   "server_exited": f"k-mcp-qa bridge: server process exited during request (exit {rc})",
                   "no_response": f"k-mcp-qa bridge: no response within {self.timeout_s}s "
                                  "(server process running)"}[kind]
        return json.dumps({"jsonrpc": "2.0", "id": mid,
                           "error": {"code": BRIDGE_CODE, "message": message, "data": {"bridge": kind}}})

    async def forward(self, msg: dict) -> str | None:
        """요청이면 같은 id 의 응답 줄(원문)을, 알림이면 None 을 돌려준다."""
        line = json.dumps(msg, ensure_ascii=False)
        if "id" not in msg or "method" not in msg:
            await self.session.send_raw(line)
            return None
        mid = msg["id"]
        if not self.session.alive():
            return self._bridge_error(mid, "server_not_running")
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
                return self._bridge_error(mid, "server_exited")
            await asyncio.sleep(0.01)
        return self._bridge_error(mid, "no_response")

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
