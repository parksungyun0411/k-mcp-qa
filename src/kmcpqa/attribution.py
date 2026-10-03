"""관찰이 서버 코드에서 나왔는지, 서버가 쓰는 MCP SDK 의 기본 동작인지 소스에서 찾아 가린다.

방법
1. 응답 문구(또는 오류 메시지)에서 시험 입력 값과 숫자를 걷어 낸 리터럴 조각을 만든다.
2. 고정 커밋으로 받은 서버 소스(의존성 디렉터리 제외)에서 먼저 찾고, 없으면 설치된 SDK 소스에서 찾는다.
3. 프로세스 종료는 stderr 의 스택 프레임 경로로 가린다
   (site-packages/mcp, node_modules/@modelcontextprotocol → SDK).

결과: origin = server | sdk | unknown, where = ["상대경로:줄", ...]. 찾지 못하면 unknown 으로 둔다.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path

SOURCE_SUFFIXES = {".ts", ".js", ".mjs", ".py"}
SERVER_EXCLUDE = {"node_modules", ".venv", "dist", "build", ".git", "tests", "test", "e2e", "__pycache__"}
SDK_GLOBS = [  # fastmcp(독립 패키지)를 쓰는 서버는 그쪽 경로가 실제 실행 경로라 먼저 본다
    "node_modules/@modelcontextprotocol/sdk/dist/esm",
    ".venv/lib/python*/site-packages/fastmcp",
    ".venv/lib/python*/site-packages/mcp",
]
_COMMENT = re.compile(r"^\s*(//|#|\*|/\*)")
PLACEHOLDER = re.compile(r"\$\{[^}]+\}|\{[^}]+\}|%s|%r")
_PY_FRAME = re.compile(r'File "([^"]+)", line (\d+)')
_JS_FRAME = re.compile(r"(?:file://)?(/[^\s():]+\.(?:js|mjs|ts)):(\d+):\d+")


def _walk(root: Path, exclude: set[str], suffixes: set[str] = SOURCE_SUFFIXES) -> Iterable[Path]:
    if not root.exists():
        return
    stack = [root]
    while stack:
        d = stack.pop()
        for p in d.iterdir():
            if p.is_dir():
                if p.name not in exclude:
                    stack.append(p)
            elif p.suffix in suffixes:
                yield p


def sdk_roots(server_root: Path) -> list[Path]:
    roots = []
    for g in SDK_GLOBS:
        roots += [p for p in server_root.glob(g) if p.is_dir()]
    return roots


def _search(files: Iterable[Path], pattern: re.Pattern, base: Path, limit: int = 3) -> list[str]:
    hits = []
    for f in files:
        try:
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if pattern.search(line) and not _COMMENT.match(line):
                hits.append(f"{f.relative_to(base)}:{i}")
                if len(hits) >= limit:
                    return hits
    return hits


def template_pattern(text: str, dynamic: list[str]) -> re.Pattern | None:
    """응답 문구를 소스 템플릿 정규식으로 바꾼다. 동적 값 자리는 ${x} / {x} / 아무 값으로 둔다."""
    text = re.sub(r"^MCP error -?\d+: ", "", text.strip().splitlines()[0] if text.strip() else "")
    if not text:
        return None
    parts = [re.escape(text)]
    for value in sorted({v for v in dynamic if v}, key=len, reverse=True):
        ev = re.escape(value)
        parts = [p.replace(ev, "\x00") for p in parts]
    body = parts[0]
    body = re.sub(r"\d+", r"\\d+", body)
    hole = r"(?:\$\{[^}]+\}|\{[^}]+\}|%s|%r|\w+)"
    body = body.replace("\x00", hole)
    # 템플릿의 리터럴이 너무 짧으면 찾지 않는다(우연 일치 방지)
    if len(re.sub(r"\(\?:.*?\)|\\.", "", body)) < 8:
        return None
    return re.compile(body)


def literal_fragments(text: str, dynamic: list[str]) -> list[str]:
    """JSON 응답이면 error/message 값, 아니면 첫 줄에서 동적 값을 뺀 긴 리터럴 조각들."""
    candidates = []
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            for k in ("error", "message", "errorMessage", "detail"):
                if isinstance(obj.get(k), str):
                    candidates.append(obj[k])
                elif isinstance(obj.get(k), dict):
                    candidates += [v for v in obj[k].values() if isinstance(v, str)]
    except ValueError:
        candidates.append(text.strip().splitlines()[0] if text.strip() else "")
    frags: list[str] = []
    for c in candidates:
        for v in dynamic:
            if v:
                c = c.replace(v, "\x00")
        for chunk in re.split(r"[\x00\d<>\"'`()\[\]{}]+", c):
            words = chunk.split()
            for n in (4, 3, 2, 1):
                for i in range(len(words) - n + 1):
                    w = " ".join(words[i:i + n]).strip(" :,.-")
                    dense = len(w.replace(" ", ""))
                    if dense >= 10 or (dense >= 6 and re.search(r"[^\x00-\x7f]", w)):
                        frags.append(w)
    seen, out = set(), []
    def rank(f: str) -> tuple:
        return (bool(re.search(r"[^\x00-\x7f]", f)), len(f.split()), len(f))

    for f in sorted(frags, key=rank, reverse=True):
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out[:15]


def from_text(text: str, dynamic: list[str], server_root: Path) -> dict:
    server_files = list(_walk(server_root, SERVER_EXCLUDE))
    pats = []
    tp = template_pattern(text, dynamic)
    if tp:
        pats.append(tp)
    pats += [re.compile(r"\s+".join(map(re.escape, f.split()))) for f in literal_fragments(text, dynamic)]
    for pat in pats:
        hits = _search(server_files, pat, server_root)
        if hits:
            return {"origin": "server", "where": hits, "pattern": pat.pattern}
        for root in sdk_roots(server_root):
            hits = _search(_walk(root, {"__pycache__"}), pat, server_root)
            if hits:
                return {"origin": "sdk", "where": hits, "pattern": pat.pattern}
    return {"origin": "unknown", "where": [], "pattern": pats[0].pattern if pats else None}


def _norm(path: str) -> str:
    return path[len("/private"):] if path.startswith("/private/") else path


def from_stderr(lines: list[str], server_root: Path) -> dict:
    """스택 프레임 중 안쪽(나중에 찍힌) 프레임부터 보며 SDK·서버 소스 위치를 모은다."""
    frames = []
    for line in lines:
        for path, ln in _PY_FRAME.findall(line) + _JS_FRAME.findall(line):
            frames.append((_norm(path), int(ln)))
    if not frames:
        return {"origin": "unknown", "where": [], "frames": 0}
    root = _norm(str(server_root.resolve()))
    sdk_markers = ("site-packages/mcp/", "site-packages/fastmcp/", "node_modules/@modelcontextprotocol/")
    where, origin = [], "unknown"
    for path, ln in reversed(frames):
        rel = path[len(root) + 1:] if path.startswith(root + "/") else path
        if any(m in path for m in sdk_markers):
            kind = "sdk"
        elif path.startswith(root + "/") and "site-packages" not in path and "node_modules" not in path:
            kind = "server"
        else:
            continue
        if origin == "unknown":
            origin = kind
        if f"{rel}:{ln}" not in where:
            where.append(f"{rel}:{ln}")
        if len(where) >= 3:
            break
    return {"origin": origin, "where": where, "frames": len(frames)}


def find(server_root: Path, regex: str, scope: str = "server", limit: int = 2,
         suffixes: set[str] = SOURCE_SUFFIXES) -> list[str]:
    """정해 둔 정규식으로 서버 소스 또는 SDK 소스에서 위치를 찾는다."""
    pat = re.compile(regex)
    if scope == "server":
        return _search(_walk(server_root, SERVER_EXCLUDE, suffixes), pat, server_root, limit)
    hits: list[str] = []
    for root in sdk_roots(server_root):
        hits += _search(_walk(root, {"__pycache__"}), pat, server_root, limit)
    return hits[:limit]


def dynamic_values(args: object, extra: Iterable[str] = ()) -> list[str]:
    vals = [str(x) for x in extra]
    if isinstance(args, dict):
        for v in args.values():
            if isinstance(v, (str, int, float)) and not isinstance(v, bool):
                vals.append(str(v))
    return vals
