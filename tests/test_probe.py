"""공통 시험을 픽스처 서버(SYNTHETIC)에 실제로 돌려 관찰 유형 분류를 확인한다."""

import sys
from collections import Counter
from pathlib import Path

import httpx
import pytest

from kmcpqa.bridge import StdioBridge
from kmcpqa.defects import TAXONOMY, findings
from kmcpqa.probe import ProbeConfig, full_probe, start_check
from kmcpqa.wire import WireSession

FIXTURE = Path(__file__).parent / "fixtures" / "fixture_server.py"
CFG = ProbeConfig(start_timeout_s=10, call_timeout_s=1.5, pause_s=0.05, idle_s=0.5)


def argv(mode: str) -> list[str]:
    return [sys.executable, str(FIXTURE), mode]


async def probe(mode: str, tmp_path: Path) -> dict:
    res = await full_probe(argv(mode), None, {"FIXTURE_NTS_BASE": "http://127.0.0.1:9"}, CFG, tmp_path)
    return {"install": {"ok": True}, "probe": res}


async def test_good_server_has_no_observations(tmp_path):
    record = await probe("good", tmp_path)
    p = record["probe"]
    assert p["initialize"]["spec_violations"] == []
    assert p["tools_list"]["count"] == 2
    assert p["unknown_method"]["error_code"] == -32601
    lookup = next(t for t in p["tools"] if t["name"] == "lookup")
    assert lookup["probes"]["missing_required"]["outcome"] == "tool_error"
    assert lookup["probes"]["valid"]["outcome"] == "ok"
    assert lookup["probes"]["valid"]["output_mismatch"] == []
    assert [f["code"] for f in findings(record)] == []


async def test_bad_server_observations_are_classified(tmp_path):
    record = await probe("bad", tmp_path)
    codes = Counter(f["code"] for f in findings(record))
    assert codes["P1"] == 1  # stdout 로그 줄
    assert codes["P3"] == 1 and codes["P6"] >= 1  # 알 수 없는 메서드에 응답 없이 종료
    assert codes["P4"] == 1  # 알 수 없는 툴을 isError 로
    assert codes["S2"] == 1  # required 에 없는 속성
    assert codes["P5"] >= 1  # hang
    assert codes["E3"] >= 1  # 입력 오류를 isError 없이
    assert codes["E1"] >= 1  # 인증 오류 문구를 isError 없이
    assert codes["E2"] >= 1  # -32603
    assert record["probe"]["restarts"] >= 1
    assert (tmp_path / "wire.jsonl").exists()
    lookup = next(t for t in record["probe"]["tools"] if t["name"] == "lookup")
    assert lookup["probes"]["valid"]["auth_marker"] == "SERVICE_KEY_IS_NOT_REGISTERED"


async def test_start_check_reports_exit(tmp_path):
    out = await start_check([sys.executable, "-c", "import sys; sys.exit(3)"], None, {}, CFG, tmp_path)
    assert out["initialize"] == "closed" and out["returncode"] == 3


def test_every_code_is_documented():
    assert all(len(v) == 2 and v[0] and v[1] for v in TAXONOMY.values())


async def test_bridge_passes_server_lines_through_unchanged():
    session = WireSession(argv("good"))
    await session.start()
    bridge = StdioBridge(session, timeout_s=5)
    transport = httpx.ASGITransport(app=bridge.app())
    async with httpx.AsyncClient(transport=transport, base_url="http://bridge") as client:
        r = await client.post("/mcp", json={"jsonrpc": "2.0", "id": 7, "method": "initialize",
                                            "params": {"protocolVersion": "2025-11-25",
                                                       "capabilities": {},
                                                       "clientInfo": {"name": "t", "version": "0"}}})
        n = await client.post("/mcp", json={"jsonrpc": "2.0", "method": "notifications/initialized"})
        g = await client.get("/mcp")
    await session.close()
    raw = [row["line"] for row in session.transcript if row["dir"] == "recv"][0]
    assert r.status_code == 200 and r.text == raw
    assert n.status_code == 202 and g.status_code == 405


@pytest.mark.parametrize("mode", ["good", "bad"])
async def test_transcript_records_both_directions(mode, tmp_path):
    await probe(mode, tmp_path)
    lines = (tmp_path / "wire.jsonl").read_text().splitlines()
    assert any('"dir": "send"' in x for x in lines) and any('"dir": "recv"' in x for x in lines)
