# data-go-nts-business-verification-mcp1

- 저장소: https://github.com/Koomook/data-go-mcp-servers @ `dd27f99490400b31fa14f96045a138fa217580a4`
- 실행 시각: 2026-10-03T10:58:13+00:00 (UTC), 샌드박스: True
- 설치: uv venv -q -p 3.12 .venv && uv pip install -q -p .venv -e . 'mcp[cli]<2'
- 실행 명령: `.venv/bin/python -m data_go_mcp.nts_business_verification.server`, MCP SDK: mcp 1.30.0
- 툴 수: 3, 원본 로그: `reports/raw/data-go-nts-business-verification-mcp1/`

## 서버 코드

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: validate_business
- 소스 위치: `data_go_mcp/nts_business_verification/api_client.py:98`
- 예시 입력: `{"business_number": "1248100998", "start_date": "20250101", "representative_name": "서울"}`
- 응답: 'marker=\'401\': {\n  "error": "HTTP error occurred: 401",\n  "business_number": "1248100998"\n}'
- 재현: `uv run python -m kmcpqa.repro data-go-nts-business-verification-mcp1 tools/call '{"name": "validate_business", "arguments": {"business_number": "1248100998", "start_date": "20250101", "representative_name": "서울"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: check_business_status
- 소스 위치: `data_go_mcp/nts_business_verification/api_client.py:98`
- 예시 입력: `{"business_numbers": "1248100998"}`
- 응답: 'marker=\'401\': {\n  "error": "HTTP error occurred: 401",\n  "business_numbers": [\n    "1248100998"\n  ]\n}'
- 재현: `uv run python -m kmcpqa.repro data-go-nts-business-verification-mcp1 tools/call '{"name": "check_business_status", "arguments": {"business_numbers": "1248100998"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 1건

- 툴: batch_validate_businesses
- 소스 위치: `data_go_mcp/nts_business_verification/server.py:237`
- 예시 입력: `{"businesses_json": "test"}`
- 응답: 'valid(합성 입력): {\n  "error": "JSON 파싱 오류: Expecting value: line 1 column 1 (char 0)",\n  "hint": "올바른 JSON 형식으로 입력해주세요."\n}'
- 재현: `uv run python -m kmcpqa.repro data-go-nts-business-verification-mcp1 tools/call '{"name": "batch_validate_businesses", "arguments": {"businesses_json": "test"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

## SDK 기본 동작(확인)

### P3 · 알 수 없는 메서드에 -32601 이 아닌 응답(또는 무응답) — 발생 1건

- 툴: -
- 소스 위치: `.venv/lib/python3.12/site-packages/mcp/shared/session.py:390`
- 예시 입력: `{}`
- 응답: 'method=kmcpqa/unknown_method → error code=-32602 Invalid request parameters'
- 재현: `uv run python -m kmcpqa.repro data-go-nts-business-verification-mcp1 kmcpqa/unknown_method '{}'`
- 근거: [https://www.jsonrpc.org/specification#error_object](https://www.jsonrpc.org/specification#error_object) (JSON-RPC 2.0 오류 코드 표)

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/tool_manager.py:78`, `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/tool_manager.py:91`
- 예시 입력: `{}`
- 응답: 'tool_error: Unknown tool: kmcpqa_no_such_tool'
- 재현: `uv run python -m kmcpqa.repro data-go-nts-business-verification-mcp1 tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

