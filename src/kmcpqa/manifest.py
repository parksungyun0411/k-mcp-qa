"""servers.toml 읽기."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ServerSpec:
    id: str
    repo: str
    sha: str
    license: str
    runtime: str
    upstream_api: str
    install: list[list[str]]
    command: list[str]
    key_env: list[str]
    subdir: str = ""
    variant_of: str = ""
    modification: str = ""
    agreement: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class Skipped:
    repo: str
    sha: str
    reason: str
    listed_as: str = ""


def load(path: Path) -> tuple[list[ServerSpec], list[Skipped]]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    servers = [ServerSpec(**s) for s in data.get("server", [])]
    skipped = [Skipped(**s) for s in data.get("skipped", [])]
    ids = [s.id for s in servers]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate server id in manifest")
    return servers, skipped
