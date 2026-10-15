"""결과 JSON → 보고서.

    python -m kmcpqa.report

만드는 파일
- reports/RESULTS.md               서버별 요약, 출처별 관찰(서버 코드 / SDK 기본 동작 / 미확인), 실행 환경
- reports/findings/<id>.md         문구 유형별 관찰, 소스 위치, 재현 명령
- reports/upstream-drafts/<id>.md  서버 코드에서 나온 관찰만 담은 이슈 초안. 올리지 않는다(사용자 검토용)
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from collections import Counter
from pathlib import Path

from kmcpqa.defects import (
    BASIS,
    JSONRPC_QUOTE,
    JSONRPC_URL,
    SPEC_TOOLS_ERRORS_QUOTE,
    SPEC_TOOLS_ERRORS_URL,
    TAXONOMY,
    findings,
    group_causes,
)
from kmcpqa.manifest import ServerSpec, load
from kmcpqa.specschema import SPEC_SOURCE

ORIGIN_LABEL = {"server": "서버 코드", "sdk": "SDK 기본 동작(확인)", "unknown": "출처 미확인"}


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


def server_root(workdir: Path, spec: ServerSpec | None) -> Path | None:
    if spec is None:
        return None
    root = workdir / spec.id / "src"
    root = root / spec.subdir if spec.subdir else root
    return root if root.exists() else None


def sdk_label(rec: dict) -> str:
    return ", ".join(f"{k} {v}" for k, v in (rec.get("sdk") or {}).items()) or "-"


def conformance_status(v: dict) -> str:
    if v.get("measurable") is False:
        return "측정 불가(서버 프로세스 종료)"
    statuses = [c["status"] for c in v.get("checks", [])]
    if not statuses:
        return "결과 없음"
    return "통과" if all(s == "SUCCESS" for s in statuses) else "실패"


def conformance_cell(rec: dict) -> str:
    conf = (rec.get("external") or {}).get("conformance") or {}
    if not conf:
        return "-"
    return "<br>".join(f"{scenario} {conformance_status(v)}" for scenario, v in conf.items())


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
    if f["code"] == "P3" or (f["code"] == "P6" and f["tool"] is None):
        return f"python -m kmcpqa.repro {server_id} kmcpqa/unknown_method '{{}}'"
    if f["code"] in ("I2", "I3"):
        return f"python -m kmcpqa.runner --only {server_id}"
    if f["tool"] and f["args"] is not None:
        params = json.dumps({"name": f["tool"], "arguments": f["args"]}, ensure_ascii=False)
        return f"python -m kmcpqa.repro {server_id} tools/call {shlex.quote(params)}"
    return f"python -m kmcpqa.runner --only {server_id}"


def where_text(g: dict) -> str:
    w = ", ".join(f"`{x}`" for x in (g.get("where") or [])) or "소스 위치 미확인"
    return w + (f" — {g['note']}" if g.get("note") else "")


def tool_count(rec: dict) -> int:
    return ((rec.get("probe") or {}).get("tools_list") or {}).get("count") or 0


def basis_line(code: str) -> str:
    key = TAXONOMY[code][2]
    if not key:
        return ""
    url, kind = BASIS[key]
    return f"근거: [{url}]({url}) ({kind})"


def render(meta: dict, recs: dict[str, dict], manifest_path: Path, workdir: Path, out: Path) -> dict:
    servers, skipped = load(manifest_path)
    specs = {s.id: s for s in servers}
    all_f = {sid: findings(r, server_root(workdir, specs.get(sid))) for sid, r in recs.items()}
    causes = {sid: group_causes(fs) for sid, fs in all_f.items()}

    tools = meta.get("tools", {})
    any_ext = next((r["external"] for r in recs.values() if r.get("external")), {})
    lines = [
        "# 결과", "",
        f"실행: {meta.get('run_at', '')} (UTC) · 요청한 프로토콜 버전 {meta.get('protocol_version_requested')} · "
        f"node {tools.get('node')} · npm {tools.get('npm')} · {tools.get('uv')} · {tools.get('os')}", "",
        f"스펙 스키마: `{SPEC_SOURCE}`  ",
        f"공식 conformance: `@modelcontextprotocol/conformance@{any_ext.get('conformance_version', '-')}` "
        "(server-initialize, ping, tools-list)  ",
        f"mcp-audit: `Alpha-W0lf/mcp-audit@{any_ext.get('mcp_audit_sha', '-')}` (SCHEMA001, RUNTIME001, HYGIENE001)",
        "",
        "모든 서버는 실제 키 없이 실행했다. 키 변수에는 자리 표시자 문자열을 넣었다. "
        "따라서 기관 API 를 실제로 부르는 호출은 인증 오류를 받는 것이 정상이며, "
        "아래 표는 그 상황에서의 동작이다.", "",
        "관찰은 출처별로 나눈다. **서버 코드**: 응답 문구·스택이 서버 저장소 소스에서 확인되었거나 툴 핸들러가 "
        "만든 응답. **SDK 기본 동작(확인)**: 응답 문구·스택이 설치된 MCP SDK 소스에서만 확인됨 — 서버에 대한 "
        "관찰이 아니다. **출처 미확인**: 어느 쪽에서도 위치를 찾지 못함.", "",
        "## 서버별 요약", "",
        "| 서버 | 커밋 (날짜) | 라이선스 | MCP SDK | 설치 | 키 없이 시작 | initialize (협상 버전) | 툴 수 "
        "| 공식 conformance | mcp-audit |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, r in recs.items():
        spec = specs.get(sid)
        init = (r.get("probe") or {}).get("initialize") or {}
        init_cell = f"응답 ({init.get('protocolVersion')})" if init.get("outcome") == "result" \
            else (init.get("outcome") or "-")
        name = f"[{sid}](findings/{sid}.md)"
        if spec and spec.modification:
            name += f"<br>(변형: {spec.modification})"
        lines.append(
            f"| {name} | `{r.get('sha_tested', '')[:10]}` ({commit_date(workdir, sid, r.get('sha_tested', ''))}) "
            f"| {spec.license if spec else ''} | {sdk_label(r)} "
            f"| {'성공' if (r.get('install') or {}).get('ok') else '실패'} | {start_cell(r)} | {init_cell} "
            f"| {tool_count(r) or '-'} | {conformance_cell(r)} | {audit_cell(r)} |")
    lines += ["", "`측정 불가(서버 프로세스 종료)`: 시나리오 도중 서버 프로세스가 이미 종료되어, 응답을 "
              "k-mcp-qa 중계기가 대신 만든 경우다(중계기 오류 코드 -32099). 서버의 conformance 실패로 세지 않는다."]

    server_codes = [c for c in TAXONOMY if any(g["code"] == c and g["origin"] == "server"
                                               for gs in causes.values() for g in gs)]
    lines += ["", "## 서버 코드에서 나온 관찰", "",
              "칸의 값은 `문구 유형 수/발생 수`. 같은 코드·같은 출처·같은 문구(입력 값·숫자 제거)를 한 문구 유형으로 "
              "묶었다. 근본 원인 수가 아니며, 같은 소스 줄에서 나온 응답도 입력 종류나 응답 모양에 따라 여러 유형으로 "
              "나뉠 수 있다. 발생 수는 툴 수에 비례해 늘어나므로 서버 사이 비교에는 문구 유형 수나 "
              "툴당 발생 수를 본다.",
              "",
              "| 서버 | 툴 수 | 문구 유형 수 | 발생 수 | 툴당 발생 | " + " | ".join(server_codes) + " |",
              "|---|---:|---:|---:|---:|" + "---|" * len(server_codes)]
    summary: dict[str, dict] = {}
    for sid, gs in causes.items():
        sg = [g for g in gs if g["origin"] == "server"]
        n_tools = tool_count(recs[sid])
        occ = sum(g["count"] for g in sg)
        per_tool = f"{occ / n_tools:.2f}" if n_tools else "-"
        cells = []
        for code in server_codes:
            cg = [g for g in sg if g["code"] == code]
            cells.append(f"{len(cg)}/{sum(g['count'] for g in cg)}" if cg else "")
        lines.append(f"| {sid} | {n_tools or '-'} | {len(sg)} | {occ} | {per_tool} | " + " | ".join(cells) + " |")
        summary[sid] = {"tools": n_tools, "server_phrase_types": len(sg), "server_occurrences": occ,
                        "server_codes": sorted({g["code"] for g in sg}),
                        "sdk_codes": sorted({g["code"] for g in gs if g["origin"] == "sdk"}),
                        "unknown_codes": sorted({g["code"] for g in gs if g["origin"] == "unknown"})}

    lines += ["", "## SDK 기본 동작으로 확인된 관찰 (서버에 대한 관찰이 아님)", "",
              "| 서버 | 코드 | SDK | SDK 소스 위치 | 응답 |", "|---|---|---|---|---|"]
    for sid, gs in causes.items():
        for g in gs:
            if g["origin"] == "sdk":
                lines.append(f"| {sid} | {g['code']} | {sdk_label(recs[sid])} | {where_text(g)} "
                             f"| {g['example']['evidence'][:120]!r} |")
    unknown = [(sid, g) for sid, gs in causes.items() for g in gs if g["origin"] == "unknown"]
    if unknown:
        lines += ["", "## 출처를 확인하지 못한 관찰", "", "| 서버 | 코드 | 발생 수 | 응답 |", "|---|---|---:|---|"]
        lines += [f"| {sid} | {g['code']} | {g['count']} | {g['example']['evidence'][:120]!r} |"
                  for sid, g in unknown]

    lines += ["", "## 관찰 유형", "", "| 코드 | 분류 | 내용 | 근거 |", "|---|---|---|---|"]
    for c, (cat, desc, key) in TAXONOMY.items():
        lines.append(f"| {c} | {cat} | {desc} | {BASIS[key][1] + ' — ' + BASIS[key][0] if key else '-'} |")
    lines += ["", "## 근거 문장 (원문 그대로)", "",
              f"MCP 2025-11-25, Tools › Error Handling — {SPEC_TOOLS_ERRORS_URL}", "",
              *[f"> {ln}" for ln in SPEC_TOOLS_ERRORS_QUOTE.splitlines()], "",
              "이 절에는 MUST/SHOULD 같은 규범 키워드가 없다. P4·E1·E2·E3 은 이 서술과 다른 동작을 기록한 것이며 "
              "스펙 위반 판정이 아니다.", "",
              f"JSON-RPC 2.0, Error object — {JSONRPC_URL}", "", f"> {JSONRPC_QUOTE}", ""]
    lines += ["## 시험하지 않은 서버", "", "| 저장소 | 커밋 | 이유 |", "|---|---|---|"]
    lines += [f"| {s.repo} | `{s.sha[:10]}` | {s.reason} |" for s in skipped]
    out.mkdir(parents=True, exist_ok=True)
    (out / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")

    fdir, ddir = out / "findings", out / "upstream-drafts"
    fdir.mkdir(exist_ok=True)
    ddir.mkdir(exist_ok=True)
    for old in ddir.glob("*.md"):
        old.unlink()
    for sid, gs in causes.items():
        r = recs[sid]
        body = [f"# {sid}", "",
                f"- 저장소: https://github.com/{r['repo']} @ `{r.get('sha_tested')}`",
                f"- 실행 시각: {r.get('started_at')} (UTC), 샌드박스: {r.get('sandbox')}",
                f"- 설치: {' && '.join(' '.join(s) for s in r.get('install_steps', []))}",
                f"- 실행 명령: `{' '.join(r.get('command', []))}`, MCP SDK: {sdk_label(r)}",
                f"- 툴 수: {tool_count(r)}, 원본 로그: `reports/raw/{sid}/`", ""]
        if not gs:
            body.append("관찰된 항목이 없다.")
        for origin in ("server", "sdk", "unknown"):
            og = [g for g in gs if g["origin"] == origin]
            if not og:
                continue
            body += [f"## {ORIGIN_LABEL[origin]}", ""]
            for g in sorted(og, key=lambda g: (list(TAXONOMY).index(g["code"]), -g["count"])):
                ex = g["example"]
                args = json.dumps(ex["args"], ensure_ascii=False) if ex["args"] is not None else "-"
                tools_ = ", ".join(sorted(g["tools"])[:8]) + (" 외" if len(g["tools"]) > 8 else "")
                body += [f"### {g['code']} · {TAXONOMY[g['code']][1]} — 발생 {g['count']}건",
                         "", f"- 툴: {tools_ or '-'}", f"- 소스 위치: {where_text(g)}",
                         f"- 예시 입력: `{args}`", f"- 응답: {ex['evidence']!r}",
                         f"- 재현: `{repro_cmd(sid, ex)}`"]
                if basis_line(g["code"]):
                    body.append(f"- {basis_line(g['code'])}")
                body.append("")
        (fdir / f"{sid}.md").write_text("\n".join(body) + "\n", encoding="utf-8")

        sg = [g for g in gs if g["origin"] == "server"]
        if not sg:
            continue
        draft = ["<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->",
                 f"# [재현 보고] {sid}: 공통 시험에서 관찰한 동작", "",
                 "한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. "
                 "실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.", "",
                 "## 환경", "", f"- 커밋: `{r.get('sha_tested')}`",
                 f"- 실행 명령: `{' '.join(r.get('command', []))}`",
                 f"- MCP SDK: {sdk_label(r)}, 클라이언트 요청 프로토콜 버전 {r.get('protocol_version_requested')}",
                 f"- 날짜: {r.get('started_at', '')[:10]}", "", "## 관찰", ""]
        for g in sorted(sg, key=lambda g: list(TAXONOMY).index(g["code"])):
            ex = g["example"]
            args = json.dumps(ex["args"], ensure_ascii=False) if ex["args"] is not None else "-"
            draft += [f"### {TAXONOMY[g['code']][1]} (발생 {g['count']}건)", "",
                      f"- 예시: 툴 `{ex['tool'] or '-'}`, 입력 `{args}`",
                      f"- 응답: `{ex['evidence'][:240]}`", f"- 소스 위치: {where_text(g)}"]
            if TAXONOMY[g["code"]][2] == "tools_errors":
                draft.append(f"- 참고: MCP 2025-11-25 Tools › Error Handling ({SPEC_TOOLS_ERRORS_URL}) 의 서술과 "
                             "다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.")
            draft.append("")
        draft += ["## 재현", "", "요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.", ""]
        (ddir / f"{sid}.md").write_text("\n".join(draft), encoding="utf-8")
    return summary


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
