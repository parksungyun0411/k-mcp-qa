# assembly-api-mcp

- 저장소: https://github.com/hollobit/assembly-api-mcp @ `f74c6b452c59d87e2fa7265fd985b90e4057a8ef`
- 실행 시각: 2026-10-03T10:55:54+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc
- 실행 명령: `node dist/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.29.0
- 툴 수: 6, 원본 로그: `reports/raw/assembly-api-mcp/`

## SDK 기본 동작(확인)

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:104`
- 예시 입력: `{}`
- 응답: 'tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found'
- 재현: `uv run python -m kmcpqa.repro assembly-api-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

