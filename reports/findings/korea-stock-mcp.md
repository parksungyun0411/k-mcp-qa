# korea-stock-mcp

- 저장소: https://github.com/jjlabsio/korea-stock-mcp @ `210595eec73a39cd04e2fb175f6e69b1516f0dd4`
- 실행 시각: 2026-10-03T10:56:07+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc
- 실행 명령: `node dist/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.29.0
- 툴 수: 8, 원본 로그: `reports/raw/korea-stock-mcp/`

## 서버 코드

### R3 · 스키마를 만족하는 입력을 스키마에 없는 인자 조건으로 거부함 — 발생 1건

- 툴: get_corp_code
- 소스 위치: `src/dart/get-corp-code.ts:69`
- 예시 입력: `{}`
- 응답: 'corp_name 또는 stock_code 중 하나를 입력해주세요.'
- 재현: `python -m kmcpqa.repro korea-stock-mcp tools/call '{"name": "get_corp_code", "arguments": {}}'`

## SDK 기본 동작(확인)

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:104`
- 예시 입력: `{}`
- 응답: 'tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found'
- 재현: `python -m kmcpqa.repro korea-stock-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

