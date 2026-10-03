"""stdio JSON-RPC 클라이언트. SDK 를 거치지 않고 줄 단위로 직접 읽고 쓴다.

SDK 클라이언트는 잘못된 메시지를 걸러 내거나 예외로 바꾸기 때문에, 서버가 실제로 무엇을
stdout 에 썼는지 남기려고 직접 구현했다. 모든 송수신 줄은 transcript 에 시각과 함께 남는다.
"""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = "2025-11-25"
CLIENT_INFO = {"name": "k-mcp-qa", "version": "0.1.0"}


@dataclass
class Reply:
    """요청 하나의 결과. kind: result | error | timeout | closed"""

    kind: str
    message: dict | None = None
    elapsed_ms: float = 0.0

    @property
    def result(self) -> Any:
        return (self.message or {}).get("result")

    @property
    def error(self) -> dict | None:
        return (self.message or {}).get("error")


@dataclass
class WireSession:
    argv: list[str]
    cwd: Path | None = None
    env: dict[str, str] | None = None
    transcript: list[dict] = field(default_factory=list)
    stdout_noise: list[str] = field(default_factory=list)
    stderr: list[str] = field(default_factory=list)
    server_messages: list[dict] = field(default_factory=list)  # 요청에 대한 응답이 아닌 메시지

    def __post_init__(self) -> None:
        self._proc: asyncio.subprocess.Process | None = None
        self._pending: dict[int, asyncio.Future] = {}
        self._next_id = 1
        self._tasks: list[asyncio.Task] = []
        self._t0 = time.perf_counter()

    def _log(self, direction: str, line: str) -> None:
        self.transcript.append({"t": round(time.perf_counter() - self._t0, 4), "dir": direction,
                                "line": line})

    async def start(self) -> None:
        self._proc = await asyncio.create_subprocess_exec(
            *self.argv, cwd=self.cwd, env=self.env, stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, limit=2**24,
        )
        self._tasks = [asyncio.create_task(self._read_stdout()),
                       asyncio.create_task(self._read_stderr())]

    @property
    def returncode(self) -> int | None:
        return self._proc.returncode if self._proc else None

    def alive(self) -> bool:
        return self._proc is not None and self._proc.returncode is None

    async def _read_stdout(self) -> None:
        assert self._proc and self._proc.stdout
        while True:
            raw = await self._proc.stdout.readline()
            if not raw:
                break
            line = raw.decode("utf-8", errors="replace").rstrip("\n")
            self._log("recv", line)
            try:
                msg = json.loads(line)
            except ValueError:
                self.stdout_noise.append(line)
                continue
            if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
                self.stdout_noise.append(line)
                continue
            mid = msg.get("id")
            if ("result" in msg or "error" in msg) and mid in self._pending:
                fut = self._pending.pop(mid)
                if not fut.done():
                    fut.set_result(msg)
            else:
                self.server_messages.append(msg)
        for fut in self._pending.values():
            if not fut.done():
                fut.set_result(None)

    async def _read_stderr(self) -> None:
        assert self._proc and self._proc.stderr
        while True:
            raw = await self._proc.stderr.readline()
            if not raw:
                break
            self.stderr.append(raw.decode("utf-8", errors="replace").rstrip("\n"))

    async def send_raw(self, line: str) -> None:
        assert self._proc and self._proc.stdin
        self._log("send", line)
        try:
            self._proc.stdin.write((line + "\n").encode())
            await self._proc.stdin.drain()
        except (BrokenPipeError, ConnectionResetError):
            pass

    async def request(self, method: str, params: dict | None = None, timeout_s: float = 30.0) -> Reply:
        mid = self._next_id
        self._next_id += 1
        msg: dict = {"jsonrpc": "2.0", "id": mid, "method": method}
        if params is not None:
            msg["params"] = params
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        self._pending[mid] = fut
        started = time.perf_counter()
        if not self.alive():
            self._pending.pop(mid, None)
            return Reply("closed")
        await self.send_raw(json.dumps(msg, ensure_ascii=False))
        try:
            reply = await asyncio.wait_for(fut, timeout_s)
        except TimeoutError:
            self._pending.pop(mid, None)
            return Reply("timeout", elapsed_ms=round((time.perf_counter() - started) * 1000, 1))
        elapsed = round((time.perf_counter() - started) * 1000, 1)
        if reply is None:
            return Reply("closed", elapsed_ms=elapsed)
        return Reply("error" if "error" in reply else "result", reply, elapsed)

    async def notify(self, method: str, params: dict | None = None) -> None:
        msg: dict = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        await self.send_raw(json.dumps(msg, ensure_ascii=False))

    async def initialize(self, timeout_s: float = 30.0) -> Reply:
        reply = await self.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {}, "clientInfo": CLIENT_INFO,
        }, timeout_s)
        if reply.kind == "result":
            await self.notify("notifications/initialized")
        return reply

    async def close(self, grace_s: float = 3.0) -> None:
        if self._proc is None:
            return
        if self._proc.stdin and not self._proc.stdin.is_closing():
            self._proc.stdin.close()
        try:
            await asyncio.wait_for(self._proc.wait(), grace_s)
        except TimeoutError:
            self._proc.terminate()
            try:
                await asyncio.wait_for(self._proc.wait(), grace_s)
            except TimeoutError:
                self._proc.kill()
                await self._proc.wait()
        for t in self._tasks:
            try:
                await asyncio.wait_for(t, 2)
            except (TimeoutError, asyncio.CancelledError):
                t.cancel()

    def dump(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / "wire.jsonl").open("w", encoding="utf-8") as f:
            for row in self.transcript:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        (directory / "stderr.log").write_text("\n".join(self.stderr) + "\n", encoding="utf-8")
