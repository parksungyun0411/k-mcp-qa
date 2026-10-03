# data4library-mcp

- 저장소: https://github.com/isnow890/data4library-mcp @ `5708f84552076359847ae9ba4b912383c6cf6183`
- 실행 시각: 2026-10-03T10:59:33+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc && node scripts/copy-data.mjs
- 실행 명령: `node dist/src/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.30.0
- 툴 수: 27, 원본 로그: `reports/raw/data4library-mcp/`

## 서버 코드

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 13건

- 툴: get_book_detail, get_book_keywords, get_book_usage_analysis, get_library_info, get_mania_recommendations, get_monthly_keywords, get_reader_recommendations, get_reading_quantity 외
- 소스 위치: 소스 위치 미확인
- 예시 입력: `{}`
- 응답: 'marker=\'error\': {\n  "response": {\n    "errCode": "authErr",\n    "error": "인증정보가 일치하지 않습니다."\n  }\n}'
- 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "search_libraries", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

## SDK 기본 동작(확인)

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:104`
- 예시 입력: `{}`
- 응답: 'tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found'
- 재현: `python -m kmcpqa.repro data4library-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

