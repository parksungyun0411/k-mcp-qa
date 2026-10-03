"""결과 JSON → 보고서.

    python -m kmcpqa.report

만드는 파일
- reports/RESULTS.md            서버별 요약, 관찰 유형별 건수, 실행 환경
- reports/findings/<id>.md      관찰 목록과 재현 명령
- reports/upstream-drafts/<id>.md  이슈 초안. 올리지 않는다(사용자 검토용)
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from kmcpqa.defects import TAXONOMY, findings
from kmcpqa.manifest import load
from kmcpqa.specschema import SPEC_SOURCE

SDK_CODES = {"P3", "P4"}


def load_results(results_dir: Path) -> tuple[dict, dict[str, dict]]:
    meta = json.loads((results_dir / "_run.json").read_text()) if (results_dir / "_run.json").exists() else {}
    recs = {}
    for f in sorted(results_dir.glob("*.json")):
        if f.name.startswith("_"):
            continue
        r = json.loads(f.read_text(encoding="utf-8"))
        recs[r["id"]] = r
    return meta, recs


def commit_date(workdir: Path, server_id: str, sha: str) -> str:
    src = workdir / server_id / "src"
    if not (src / ".git").exists():
        return ""
    out = subprocess.run(["git", "-C", str(src), "log", "-1", "--format=%cs", sha], capture_output=True,
                         text=True)
    return out.stdout.strip()


def sdk_label(rec: dict) -> str:
    return ", ".join(f"{k} {v}" for k, v in (rec.get("sdk") or {}).items()) or "-"


def conformance_cell(rec: dict) -> str:
    conf = (rec.get("external") or {}).get("conformance") or {}
    if not conf:
        return "-"
    cells = []
    for scenario, v in conf.items():
        statuses = [c["status"] for c in v.get("checks", [])]
        ok = statuses and all(s == "SUCCESS" for s in statuses)
        cells.append(f"{scenario} {'통과' if ok else '실패' if statuses else '결과 없음'}")
    return "<br>".join(cells)


def audit_cell(rec: dict) -> str:
    rep = ((rec.get("external") or {}).get("mcp_audit") or {}).get("report")
    if not rep:
        return "-"
    c = Counter(r.get("status") for r in rep.get("results", []))
    return f"pass {c.get('pass', 0)} / fail {c.get('fail', 0)} / skip {c.get('skip', 0)}"


def start_cell(rec: dict) -> str:
    s = rec.get("start_without_key") or {}
    if not s:
        return "-"
    return "시작함" if s.get("initialize") == "result" else f"종료(코드 {s.get('returncode')})"


def repro_cmd(server_id: str, f: dict) -> str:
    if f["code"] in ("P3",) or (f["code"] == "P6" and f["tool"] is None):
        return f"python -m kmcpqa.repro {server_id} kmcpqa/unknown_method '{{}}'"
    if f["tool"] and f["args"] is not None:
        params = json.dumps({"name": f["tool"], "arguments": f["args"]}, ensure_ascii=False)
        return f"python -m kmcpqa.repro {server_id} tools/call {shlex.quote(params)}"
    return f"python -m kmcpqa.runner --only {server_id}"


def shared_sdk_note(code: str, rec: dict, by_code_sdk: dict) -> str:
    key = (code, sdk_label(rec))
    others = sorted(s for s in by_code_sdk.get(key, set()) if s != rec["id"])
    if code in SDK_CODES and others:
        return f"같은 SDK({sdk_label(rec)})를 쓰는 {', '.join(others)} 에서도 같은 유형이 관찰됨"
    return ""


def render(meta: dict, recs: dict[str, dict], manifest_path: Path, workdir: Path, out: Path) -> None:
    servers, skipped = load(manifest_path)
    specs = {s.id: s for s in servers}
    all_f = {sid: findings(r) for sid, r in recs.items()}
    by_code_sdk: dict[tuple, set] = defaultdict(set)
    for sid, fs in all_f.items():
        for f in fs:
            by_code_sdk[(f["code"], sdk_label(recs[sid]))].add(sid)

    run_at = meta.get("run_at", "")
    tools = meta.get("tools", {})
    any_ext = next((r["external"] for r in recs.values() if r.get("external")), {})
    lines = [
        "# 결과", "",
        f"실행: {run_at} (UTC) · 요청한 프로토콜 버전 {meta.get('protocol_version_requested')} · "
        f"node {tools.get('node')} · npm {tools.get('npm')} · {tools.get('uv')} · {tools.get('os')}", "",
        f"스펙 스키마: `{SPEC_SOURCE}`  ",
        f"공식 conformance: `@modelcontextprotocol/conformance@{any_ext.get('conformance_version', '-')}` "
        f"(server-initialize, ping, tools-list)  ",
        f"mcp-audit: `Alpha-W0lf/mcp-audit@{any_ext.get('mcp_audit_sha', '-')}` "
        f"(SCHEMA001, RUNTIME001, HYGIENE001)", "",
        "모든 서버는 실제 키 없이 실행했다. 키 변수에는 자리 표시자 문자열을 넣었다. "
        "따라서 기관 API 를 실제로 부르는 호출은 인증 오류를 받는 것이 정상이며, "
        "아래 표는 그 상황에서의 동작이다.", "",
        "## 서버별 요약", "",
        "| 서버 | 커밋 (날짜) | 라이선스 | MCP SDK | 설치 | 키 없이 시작 | initialize (협상 버전) | 툴 수 "
        "| 공식 conformance | mcp-audit |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, r in recs.items():
        spec = specs.get(sid)
        p = r.get("probe") or {}
        init = p.get("initialize") or {}
        init_cell = f"응답 ({init.get('protocolVersion')})" if init.get("outcome") == "result" \
            else (init.get("outcome") or "-")
        sha = r.get("sha_tested", "")[:10]
        date = commit_date(workdir, sid, r.get("sha_tested", ""))
        name = f"[{sid}](findings/{sid}.md)"
        if spec and spec.modification:
            name += f"<br>(변형: {spec.modification})"
        lines.append(
            f"| {name} | `{sha}` ({date}) | {spec.license if spec else ''} | {sdk_label(r)} "
            f"| {'성공' if (r.get('install') or {}).get('ok') else '실패'} | {start_cell(r)} | {init_cell} "
            f"| {(p.get('tools_list') or {}).get('count', '-')} | {conformance_cell(r)} | {audit_cell(r)} |")

    used = [c for c in TAXONOMY if any(f["code"] == c for fs in all_f.values() for f in fs)]
    lines += ["", "## 관찰 유형별 건수", "",
              "툴 하나에서 여러 입력으로 같은 유형이 나오면 각각 센다. 유형 정의는 아래 표.", "",
              "| 서버 | " + " | ".join(used) + " |", "|---|" + "---|" * len(used)]
    for sid, fs in all_f.items():
        c = Counter(f["code"] for f in fs)
        lines.append(f"| {sid} | " + " | ".join(str(c.get(code, 0)) for code in used) + " |")
    lines += ["", "## 관찰 유형", "", "| 코드 | 분류 | 내용 |", "|---|---|---|"]
    lines += [f"| {c} | {cat} | {desc} |" for c, (cat, desc) in TAXONOMY.items()]
    lines += ["", "## 시험하지 않은 서버", "", "| 저장소 | 커밋 | 이유 |", "|---|---|---|"]
    lines += [f"| {s.repo} | `{s.sha[:10]}` | {s.reason} |" for s in skipped]
    out.mkdir(parents=True, exist_ok=True)
    (out / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    fdir, ddir = out / "findings", out / "upstream-drafts"
    fdir.mkdir(exist_ok=True)
    ddir.mkdir(exist_ok=True)
    for sid, fs in all_f.items():
        r = recs[sid]
        head = [f"# {sid}", "",
                f"- 저장소: https://github.com/{r['repo']} @ `{r.get('sha_tested')}`",
                f"- 실행 시각: {r.get('started_at')} (UTC), 샌드박스: {r.get('sandbox')}",
                f"- 설치: {' && '.join(' '.join(s) for s in r.get('install_steps', []))}",
                f"- 실행 명령: `{' '.join(r.get('command', []))}`, MCP SDK: {sdk_label(r)}",
                f"- 원본 로그: `reports/raw/{sid}/`", ""]
        body = []
        for code in TAXONOMY:
            group = [f for f in fs if f["code"] == code]
            if not group:
                continue
            body += [f"## {code} · {TAXONOMY[code][1]} ({len(group)}건)", ""]
            note = shared_sdk_note(code, r, by_code_sdk)
            if note:
                body += [f"> {note}", ""]
            for f in group[:20]:
                args = json.dumps(f["args"], ensure_ascii=False) if f["args"] is not None else "-"
                body += [f"- 툴 `{f['tool'] or '-'}` · 입력 `{args}`",
                         f"  - 응답: {f['evidence']!r}",
                         f"  - 재현: `{repro_cmd(sid, f)}`"]
            if len(group) > 20:
                body.append(f"- 외 {len(group) - 20}건은 `reports/results/{sid}.json` 참고")
            body.append("")
        if not body:
            body = ["관찰된 항목이 없다.", ""]
        (fdir / f"{sid}.md").write_text("\n".join(head + body), encoding="utf-8")

        if fs:
            draft = ["<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. "
                     "올리기 전 내용을 직접 재현·검토할 것. -->",
                     f"# [재현 보고] {sid}: MCP 공통 시험에서 관찰한 동작", "",
                     "안녕하세요. 한국 공공데이터 MCP 서버들에 같은 시험을 돌려 보다가 "
                     "아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다.",
                     "",
                     "## 환경", "",
                     f"- 커밋: `{r.get('sha_tested')}`",
                     f"- 실행 명령: `{' '.join(r.get('command', []))}`",
                     f"- MCP SDK: {sdk_label(r)}, "
                     f"클라이언트 요청 프로토콜 버전 {r.get('protocol_version_requested')}",
                     f"- 날짜: {r.get('started_at', '')[:10]}", "", "## 관찰", ""]
            for code in TAXONOMY:
                group = [f for f in fs if f["code"] == code]
                if not group:
                    continue
                f = group[0]
                args = json.dumps(f["args"], ensure_ascii=False) if f["args"] is not None else "-"
                draft += [f"### {TAXONOMY[code][1]}", "",
                          f"- 툴 `{f['tool'] or '-'}`, 입력 `{args}` (같은 유형 {len(group)}건)",
                          f"- 응답: `{f['evidence'][:200]}`"]
                note = shared_sdk_note(code, r, by_code_sdk)
                if note:
                    draft.append(f"- 참고: {note}. 서버 코드가 아니라 SDK 동작일 수 있습니다.")
                draft.append("")
            draft += ["## 재현", "", "요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다. "
                      "MCP 2025-11-25 스펙의 해당 항목과 다르게 보이는 부분만 적었습니다. "
                      "의도된 동작이라면 알려 주세요.", ""]
            (ddir / f"{sid}.md").write_text("\n".join(draft), encoding="utf-8")


def redact_tree(root: Path, home: str) -> int:
    """보고서 파일에 남은 이 머신의 홈 경로를 ~ 로 바꾼다(서버 traceback·실행 명령에 섞여 들어온다)."""
    changed = 0
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix not in (".json", ".jsonl", ".log", ".md", ".txt"):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if home in text:
            f.write_text(text.replace(home, "~"), encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", default="servers.toml")
    p.add_argument("--reports", default="reports")
    p.add_argument("--workdir", default="/tmp/kmcp-work")
    a = p.parse_args()
    redact_tree(Path(a.reports), str(Path.home()))
    meta, recs = load_results(Path(a.reports) / "results")
    render(meta, recs, Path(a.manifest), Path(a.workdir), Path(a.reports))
    print(f"→ {a.reports}/RESULTS.md ({len(recs)} servers)")


if __name__ == "__main__":
    main()
