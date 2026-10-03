# data-go-nts-business-verification-mcp1

- 저장소: https://github.com/Koomook/data-go-mcp-servers @ `dd27f99490400b31fa14f96045a138fa217580a4`
- 실행 시각: 2026-10-03T07:12:44+00:00 (UTC), 샌드박스: True
- 설치: uv venv -q -p 3.12 .venv && uv pip install -q -p .venv -e . mcp[cli]<2
- 실행 명령: `.venv/bin/python -m data_go_mcp.nts_business_verification.server`, MCP SDK: mcp 1.30.0
- 원본 로그: `reports/raw/data-go-nts-business-verification-mcp1/`

## P3 · 알 수 없는 메서드에 -32601 오류로 답하지 않음 (1건)

- 툴 `-` · 입력 `-`
  - 응답: 'method=kmcpqa/unknown_method outcome=error code=-32602'
  - 재현: `python -m kmcpqa.repro data-go-nts-business-verification-mcp1 kmcpqa/unknown_method '{}'`

## P4 · 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함 (1건)

- 툴 `kmcpqa_no_such_tool` · 입력 `{}`
  - 응답: 'outcome=tool_error: Unknown tool: kmcpqa_no_such_tool'
  - 재현: `python -m kmcpqa.repro data-go-nts-business-verification-mcp1 tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`

## E1 · 기관 API·실행 오류를 isError 없는 결과로 돌려줌 (자리 표시자 키 호출) (3건)

- 툴 `validate_business` · 입력 `{"business_number": "1248100998", "start_date": "20250101", "representative_name": "서울"}`
  - 응답: 'marker=\'401\': {\n  "error": "HTTP error occurred: 401",\n  "business_number": "1248100998"\n}'
  - 재현: `python -m kmcpqa.repro data-go-nts-business-verification-mcp1 tools/call '{"name": "validate_business", "arguments": {"business_number": "1248100998", "start_date": "20250101", "representative_name": "서울"}}'`
- 툴 `check_business_status` · 입력 `{"business_numbers": "1248100998"}`
  - 응답: 'marker=\'401\': {\n  "error": "HTTP error occurred: 401",\n  "business_numbers": [\n    "1248100998"\n  ]\n}'
  - 재현: `python -m kmcpqa.repro data-go-nts-business-verification-mcp1 tools/call '{"name": "check_business_status", "arguments": {"business_numbers": "1248100998"}}'`
- 툴 `batch_validate_businesses` · 입력 `{"businesses_json": "test"}`
  - 응답: 'marker=\'error\': {\n  "error": "JSON 파싱 오류: Expecting value: line 1 column 1 (char 0)",\n  "hint": "올바른 JSON 형식으로 입력해주세요."\n}'
  - 재현: `python -m kmcpqa.repro data-go-nts-business-verification-mcp1 tools/call '{"name": "batch_validate_businesses", "arguments": {"businesses_json": "test"}}'`
