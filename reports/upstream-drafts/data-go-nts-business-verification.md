<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] data-go-nts-business-verification: 공통 시험에서 관찰한 동작

한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.

## 환경

- 커밋: `dd27f99490400b31fa14f96045a138fa217580a4`
- 실행 명령: `.venv/bin/python -m data_go_mcp.nts_business_verification.server`
- MCP SDK: mcp 2.3.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 자리 표시자 키를 넣어도 initialize 응답이 오지 않음 (발생 1건, 원인 1개)

- 예시: 툴 `-`, 입력 `-`
- 응답: `initialize closed, stderr 마지막 줄:     raise ModuleNotFoundError(_MESSAGE, name=__name__) | ModuleNotFoundError: No module named 'mcp.server.fastmcp'. This is mcp 2.x, where FastMCP was renamed to MCPServer (from mcp.server.mcpserver import M`
- 소스 위치: `pyproject.toml:24`, `.venv/lib/python3.12/site-packages/mcp/server/fastmcp.py:16`, `data_go_mcp/nts_business_verification/server.py:6` — 의존성 선언과 설치된 SDK 의 조합

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.
