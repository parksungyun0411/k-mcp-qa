# korea-stock-mcp

- 저장소: https://github.com/jjlabsio/korea-stock-mcp @ `210595eec73a39cd04e2fb175f6e69b1516f0dd4`
- 실행 시각: 2026-10-03T07:10:20+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc
- 실행 명령: `node dist/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.29.0
- 원본 로그: `reports/raw/korea-stock-mcp/`

## P4 · 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함 (1건)

> 같은 SDK(@modelcontextprotocol/sdk 1.29.0)를 쓰는 assembly-api-mcp 에서도 같은 유형이 관찰됨

- 툴 `kmcpqa_no_such_tool` · 입력 `{}`
  - 응답: 'outcome=tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found'
  - 재현: `python -m kmcpqa.repro korea-stock-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`

## R3 · 스키마를 만족하는 입력을 인자 누락·형식 문제로 거부함 (1건)

- 툴 `get_corp_code` · 입력 `{}`
  - 응답: 'corp_name 또는 stock_code 중 하나를 입력해주세요.'
  - 재현: `python -m kmcpqa.repro korea-stock-mcp tools/call '{"name": "get_corp_code", "arguments": {}}'`
