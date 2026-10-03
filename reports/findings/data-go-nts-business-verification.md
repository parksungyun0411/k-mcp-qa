# data-go-nts-business-verification

- 저장소: https://github.com/Koomook/data-go-mcp-servers @ `dd27f99490400b31fa14f96045a138fa217580a4`
- 실행 시각: 2026-10-03T07:12:40+00:00 (UTC), 샌드박스: True
- 설치: uv venv -q -p 3.12 .venv && uv pip install -q -p .venv -e .
- 실행 명령: `.venv/bin/python -m data_go_mcp.nts_business_verification.server`, MCP SDK: mcp 2.3.0
- 원본 로그: `reports/raw/data-go-nts-business-verification/`

## I2 · 자리 표시자 키를 넣어도 initialize 응답이 오지 않음 (1건)

- 툴 `-` · 입력 `-`
  - 응답: "initialize closed, stderr 마지막 줄:     raise ModuleNotFoundError(_MESSAGE, name=__name__) | ModuleNotFoundError: No module named 'mcp.server.fastmcp'. This is mcp 2.x, where FastMCP was renamed to MCPServer (from mcp.server.mcpserver import MCPServer) and other APIs changed; see the migration guide at"
  - 재현: `python -m kmcpqa.runner --only data-go-nts-business-verification`
