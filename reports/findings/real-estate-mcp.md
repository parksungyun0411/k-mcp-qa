# real-estate-mcp

- 저장소: https://github.com/tae0y/real-estate-mcp @ `1119eb1069d1b1bae15f7b38c6c0268fe07995c0`
- 실행 시각: 2026-10-03T07:13:46+00:00 (UTC), 샌드박스: True
- 설치: uv sync --frozen --no-dev
- 실행 명령: `.venv/bin/real-estate-mcp`, MCP SDK: mcp 1.26.0
- 원본 로그: `reports/raw/real-estate-mcp/`

## P3 · 알 수 없는 메서드에 -32601 오류로 답하지 않음 (1건)

- 툴 `-` · 입력 `-`
  - 응답: 'method=kmcpqa/unknown_method outcome=error code=-32602'
  - 재현: `python -m kmcpqa.repro real-estate-mcp kmcpqa/unknown_method '{}'`

## P4 · 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함 (1건)

- 툴 `kmcpqa_no_such_tool` · 입력 `{}`
  - 응답: 'outcome=tool_error: Unknown tool: kmcpqa_no_such_tool'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`

## E1 · 기관 API·실행 오류를 isError 없는 결과로 돌려줌 (자리 표시자 키 호출) (12건)

- 툴 `get_apartment_rent` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_apartment_rent", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_officetel_rent` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_officetel_rent", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_villa_rent` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_villa_rent", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_single_house_rent` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_single_house_rent", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_apt_subscription_info` · 입력 `{}`
  - 응답: 'marker=\'401\': {\n  "error": "network_error",\n  "message": "HTTP error: 401"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_apt_subscription_info", "arguments": {}}'`
- 툴 `get_apt_subscription_results` · 입력 `{"stat_kind": "test"}`
  - 응답: 'marker=\'error\': {\n  "error": "validation_error",\n  "message": "Invalid stat_kind. Expected one of: reqst_area, reqst_age, przwner_area, przwner_age, cmpetrt_area, aps_przwner"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_apt_subscription_results", "arguments": {"stat_kind": "test"}}'`
- 툴 `get_apartment_trades` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_apartment_trades", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_officetel_trades` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_officetel_trades", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_villa_trades` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_villa_trades", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_single_house_trades` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_single_house_trades", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_commercial_trade` · 입력 `{"region_code": "11110", "year_month": "2024"}`
  - 응답: 'marker=\'403\': {\n  "error": "network_error",\n  "message": "HTTP error: 403"\n}'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_commercial_trade", "arguments": {"region_code": "11110", "year_month": "2024"}}'`
- 툴 `get_region_code` · 입력 `{"query": "서울"}`
  - 응답: 'marker=\'오류\': {\n  "region_code": "11000",\n  "full_name": "서울특별시",\n  "matches": [\n    {\n      "code": "1100000000",\n      "name": "서울특별시"\n    },\n    {\n      "code": "1111000000",\n      "name": "서울특별시 종로구"\n    },\n    {\n      "code": "1114000000",\n      "name": "서울특별시 중구"\n    },\n    {\n      "code": "111'
  - 재현: `python -m kmcpqa.repro real-estate-mcp tools/call '{"name": "get_region_code", "arguments": {"query": "서울"}}'`
