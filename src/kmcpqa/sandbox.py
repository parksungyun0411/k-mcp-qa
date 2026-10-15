"""남의 서버를 격리해 설치·실행하기 위한 작업 공간.

- 서버마다 작업 디렉터리 하나: src(체크아웃), home(임시 HOME), tmp, logs
- 환경 변수는 비우고 PATH·HOME·TMPDIR·로캘·패키지 캐시 위치만 넣는다. 이 머신의 토큰·키는 넘기지 않는다.
- macOS 에서는 sandbox-exec 로 감싼다: 작업 디렉터리와 시스템 임시 폴더(/private/var/folders) 밖 쓰기 금지,
  실제 HOME 내용 읽기 금지(uv 가 설치한 Python 인터프리터 경로만 예외, 파일 메타데이터 조회는 허용).
  네트워크는 막지 않는다(패키지 설치와 기관 API 호출에 필요).
"""

from __future__ import annotations

import asyncio
import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from kmcpqa.manifest import ServerSpec

PLACEHOLDER = "KMCPQA_PLACEHOLDER_NOT_A_REAL_KEY"


def _which_dirs(*names: str) -> list[str]:
    dirs = []
    for n in names:
        p = shutil.which(n)
        if p and os.path.dirname(p) not in dirs:
            dirs.append(os.path.dirname(p))
    return dirs


def uv_python_dir() -> Path:
    return Path(os.environ.get("UV_PYTHON_INSTALL_DIR", Path.home() / ".local/share/uv/python"))


def sandbox_profile(workspace: Path, real_home: Path, python_dir: Path) -> str:
    ws = os.path.realpath(workspace)
    return f"""(version 1)
(allow default)
(deny file-read* (subpath "{os.path.realpath(real_home)}"))
(allow file-read-metadata)
(allow file-read* (subpath "{os.path.realpath(python_dir)}") (subpath "{ws}"))
(deny file-write*)
(allow file-write*
  (subpath "{ws}")
  (subpath "/private/var/folders")
  (literal "/dev/null") (literal "/dev/tty") (literal "/dev/dtracehelper")
  (regex #"^/dev/fd/"))
"""


@dataclass
class StepResult:
    argv: list[str]
    returncode: int | None
    seconds: float
    timed_out: bool


class Workspace:
    def __init__(self, root: Path, use_sandbox: bool | None = None):
        self.root = root
        self.use_sandbox = (sys.platform == "darwin" and shutil.which("sandbox-exec") is not None) \
            if use_sandbox is None else use_sandbox

    def dir(self, spec: ServerSpec) -> Path:
        return self.root / spec.id

    def src(self, spec: ServerSpec) -> Path:
        return self.dir(spec) / "src"

    def cwd(self, spec: ServerSpec) -> Path:
        return self.src(spec) / spec.subdir if spec.subdir else self.src(spec)

    def logs(self, spec: ServerSpec) -> Path:
        p = self.dir(spec) / "logs"
        p.mkdir(parents=True, exist_ok=True)
        return p

    def env(self, spec: ServerSpec, key_mode: str = "placeholder") -> dict[str, str]:
        d = self.dir(spec)
        home, tmp = d / "home", d / "tmp"
        home.mkdir(parents=True, exist_ok=True)
        tmp.mkdir(parents=True, exist_ok=True)
        path = _which_dirs("node", "npm", "uv", "git") + ["/usr/bin", "/bin", "/usr/sbin", "/sbin"]
        env = {
            "PATH": ":".join(path),
            "HOME": str(home),
            "TMPDIR": str(tmp),
            "LANG": "en_US.UTF-8",
            "LC_ALL": "en_US.UTF-8",
            "npm_config_cache": str(d / "cache" / "npm"),
            "npm_config_update_notifier": "false",
            "UV_CACHE_DIR": str(d / "cache" / "uv"),
            "UV_PYTHON_INSTALL_DIR": str(uv_python_dir()),
            "UV_PYTHON_DOWNLOADS": "never",
            "PYTHONUNBUFFERED": "1",
            "NO_COLOR": "1",
        }
        if key_mode == "placeholder":
            env.update({k: PLACEHOLDER for k in spec.key_env})
        return env

    def wrap(self, spec: ServerSpec, argv: list[str]) -> list[str]:
        if not self.use_sandbox:
            return argv
        profile = self.dir(spec) / "sandbox.sb"
        profile.write_text(sandbox_profile(self.root, Path.home(), uv_python_dir()), encoding="utf-8")
        return ["sandbox-exec", "-f", str(profile), *argv]

    async def fetch(self, spec: ServerSpec) -> str:
        """저장소를 받아 지정 커밋으로 맞춘다. git 은 샌드박스 밖에서 돈다(남의 코드를 실행하지 않음)."""
        src = self.src(spec)
        if not (src / ".git").exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            await _run(["git", "clone", "-q", f"https://github.com/{spec.repo}", str(src)], None,
                       None, self.logs(spec) / "fetch.log", 600)
        await _run(["git", "-C", str(src), "checkout", "-q", "--detach", spec.sha], None, None,
                   self.logs(spec) / "fetch.log", 120)
        proc = await asyncio.create_subprocess_exec("git", "-C", str(src), "rev-parse", "HEAD",
                                                    stdout=asyncio.subprocess.PIPE)
        out, _ = await proc.communicate()
        return out.decode().strip()

    async def install(self, spec: ServerSpec, timeout_s: float = 900) -> list[StepResult]:
        results = []
        env = self.env(spec, key_mode="none")
        for step in spec.install:
            r = await _run(self.wrap(spec, step), self.cwd(spec), env,
                           self.logs(spec) / "install.log", timeout_s, label=step)
            results.append(r)
            if r.returncode != 0:
                break
        return results


async def _run(argv: list[str], cwd: Path | None, env: dict | None, log: Path, timeout_s: float,
               label: list[str] | None = None) -> StepResult:
    log.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    with log.open("ab") as f:
        f.write(f"\n$ {' '.join(label or argv)}\n".encode())
        f.flush()
        proc = await asyncio.create_subprocess_exec(*argv, cwd=cwd, env=env, stdout=f, stderr=f,
                                                    stdin=asyncio.subprocess.DEVNULL)
        try:
            rc = await asyncio.wait_for(proc.wait(), timeout_s)
            timed_out = False
        except TimeoutError:
            proc.kill()
            await proc.wait()
            rc, timed_out = None, True
        f.write(f"[exit {rc}{' timeout' if timed_out else ''}]\n".encode())
    return StepResult(label or argv, rc, round(time.perf_counter() - started, 2), timed_out)
