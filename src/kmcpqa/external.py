"""기존 도구 재사용: 공식 conformance 와 mcp-audit 을 같은 격리 환경에서 돌린다.

- modelcontextprotocol/conformance (npm @modelcontextprotocol/conformance): HTTP URL 만 받으므로
  bridge.StdioBridge 로 stdio 서버를 중계한다. 서버 쪽 시나리오 중 특정 참조 서버의 툴을 전제하지 않는
  server-initialize, ping, tools-list 만 돌린다.
- Alpha-W0lf/mcp-audit: stdio 명령을 직접 받는다. SCHEMA001·RUNTIME001·HYGIENE001 을 돌리고,
  읽기 전용 조회 툴임을 코드로 확인한 서버에만 --allow-tool 로 런타임 프로브를 허용한다.

    python -m kmcpqa.external --only korea-stock-mcp
"""

from __future__ import annotations

import argparse
import asyncio
import json
import shlex
import socket
from pathlib import Path

import uvicorn

from kmcpqa.bridge import StdioBridge
from kmcpqa.manifest import ServerSpec, load
from kmcpqa.sandbox import Workspace
from kmcpqa.wire import WireSession

CONFORMANCE_VERSION = "0.1.16"
CONFORMANCE_SCENARIOS = ["server-initialize", "ping", "tools-list"]
MCP_AUDIT_REPO = "https://github.com/Alpha-W0lf/mcp-audit"
MCP_AUDIT_SHA = "b14487ff9af2ea539fa946755949173459c2cbb9"
MCP_AUDIT_CHECKS = ["SCHEMA001", "RUNTIME001", "HYGIENE001"]


def tools_dir(ws: Workspace) -> Path:
    return ws.root / "_tools"


async def _sh(argv: list[str], cwd: Path | None = None, env: dict | None = None,
              timeout_s: float = 600) -> tuple[int | None, str]:
    proc = await asyncio.create_subprocess_exec(*argv, cwd=cwd, env=env, stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.STDOUT)
    try:
        out, _ = await asyncio.wait_for(proc.communicate(), timeout_s)
    except TimeoutError:
        proc.kill()
        out, _ = await proc.communicate()
        return None, out.decode(errors="replace")
    return proc.returncode, out.decode(errors="replace")


async def ensure_tools(ws: Workspace) -> None:
    root = tools_dir(ws)
    audit = root / "mcp-audit"
    if not (audit / ".venv" / "bin" / "mcp-audit").exists():
        root.mkdir(parents=True, exist_ok=True)
        if not audit.exists():
            await _sh(["git", "clone", "-q", MCP_AUDIT_REPO, str(audit)])
        await _sh(["git", "-C", str(audit), "checkout", "-q", "--detach", MCP_AUDIT_SHA])
        await _sh(["uv", "venv", "-q", "-p", "3.12", ".venv"], cwd=audit)
        await _sh(["uv", "pip", "install", "-q", "-p", ".venv", "-e", "."], cwd=audit)
    conf = root / "conformance"
    if not (conf / "node_modules" / ".bin" / "conformance").exists():
        conf.mkdir(parents=True, exist_ok=True)
        await _sh(["npm", "init", "-y"], cwd=conf)
        await _sh(["npm", "install", "--ignore-scripts", "--no-audit", "--no-fund",
                   f"@modelcontextprotocol/conformance@{CONFORMANCE_VERSION}"], cwd=conf)


async def run_mcp_audit(ws: Workspace, spec: ServerSpec, tool_names: list[str], out: Path) -> dict:
    """mcp-audit 은 서버에 환경 변수를 넘기지 않으므로(SDK 기본 환경만 전달) env -i 로 직접 감싼다."""
    env = ws.env(spec, "placeholder")
    server = ["/usr/bin/env", "-i", *[f"{k}={v}" for k, v in env.items()], *spec.command]
    inside = ws.dir(spec) / "mcp-audit.json"  # 샌드박스는 작업 디렉터리 안에만 쓸 수 있다
    inside.unlink(missing_ok=True)
    argv = [str(tools_dir(ws) / "mcp-audit" / ".venv" / "bin" / "mcp-audit"), "run",
            "--server", shlex.join(server), "--json", str(inside),
            "--startup-timeout", "30", "--call-timeout", "20"]
    for c in MCP_AUDIT_CHECKS:
        argv += ["--only", c]
    for t in tool_names:
        argv += ["--allow-tool", t]
    rc, log = await _sh(ws.wrap(spec, argv), cwd=ws.cwd(spec), env=env, timeout_s=1800)
    (out / "mcp-audit.log").write_text(log, encoding="utf-8")
    report = None
    if inside.exists():
        (out / "mcp-audit.json").write_text(inside.read_text(), encoding="utf-8")
        report = json.loads(inside.read_text())
    return {"returncode": rc, "report": report}


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


