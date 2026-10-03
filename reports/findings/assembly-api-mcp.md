# assembly-api-mcp

- 저장소: https://github.com/hollobit/assembly-api-mcp @ `f74c6b452c59d87e2fa7265fd985b90e4057a8ef`
- 실행 시각: 2026-10-03T07:10:07+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc
- 실행 명령: `node dist/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.29.0
- 원본 로그: `reports/raw/assembly-api-mcp/`

## P4 · 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함 (1건)

> 같은 SDK(@modelcontextprotocol/sdk 1.29.0)를 쓰는 korea-stock-mcp 에서도 같은 유형이 관찰됨

- 툴 `kmcpqa_no_such_tool` · 입력 `{}`
  - 응답: 'outcome=tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found'
  - 재현: `python -m kmcpqa.repro assembly-api-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
