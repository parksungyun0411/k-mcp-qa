"""inputSchema 로부터 시험 입력을 만든다.

- valid: 필수 필드만, 스키마를 만족하는 값. 기관 API 를 실제로 부르게 되는 입력이다.
- missing_required: 빈 객체 {}. 필수 필드가 있는 툴에만 쓴다.
- wrong_type: 모든 속성에 선언과 다른 JSON 타입의 값을 넣는다.
"""

from __future__ import annotations

from typing import Any

from kmcpqa.specschema import instance_errors

# 속성 이름에 따라 고르는 문자열 값. 실제 조회가 될 법한 값이지만 결과가 맞는지는 보지 않는다.
NAME_HINTS: list[tuple[tuple[str, ...], str]] = [
    (("corp_code", "corpcode"), "00126380"),
    (("stock_code", "ticker", "symbol"), "005930"),
    (("b_no", "bno", "business_number", "bizno", "brno"), "1248100998"),
    (("rcept_no",), "20240312000736"),
    (("bgn_de", "start_date", "from", "begin", "start"), "20250101"),
    (("end_de", "end_date", "to", "end"), "20250131"),
    (("year", "bsns_year"), "2024"),
    (("date", "ymd", "base_date"), "20250101"),
    (("isbn",), "9788936434267"),
    (("lawd_cd", "region_code", "sigungu"), "11110"),
    (("deal_ymd", "yyyymm", "month"), "202501"),
    (("lang", "language"), "ko"),
    (("query", "keyword", "search", "name", "corp_name", "q", "term", "title"), "서울"),
]


def _string_for(name: str, schema: dict) -> str:
    fmt = schema.get("format")
    if fmt == "date":
        return "2025-01-01"
    if fmt == "date-time":
        return "2025-01-01T00:00:00Z"
    lname = name.lower()
    for keys, value in NAME_HINTS:
        if any(k == lname or k in lname for k in keys):
            return value
    return "test"


def _value(name: str, schema: dict) -> Any:
    if not isinstance(schema, dict):
        return "test"
    if "const" in schema:
        return schema["const"]
    if schema.get("enum"):
        return schema["enum"][0]
    if "default" in schema:
        return schema["default"]
    if schema.get("examples"):
        return schema["examples"][0]
    for key in ("anyOf", "oneOf"):
        if schema.get(key):
            options = [s for s in schema[key] if isinstance(s, dict) and s.get("type") != "null"]
            if options:
                return _value(name, options[0])
    t = schema.get("type")
    if isinstance(t, list):
        t = next((x for x in t if x != "null"), "string")
    if t == "integer":
        return int(schema.get("minimum", 1))
    if t == "number":
        return float(schema.get("minimum", 1))
    if t == "boolean":
        return True
    if t == "array":
        item = schema.get("items")
        n = int(schema.get("minItems", 0))
        return [_value(name, item) for _ in range(max(n, 1))] if isinstance(item, dict) else []
    if t == "object":
        return valid_args(schema) or {}
    return _string_for(name, schema)


def valid_args(schema: dict) -> dict | None:
    """필수 필드만 채운 입력. 스키마를 만족하지 못하면 None."""
    props = schema.get("properties") or {}
    args = {name: _value(name, props.get(name, {})) for name in schema.get("required") or []}
    return args if not instance_errors(schema, args) else None


_WRONG = {"string": 12345, "integer": "not-a-number", "number": "not-a-number",
          "boolean": "not-a-boolean", "array": "not-an-array", "object": "not-an-object"}


def wrong_type_args(schema: dict) -> dict | None:
    props = schema.get("properties") or {}
    out = {}
    for name, p in props.items():
        t = p.get("type") if isinstance(p, dict) else None
        if isinstance(t, list):
            t = next((x for x in t if x != "null"), None)
        if t in _WRONG:
            out[name] = _WRONG[t]
    return out or None


def has_required(schema: dict) -> bool:
    return bool(schema.get("required"))