async def run_conformance(ws: Workspace, spec: ServerSpec, out: Path) -> dict:
    session = WireSession(ws.wrap(spec, spec.command), ws.cwd(spec), ws.env(spec, "placeholder"))
    await session.start()
    port = _free_port()
    bridge = StdioBridge(session)
    server = uvicorn.Server(uvicorn.Config(bridge.app(), host="127.0.0.1", port=port, log_level="warning"))
    serve = asyncio.create_task(server.serve())
    while not server.started:
        await asyncio.sleep(0.05)
    results = {}
    conf_bin = str(tools_dir(ws) / "conformance" / "node_modules" / ".bin" / "conformance")
    try:
        for scenario in CONFORMANCE_SCENARIOS:
            sdir = out / "conformance" / scenario
            sdir.mkdir(parents=True, exist_ok=True)
            seen = len(bridge.events)
            rc, log = await _sh([conf_bin, "server", "--url", f"http://127.0.0.1:{port}/mcp",
                                 "--scenario", scenario, "--spec-version", "2025-11-25",
                                 "-o", str(sdir)], env=ws.env(spec, "none"), timeout_s=300)
            (sdir / "stdout.log").write_text(log, encoding="utf-8")
            checks = []
            for f in sdir.rglob("checks.json"):
                checks += json.loads(f.read_text())
            events = bridge.events[seen:]
            # 중계기가 서버 대신 만든 응답이 있으면 이 시나리오는 서버를 잰 것이 아니다
            measurable = not any(e["kind"] in ("server_not_running", "server_exited") for e in events)
            results[scenario] = {"returncode": rc, "measurable": measurable, "bridge_events": events,
                                 "checks": [
                {"id": c.get("id"), "status": c.get("status"), "description": c.get("description"),
                 "errorMessage": c.get("errorMessage")} for c in checks]}
    finally:
        server.should_exit = True
        await serve
        await session.close()
        session.dump(out / "conformance")
    return results


async def _main(args: argparse.Namespace) -> None:
    servers, _ = load(Path(args.manifest))
    if args.only:
        servers = [s for s in servers if s.id in set(args.only)]
    ws = Workspace(Path(args.workdir))
    await ensure_tools(ws)
    reports = Path(args.reports)
    for spec in servers:
        result_path = reports / "results" / f"{spec.id}.json"
        if not result_path.exists():
            print(f"[{spec.id}] no probe result; run kmcpqa.runner first")
            continue
        record = json.loads(result_path.read_text())
        tool_names = [t["name"] for t in (record.get("probe") or {}).get("tools") or []]
        if not tool_names:
            print(f"[{spec.id}] no tools listed; skip external tools")
            continue
        out = reports / "raw" / spec.id / "external"
        out.mkdir(parents=True, exist_ok=True)
        print(f"[{spec.id}] conformance", flush=True)
        conf = await run_conformance(ws, spec, out)
        print(f"[{spec.id}] mcp-audit", flush=True)
        audit = await run_mcp_audit(ws, spec, tool_names, out)
        record["external"] = {"conformance_version": CONFORMANCE_VERSION, "conformance": conf,
                              "mcp_audit_sha": MCP_AUDIT_SHA, "mcp_audit": audit}
        result_path.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", default="servers.toml")
    p.add_argument("--reports", default="reports")
    p.add_argument("--workdir", default="/tmp/kmcp-work")
    p.add_argument("--only", nargs="*")
    asyncio.run(_main(p.parse_args()))


if __name__ == "__main__":
    main()
