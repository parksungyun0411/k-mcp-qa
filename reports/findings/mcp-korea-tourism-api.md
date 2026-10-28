# mcp-korea-tourism-api

- 저장소: https://github.com/harimkang/mcp-korea-tourism-api @ `c4d4585cb8e5c3085e3e7631467f7c6d096aa5c1`
- 실행 시각: 2026-10-03T10:58:24+00:00 (UTC), 샌드박스: True
- 설치: uv sync --frozen --no-dev
- 실행 명령: `.venv/bin/python -m mcp_tourism.server`, MCP SDK: mcp 1.9.4, fastmcp 2.9.0
- 툴 수: 8, 원본 로그: `reports/raw/mcp-korea-tourism-api/`

## SDK 기본 동작(확인)

### P3 · 알 수 없는 메서드에 -32601 이 아닌 응답(또는 무응답) — 발생 1건

- 툴: -
- 소스 위치: `.venv/lib/python3.12/site-packages/mcp/shared/session.py:367`
- 예시 입력: `{}`
- 응답: 'method=kmcpqa/unknown_method → error code=-32602 Invalid request parameters'
- 재현: `uv run python -m kmcpqa.repro mcp-korea-tourism-api kmcpqa/unknown_method '{}'`
- 근거: [https://www.jsonrpc.org/specification#error_object](https://www.jsonrpc.org/specification#error_object) (JSON-RPC 2.0 오류 코드 표)

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `.venv/lib/python3.12/site-packages/fastmcp/server/server.py:348`, `.venv/lib/python3.12/site-packages/fastmcp/server/server.py:609`, `.venv/lib/python3.12/site-packages/fastmcp/server/server.py:611`
- 예시 입력: `{}`
- 응답: 'tool_error: Unknown tool: kmcpqa_no_such_tool'
- 재현: `uv run python -m kmcpqa.repro mcp-korea-tourism-api tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

