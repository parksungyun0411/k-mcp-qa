# mcp-korea-tourism-api

- 저장소: https://github.com/harimkang/mcp-korea-tourism-api @ `c4d4585cb8e5c3085e3e7631467f7c6d096aa5c1`
- 실행 시각: 2026-10-03T07:12:56+00:00 (UTC), 샌드박스: True
- 설치: uv sync --frozen --no-dev
- 실행 명령: `.venv/bin/python -m mcp_tourism.server`, MCP SDK: mcp 1.9.4, fastmcp 2.9.0
- 원본 로그: `reports/raw/mcp-korea-tourism-api/`

## P3 · 알 수 없는 메서드에 -32601 오류로 답하지 않음 (1건)

- 툴 `-` · 입력 `-`
  - 응답: 'method=kmcpqa/unknown_method outcome=error code=-32602'
  - 재현: `python -m kmcpqa.repro mcp-korea-tourism-api kmcpqa/unknown_method '{}'`

## P4 · 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함 (1건)

- 툴 `kmcpqa_no_such_tool` · 입력 `{}`
  - 응답: 'outcome=tool_error: Unknown tool: kmcpqa_no_such_tool'
  - 재현: `python -m kmcpqa.repro mcp-korea-tourism-api tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
