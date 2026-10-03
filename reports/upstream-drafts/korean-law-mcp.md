<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] korean-law-mcp: MCP 공통 시험에서 관찰한 동작

안녕하세요. 한국 공공데이터 MCP 서버들에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다.

## 환경

- 커밋: `ff33a713970d7b504bb08cd1fc3b03944aca5757`
- 실행 명령: `node build/index.js`
- MCP SDK: @modelcontextprotocol/sdk 1.30.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함

- 툴 `kmcpqa_no_such_tool`, 입력 `{}` (같은 유형 1건)
- 응답: `outcome=tool_error: Unknown tool: kmcpqa_no_such_tool`
- 참고: 같은 SDK(@modelcontextprotocol/sdk 1.30.0)를 쓰는 data4library-mcp 에서도 같은 유형이 관찰됨. 서버 코드가 아니라 SDK 동작일 수 있습니다.

### 스키마를 만족하는 입력을 인자 누락·형식 문제로 거부함

- 툴 `get_law_text`, 입력 `{}` (같은 유형 2건)
- 응답: `[INVALID_PARAMETER] : mst 또는 lawId 중 하나는 필수입니다
도구: get_law_text
제안:
  1. 파라미터 형식과 필수 값을 확인하세요.`

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다. MCP 2025-11-25 스펙의 해당 항목과 다르게 보이는 부분만 적었습니다. 의도된 동작이라면 알려 주세요.
