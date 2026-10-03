# korean-law-mcp

- 저장소: https://github.com/chrisryugj/korean-law-mcp @ `ff33a713970d7b504bb08cd1fc3b03944aca5757`
- 실행 시각: 2026-10-03T07:09:46+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc
- 실행 명령: `node build/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.30.0
- 원본 로그: `reports/raw/korean-law-mcp/`

## P4 · 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함 (1건)

> 같은 SDK(@modelcontextprotocol/sdk 1.30.0)를 쓰는 data4library-mcp 에서도 같은 유형이 관찰됨

- 툴 `kmcpqa_no_such_tool` · 입력 `{}`
  - 응답: 'outcome=tool_error: Unknown tool: kmcpqa_no_such_tool'
  - 재현: `python -m kmcpqa.repro korean-law-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`

## R3 · 스키마를 만족하는 입력을 인자 누락·형식 문제로 거부함 (2건)

- 툴 `get_law_text` · 입력 `{}`
  - 응답: '[INVALID_PARAMETER] : mst 또는 lawId 중 하나는 필수입니다\n도구: get_law_text\n제안:\n  1. 파라미터 형식과 필수 값을 확인하세요.'
  - 재현: `python -m kmcpqa.repro korean-law-mcp tools/call '{"name": "get_law_text", "arguments": {}}'`
- 툴 `ordinance_radar` · 입력 `{}`
  - 응답: '[INVALID_PARAMETER] : ordinSeq(또는 별칭 id)·ordinanceName·query 중 하나는 필수입니다\n도구: ordinance_radar\n제안:\n  1. 파라미터 형식과 필수 값을 확인하세요.'
  - 재현: `python -m kmcpqa.repro korean-law-mcp tools/call '{"name": "ordinance_radar", "arguments": {}}'`
