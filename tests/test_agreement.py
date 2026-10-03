"""직접 호출 일치 검사. 가짜 업스트림(SYNTHETIC)을 HTTP 로 띄우고 픽스처 MCP 서버와 직접 호출을 비교한다.
여기서 나오는 일치 여부는 테스트 단언이며 실측 결과가 아니다."""

import asyncio
import socket
import sys
from pathlib import Path

import httpx
import pytest
import uvicorn

from kmcpqa.agreement import Case, compare, run_case
from kmcpqa.direct.fake_upstream import build_fake_upstream, load_companies
from kmcpqa.wire import WireSession

FIX = Path(__file__).parent / "fixtures"
CASE = Case(tool="status", args={"b_no": "0000000011"}, direct="nts_status",
            direct_args={"b_no": "0000000011"}, fields=["b_no", "b_stt_cd"])
KEYS = {"DATA_GO_KR_SERVICE_KEY": "SYNTHETIC", "OPENDART_API_KEY": "SYNTHETIC"}


@pytest.fixture
async def upstream():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    app = build_fake_upstream(load_companies(FIX / "synthetic_companies.json"))
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    task = asyncio.create_task(server.serve())
    while not server.started:
        await asyncio.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    await task


async def _run(mode: str, base: str) -> dict:
    session = WireSession([sys.executable, str(FIX / "fixture_server.py"), mode],
                          env={"FIXTURE_NTS_BASE": f"{base}/nts"})
    await session.start()
    await session.initialize()
    async with httpx.AsyncClient() as http:
        out = await run_case(session, CASE, http, KEYS, bases={"nts": f"{base}/nts"})
    await session.close()
    return out


async def test_agreeing_server(upstream):
    out = await _run("good", upstream)
    assert out["status"] == "compared" and out["agree"] is True
    assert out["fields"]["b_no"] == {"direct": "0000000011", "found_in_mcp": True}


async def test_disagreeing_server_is_detected(upstream):
    out = await _run("skew", upstream)
    assert out["status"] == "compared" and out["agree"] is False
    assert out["fields"]["b_no"]["found_in_mcp"] is False


async def test_direct_failure_is_not_counted_as_disagreement(upstream):
    session = WireSession([sys.executable, str(FIX / "fixture_server.py"), "good"],
                          env={"FIXTURE_NTS_BASE": f"{upstream}/nts"})
    await session.start()
    await session.initialize()
    async with httpx.AsyncClient() as http:
        out = await run_case(session, CASE, http, KEYS, bases={"nts": "http://127.0.0.1:9"})
    await session.close()
    assert out["status"] == "direct_failed"


def test_compare_uses_structured_content_and_text():
    record = {"b_no": "000-00-00011"}
    result = {"content": [], "structuredContent": {"bno": "0000000011"}}
    assert compare(Case("t", {}, "nts_status", {}, ["b_no"]), record, result)["agree"] is True
