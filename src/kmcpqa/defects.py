"""관찰 유형 분류. 결과 JSON 한 개에서 재현 가능한 관찰만 뽑는다.

각 관찰은 코드, 툴, 근거(응답 일부), 재현 입력을 가진다. 판단이 들어가는 말은 쓰지 않고
"무엇을 보냈고 무엇이 돌아왔는가"만 남긴다.
"""

from __future__ import annotations

import re

TAXONOMY: dict[str, tuple[str, str]] = {
    # code: (분류, 설명)
    "I1": ("설치·기동", "고정한 커밋에서 문서의 설치 절차가 실패함"),
    "I2": ("설치·기동", "자리 표시자 키를 넣어도 initialize 응답이 오지 않음"),
    "I3": ("설치·기동", "자리 표시자 키로 시작한 뒤 요청 없이 5초 안에 프로세스가 종료됨"),
    "P1": ("프로토콜", "stdout 에 JSON-RPC 가 아닌 줄을 씀"),
    "P2": ("프로토콜", "응답이 MCP 2025-11-25 스키마를 어김"),
    "P3": ("프로토콜", "알 수 없는 메서드에 -32601 오류로 답하지 않음"),
    "P4": ("프로토콜", "알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함"),
    "P5": ("프로토콜", "tools/call 이 제한 시간 안에 응답하지 않음"),
    "P6": ("프로토콜", "요청 하나를 처리한 뒤 서버 프로세스가 종료됨"),
    "S1": ("스키마", "inputSchema/outputSchema 가 메타스키마 검증을 통과하지 못함"),
    "S2": ("스키마", "required 에 properties 에 없는 이름이 있음"),
    "S3": ("스키마", "outputSchema 를 선언했지만 structuredContent 가 없거나 스키마와 다름"),
    "R1": ("스키마-런타임 불일치", "선언된 필수 인자를 빼고 호출해도 오류 없이 결과를 돌려줌"),
    "R2": ("스키마-런타임 불일치", "선언과 다른 타입의 인자로 호출해도 오류 없이 결과를 돌려줌"),
    "R3": ("스키마-런타임 불일치", "스키마를 만족하는 입력을 인자 누락·형식 문제로 거부함"),
    "E1": ("오류 처리", "기관 API·실행 오류를 isError 없는 결과로 돌려줌 (자리 표시자 키 호출)"),
    "E2": ("오류 처리", "툴 실행 오류를 JSON-RPC 내부 오류(-32603)로 답함 (스펙은 isError 결과로 규정)"),
    "E3": ("오류 처리", "입력 검증 오류를 isError 없는 결과로 돌려줌"),
    "H1": ("오류 처리", "응답 본문에 Python traceback 과 서버 파일 경로가 담김"),
}

_ARG_COMPLAINT = re.compile(
    r"(필수|입력해|입력하|required|missing|must (be|provide|specify)|is not valid|형식|올바르지|"
    r"하나를|one of)", re.IGNORECASE)


def _obs(code: str, tool: str | None, evidence: str, args: object = None) -> dict:
    cat, desc = TAXONOMY[code]
    return {"code": code, "category": cat, "description": desc, "tool": tool,
            "evidence": evidence[:300], "args": args}


