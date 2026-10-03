# data4library-mcp

- 저장소: https://github.com/isnow890/data4library-mcp @ `5708f84552076359847ae9ba4b912383c6cf6183`
- 실행 시각: 2026-10-03T07:14:06+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc && node scripts/copy-data.mjs
- 실행 명령: `node dist/src/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.30.0
- 원본 로그: `reports/raw/data4library-mcp/`

## P4 · 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함 (1건)

> 같은 SDK(@modelcontextprotocol/sdk 1.30.0)를 쓰는 korean-law-mcp 에서도 같은 유형이 관찰됨

- 툴 `kmcpqa_no_such_tool` · 입력 `{}`
  - 응답: 'outcome=tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`

## E1 · 기관 API·실행 오류를 isError 없는 결과로 돌려줌 (자리 표시자 키 호출) (13건)

- 툴 `search_libraries` · 입력 `{}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "search_libraries", "arguments": {}}'`
- 툴 `search_books` · 입력 `{}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "search_books", "arguments": {}}'`
- 툴 `search_popular_books` · 입력 `{}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "search_popular_books", "arguments": {}}'`
- 툴 `get_book_detail` · 입력 `{"isbn13": "9788936434267"}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "get_book_detail", "arguments": {"isbn13": "9788936434267"}}'`
- 툴 `search_libraries_by_book` · 입력 `{"isbn": "9788936434267", "region": "11"}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "search_libraries_by_book", "arguments": {"isbn": "9788936434267", "region": "11"}}'`
- 툴 `get_reading_quantity` · 입력 `{}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "get_reading_quantity", "arguments": {}}'`
- 툴 `get_monthly_keywords` · 입력 `{}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "get_monthly_keywords", "arguments": {}}'`
- 툴 `get_mania_recommendations` · 입력 `{"isbn13": "9788936434267"}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "get_mania_recommendations", "arguments": {"isbn13": "9788936434267"}}'`
- 툴 `get_reader_recommendations` · 입력 `{"isbn13": "9788936434267"}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "get_reader_recommendations", "arguments": {"isbn13": "9788936434267"}}'`
- 툴 `get_book_keywords` · 입력 `{"isbn13": "9788936434267"}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "get_book_keywords", "arguments": {"isbn13": "9788936434267"}}'`
- 툴 `get_book_usage_analysis` · 입력 `{"isbn13": "9788936434267"}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "get_book_usage_analysis", "arguments": {"isbn13": "9788936434267"}}'`
- 툴 `search_popular_books_by_library` · 입력 `{}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "search_popular_books_by_library", "arguments": {}}'`
- 툴 `get_library_info` · 입력 `{}`
  - 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
  - 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "get_library_info", "arguments": {}}'`
