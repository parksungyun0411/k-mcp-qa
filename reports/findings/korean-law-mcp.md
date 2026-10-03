# korean-law-mcp

- 저장소: https://github.com/chrisryugj/korean-law-mcp @ `ff33a713970d7b504bb08cd1fc3b03944aca5757`
- 실행 시각: 2026-10-03T10:55:33+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc
- 실행 명령: `node build/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.30.0
- 툴 수: 10, 원본 로그: `reports/raw/korean-law-mcp/`

## 서버 코드

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `src/tool-registry.ts:884`
- 예시 입력: `{}`
- 응답: 'tool_error: Unknown tool: kmcpqa_no_such_tool'
- 재현: `python -m kmcpqa.repro korean-law-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### R3 · 스키마를 만족하는 입력을 스키마에 없는 인자 조건으로 거부함 — 발생 1건

- 툴: get_law_text
- 소스 위치: `src/tools/law-text.ts:28`, `src/tools/batch-articles.ts:43`, `src/tools/article-link-parser.ts:18`
- 예시 입력: `{}`
- 응답: '[INVALID_PARAMETER] : mst 또는 lawId 중 하나는 필수입니다\n도구: get_law_text\n제안:\n  1. 파라미터 형식과 필수 값을 확인하세요.'
- 재현: `python -m kmcpqa.repro korean-law-mcp tools/call '{"name": "get_law_text", "arguments": {}}'`

### R3 · 스키마를 만족하는 입력을 스키마에 없는 인자 조건으로 거부함 — 발생 1건

- 툴: ordinance_radar
- 소스 위치: `src/tools/ordinance-radar.ts:30`
- 예시 입력: `{}`
- 응답: '[INVALID_PARAMETER] : ordinSeq(또는 별칭 id)·ordinanceName·query 중 하나는 필수입니다\n도구: ordinance_radar\n제안:\n  1. 파라미터 형식과 필수 값을 확인하세요.'
- 재현: `python -m kmcpqa.repro korean-law-mcp tools/call '{"name": "ordinance_radar", "arguments": {}}'`

