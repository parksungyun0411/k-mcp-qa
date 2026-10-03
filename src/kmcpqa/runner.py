"""전체 실행: 받기 → 설치 → 키 없이 시작 → 자리 표시자 키로 공통 시험 → 결과 저장.

    python -m kmcpqa.runner                       # servers.toml 전체
    python -m kmcpqa.runner --only korean-law-mcp

결과: reports/results/<id>.json, 원본 로그: reports/raw/<id>/ (wire.jsonl, stderr.log, install.log)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import platform
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from kmcpqa.manifest import ServerSpec, load
from kmcpqa.probe import ProbeConfig, full_probe, start_check
from kmcpqa.sandbox import Workspace
from kmcpqa.wire import PROTOCOL_VERSION


def tool_versions() -> dict:
    def v(cmd: list[str]) -> str | None:
        if not shutil.which(cmd[0]):
            return None
        return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

    return {"node": v(["node", "--version"]), "npm": v(["npm", "--version"]),
            "uv": v(["uv", "--version"]), "os": platform.platform()}


def sdk_versions(root: Path) -> dict:
    """설치된 MCP SDK 버전. 일부 동작은 서버 코드가 아니라 SDK 에서 온다."""
    out = {}
    pkg = root / "node_modules" / "@modelcontextprotocol" / "sdk" / "package.json"
    if pkg.exists():
        out["@modelcontextprotocol/sdk"] = json.loads(pkg.read_text())["version"]
    for dist in root.glob(".venv/lib/python*/site-packages/*.dist-info"):
        name, _, version = dist.name[: -len(".dist-info")].rpartition("-")
        if name.lower() in ("mcp", "fastmcp"):
            out[name.lower()] = version
    return out


async def run_server(ws: Workspace, spec: ServerSpec, reports: Path, cfg: ProbeConfig,
                     reinstall: bool = False) -> dict:
    raw = reports / "raw" / spec.id
    raw.mkdir(parents=True, exist_ok=True)
    record: dict = {"id": spec.id, "repo": spec.repo, "sha_expected": spec.sha,
                    "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
                    "protocol_version_requested": PROTOCOL_VERSION, "sandbox": ws.use_sandbox,
                    "command": spec.command, "install_steps": spec.install}
    if reinstall and ws.dir(spec).exists():
        shutil.rmtree(ws.dir(spec))  # 이전 설치 흔적 없이 처음부터
    record["sha_tested"] = await ws.fetch(spec)
    if record["sha_tested"] != spec.sha:
        record["error"] = "checkout sha mismatch"
        return record

    marker = ws.dir(spec) / ".installed"
    if reinstall or not marker.exists():
        (ws.logs(spec) / "install.log").unlink(missing_ok=True)
        steps = await ws.install(spec)
        record["install"] = {"ok": all(s.returncode == 0 for s in steps) and len(steps) == len(spec.install),
                             "steps": [s.__dict__ for s in steps]}
        if record["install"]["ok"]:
            marker.write_text(spec.sha)
    else:
        record["install"] = {"ok": True, "reused": True}
    shutil.copy(ws.logs(spec) / "install.log", raw / "install.log") \
        if (ws.logs(spec) / "install.log").exists() else None
    if not record["install"]["ok"]:
        return record

    record["sdk"] = sdk_versions(ws.cwd(spec))
    argv = ws.wrap(spec, spec.command)
    cwd = ws.cwd(spec)
    record["start_without_key"] = await start_check(argv, cwd, ws.env(spec, "none"), cfg, raw / "nokey")
    record["probe"] = await full_probe(argv, cwd, ws.env(spec, "placeholder"), cfg, raw / "probe")
    record["finished_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    return record


async def _main(args: argparse.Namespace) -> None:
    servers, _ = load(Path(args.manifest))
    if args.only:
        servers = [s for s in servers if s.id in set(args.only)]
    reports = Path(args.reports)
    (reports / "results").mkdir(parents=True, exist_ok=True)
    ws = Workspace(Path(args.workdir))
    cfg = ProbeConfig(call_timeout_s=args.call_timeout, max_tools=args.max_tools or None)
    meta = {"run_at": datetime.now(UTC).isoformat(timespec="seconds"), "tools": tool_versions(),
            "protocol_version_requested": PROTOCOL_VERSION}
    (reports / "results" / "_run.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    for spec in servers:
        print(f"[{spec.id}] start", flush=True)
        rec = await run_server(ws, spec, reports, cfg, args.reinstall)
        (reports / "results" / f"{spec.id}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        tools = (rec.get("probe") or {}).get("tools_list", {}).get("count")
        print(f"[{spec.id}] done install={rec.get('install', {}).get('ok')} tools={tools}", flush=True)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", default="servers.toml")
    p.add_argument("--reports", default="reports")
    p.add_argument("--workdir", default="/tmp/kmcp-work")
    p.add_argument("--only", nargs="*")
    p.add_argument("--call-timeout", type=float, default=20.0)
    p.add_argument("--max-tools", type=int, default=0)
    p.add_argument("--reinstall", action="store_true")
    asyncio.run(_main(p.parse_args()))


if __name__ == "__main__":
    main()
