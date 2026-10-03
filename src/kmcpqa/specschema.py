"""MCP 공식 스키마(2025-11-25)로 메시지를 검증하고, 툴의 JSON Schema 자체가 유효한지 본다.

spec/schema-2025-11-25.json 은 modelcontextprotocol/modelcontextprotocol 저장소
커밋 75db1e987cbbba6d170315dc99d0dfc440754aef 의 schema/2025-11-25/schema.json 을 그대로 복사한 것이다.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

from jsonschema import Draft202012Validator, validators
from jsonschema.exceptions import SchemaError

SPEC_PATH = Path(__file__).parent / "spec" / "schema-2025-11-25.json"
SPEC_SOURCE = ("modelcontextprotocol/modelcontextprotocol@75db1e987cbbba6d170315dc99d0dfc440754aef"
               ":schema/2025-11-25/schema.json")


@cache
def _spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


@cache
def _validator(definition: str) -> Draft202012Validator:
    spec = _spec()
    return Draft202012Validator({"$ref": f"#/$defs/{definition}", "$defs": spec["$defs"]})


def spec_errors(definition: str, instance: object, limit: int = 5) -> list[str]:
    """instance 가 스펙 정의를 어기면 오류 문장 목록(최대 limit 개)."""
    errors = sorted(_validator(definition).iter_errors(instance), key=lambda e: list(e.path))
    out = []
    for e in errors[:limit]:
        where = "/".join(str(p) for p in e.absolute_path) or "(root)"
        out.append(f"{where}: {e.message[:200]}")
    return out


def schema_dialect(schema: dict) -> str:
    return str(schema.get("$schema") or "default(2020-12)")


def check_json_schema(schema: object) -> list[str]:
    """툴의 inputSchema/outputSchema 가 자기 방언의 메타스키마로 유효한지와 구조 일관성."""
    if not isinstance(schema, dict):
        return ["schema is not an object"]
    problems = []
    cls = validators.validator_for(schema, default=Draft202012Validator)
    try:
        cls.check_schema(schema)
    except SchemaError as e:
        problems.append(f"metaschema: {e.message[:200]}")
    props = schema.get("properties") or {}
    required = schema.get("required") or []
    if isinstance(required, list) and isinstance(props, dict):
        missing = [r for r in required if r not in props]
        if missing:
            problems.append(f"required not in properties: {missing}")
    return problems


def instance_errors(schema: dict, instance: object, limit: int = 5) -> list[str]:
    cls = validators.validator_for(schema, default=Draft202012Validator)
    try:
        v = cls(schema)
        errs = list(v.iter_errors(instance))
    except Exception as e:  # 스키마 자체가 깨진 경우
        return [f"schema unusable: {e}"]
    return [f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message[:200]}" for e in errs[:limit]]
