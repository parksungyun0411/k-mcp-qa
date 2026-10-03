<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] data-go-nts-business-verification-mcp1: MCP 공통 시험에서 관찰한 동작

안녕하세요. 한국 공공데이터 MCP 서버들에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다.

## 환경

- 커밋: `dd27f99490400b31fa14f96045a138fa217580a4`
- 실행 명령: `.venv/bin/python -m data_go_mcp.nts_business_verification.server`
- MCP SDK: mcp 1.30.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 알 수 없는 메서드에 -32601 오류로 답하지 않음

- 툴 `-`, 입력 `-` (같은 유형 1건)
- 응답: `method=kmcpqa/unknown_method outcome=error code=-32602`

### 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함

- 툴 `kmcpqa_no_such_tool`, 입력 `{}` (같은 유형 1건)
- 응답: `outcome=tool_error: Unknown tool: kmcpqa_no_such_tool`

### 기관 API·실행 오류를 isError 없는 결과로 돌려줌 (자리 표시자 키 호출)

- 툴 `validate_business`, 입력 `{"business_number": "1248100998", "start_date": "20250101", "representative_name": "서울"}` (같은 유형 3건)
- 응답: `marker='401': {
  "error": "HTTP error occurred: 401",
  "business_number": "1248100998"
}`

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다. MCP 2025-11-25 스펙의 해당 항목과 다르게 보이는 부분만 적었습니다. 의도된 동작이라면 알려 주세요.