def findings(record: dict) -> list[dict]:
    out: list[dict] = []
    inst = record.get("install") or {}
    if inst and not inst.get("ok"):
        failed = next((s for s in inst.get("steps", []) if s.get("returncode") != 0), {})
        out.append(_obs("I1", None, f"step {failed.get('argv')} exit {failed.get('returncode')}"))
        return out
    probe = record.get("probe") or {}
    init = probe.get("initialize") or {}
    if init and init.get("outcome") != "result":
        last = " | ".join((init.get("stderr_tail") or [])[-2:])
        out.append(_obs("I2", None, f"initialize {init.get('outcome')}, stderr 마지막 줄: {last}"))
        return out
    if not probe:
        return out

    idle_exit = probe.get("idle_alive") is False
    if idle_exit:
        ie = probe.get("idle_exit") or {}
        tail = " | ".join(ie.get("stderr_tail") or [])
        out.append(_obs("I3", None, f"exit {ie.get('returncode')}: {tail}"))
    noise = probe.get("stdout_noise") or {}
    if noise.get("count"):
        out.append(_obs("P1", None, f"{noise['count']} lines, e.g. {noise.get('sample', [''])[0]!r}"))
    for where in ("initialize", "tools_list", "ping"):
        v = (probe.get(where) or {}).get("spec_violations") or []
        if v:
            out.append(_obs("P2", None, f"{where}: {v[0]}"))
    um = probe.get("unknown_method") or {}
    if um and not (um.get("outcome") == "error" and um.get("error_code") == -32601):
        out.append(_obs("P3", None, f"method=kmcpqa/unknown_method outcome={um.get('outcome')} "
                        f"code={um.get('error_code')}"))
    if um.get("alive_after") is False and not idle_exit:
        out.append(_obs("P6", None, "method=kmcpqa/unknown_method: process exited"))
    ut = probe.get("unknown_tool") or {}
    if ut.get("outcome") in ("tool_error", "ok"):
        out.append(_obs("P4", "kmcpqa_no_such_tool",
                        f"outcome={ut['outcome']}: {ut.get('text_excerpt', '')}", {}))
    if ut.get("alive_after") is False and not idle_exit:
        out.append(_obs("P6", "kmcpqa_no_such_tool", "process exited", {}))

    for t in probe.get("tools") or []:
        name = t["name"]
        traced = False
        for p in t.get("input_schema_problems") or []:
            out.append(_obs("S2" if p.startswith("required not in") else "S1", name, f"inputSchema {p}"))
        for p in t.get("output_schema_problems") or []:
            out.append(_obs("S2" if p.startswith("required not in") else "S1", name, f"outputSchema {p}"))
        for label, c in (t.get("probes") or {}).items():
            outcome = c.get("outcome")
            args = c.get("args")
            if outcome == "timeout":
                out.append(_obs("P5", name, f"{label}: no response in {c.get('elapsed_ms')} ms", args))
            if c.get("alive_after") is False and not idle_exit:
                out.append(_obs("P6", name, f"{label}: process exited after call", args))
            if outcome == "ok" and c.get("spec_violations"):
                out.append(_obs("P2", name, f"CallToolResult: {c['spec_violations'][0]}", args))
            if c.get("output_mismatch"):
                out.append(_obs("S3", name, f"{c['output_mismatch'][0]}", args))
            if outcome == "error" and c.get("error_code") == -32603:
                out.append(_obs("E2", name, f"{label}: {c.get('error_message')}", args))
            text = c.get("text_excerpt", "") or c.get("error_message", "") or ""
            if c.get("traceback") and not traced:
                traced = True
                out.append(_obs("H1", name, f"{label}: {text}", args))
            if label in ("missing_required", "wrong_type") and outcome == "ok":
                if c.get("error_marker"):
                    out.append(_obs("E3", name, f"{label} → isError 없음: {text}", args))
                else:
                    code = "R1" if label == "missing_required" else "R2"
                    out.append(_obs(code, name, f"required={t.get('required')} → {text}", args))
            if label == "valid":
                if outcome == "ok" and (c.get("auth_marker") or c.get("error_marker")):
                    marker = c.get("auth_marker") or c.get("error_marker")
                    out.append(_obs("E1", name, f"marker={marker!r}: {text}", args))
                elif outcome == "tool_error" and not c.get("auth_marker") and _ARG_COMPLAINT.search(text):
                    out.append(_obs("R3", name, text, args))
    return out


def summarize(all_findings: dict[str, list[dict]]) -> dict[str, dict[str, int]]:
    """서버별 코드별 건수."""
    return {sid: {code: sum(1 for f in fs if f["code"] == code) for code in TAXONOMY}
            for sid, fs in all_findings.items()}
