# real-estate-mcp

- 저장소: https://github.com/tae0y/real-estate-mcp @ `1119eb1069d1b1bae15f7b38c6c0268fe07995c0`
- 실행 시각: 2026-10-03T10:59:14+00:00 (UTC), 샌드박스: True
- 설치: uv sync --frozen --no-dev
- 실행 명령: `.venv/bin/real-estate-mcp`, MCP SDK: mcp 1.26.0
- 툴 수: 16, 원본 로그: `reports/raw/real-estate-mcp/`

## 서버 코드

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 10건

- 툴: get_apartment_rent, get_apartment_trades, get_apt_subscription_info, get_commercial_trade, get_officetel_rent, get_officetel_trades, get_single_house_rent, get_single_house_trades 외
- 소스 위치: `src/real_estate/mcp_server/_helpers.py:66`, `src/real_estate/mcp_server/_helpers.py:69`, `src/real_estate/mcp_server/_helpers.py:73`
- 예시 입력: `{"region_code": "11110", "year_month": "2024"}`
- 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
- 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_apartment_rent", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: get_apt_subscription_results
- 소스 위치: `src/real_estate/mcp_server/tools/subscription.py:156`
- 예시 입력: `{"stat_kind": "test"}`
- 응답: 'marker=\'error\': {\n  "error": "validation_error",\n  "message": "Invalid stat_kind. Expected one of: reqst_area, reqst_age, przwner_area, przwner_age, cmpetrt_area, aps_przwner"\n}'
- 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_apt_subscription_results", "arguments": {"stat_kind": "test"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: get_region_code
- 소스 위치: 소스 위치 미확인
- 예시 입력: `{"query": "서울"}`
- 응답: 'marker=\'오류\': {\n  "region_code": "11000",\n  "full_name": "서울특별시",\n  "matches": [\n    {\n      "code": "1100000000",\n      "name": "서울특별시"\n    },\n    {\n      "code": "1111000000",\n      "name": "서울특별시 종로구"\n    },\n    {\n      "code": "1114000000",\n      "name": "서울특별시 중구"\n    },\n    {\n      "code": "1117000000",\n   '
- 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_region_code", "arguments": {"query": "서울"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

## SDK 기본 동작(확인)

### P3 · 알 수 없는 메서드에 -32601 이 아닌 응답(또는 무응답) — 발생 1건

- 툴: -
- 소스 위치: `.venv/lib/python3.12/site-packages/mcp/shared/session.py:390`
- 예시 입력: `{}`
- 응답: 'method=kmcpqa/unknown_method → error code=-32602 Invalid request parameters'
- 재현: `python -m kmcpqa.repro real-estate-mcp kmcpqa/unknown_method '{}'`
- 근거: [https://www.jsonrpc.org/specification#error_object](https://www.jsonrpc.org/specification#error_object) (JSON-RPC 2.0 오류 코드 표)

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/tool_manager.py:78`, `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/tool_manager.py:91`
- 예시 입력: `{}`
- 응답: 'tool_error: Unknown tool: kmcpqa_no_such_tool'
- 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

