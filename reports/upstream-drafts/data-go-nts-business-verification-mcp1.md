<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] data-go-nts-business-verification-mcp1: 공통 시험에서 관찰한 동작

한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.

## 환경

- 커밋: `dd27f99490400b31fa14f96045a138fa217580a4`
- 설치: `uv venv -q -p 3.12 .venv && uv pip install -q -p .venv -e . mcp[cli]<2` (`src/nts-business-verification` 에서 실행)
- 실행 명령: `.venv/bin/python -m data_go_mcp.nts_business_verification.server`
- 키 변수: `API_KEY` (실제 키가 아닌 값)
- MCP SDK: mcp 1.30.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03
- 이 프로젝트의 수정: mcp<2 고정. 원 저장소의 설치 절차가 아니라 위 설치 명령으로 설치한 결과입니다.

## 관찰

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `validate_business`, 입력 `{"business_number": "1248100998", "start_date": "20250101", "representative_name": "서울"}`
- 응답: `marker='401': {
  "error": "HTTP error occurred: 401",
  "business_number": "1248100998"
}`
- 소스 위치: `data_go_mcp/nts_business_verification/api_client.py:98`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `check_business_status`, 입력 `{"business_numbers": "1248100998"}`
- 응답: `marker='401': {
  "error": "HTTP error occurred: 401",
  "business_numbers": [
    "1248100998"
  ]
}`
- 소스 위치: `data_go_mcp/nts_business_verification/api_client.py:98`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 1건)

- 예시: 툴 `batch_validate_businesses`, 입력 `{"businesses_json": "test"}`
- 응답: `valid(합성 입력): {
  "error": "JSON 파싱 오류: Expecting value: line 1 column 1 (char 0)",
  "hint": "올바른 JSON 형식으로 입력해주세요."
}`
- 소스 위치: `data_go_mcp/nts_business_verification/server.py:237`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

## 재현

1. 위 커밋을 받아 설치 명령을 실행합니다.
2. 키 변수에 실제 키가 아닌 값을 넣고 실행 명령으로 서버를 stdio 로 띄웁니다.
3. `initialize` 를 보낸 뒤 관찰마다 적은 툴과 입력으로 `tools/call` 을 보냅니다. 툴이 `-` 인 관찰은 툴 호출 전, 서버 시작이나 initialize 단계에서 나타납니다.

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.
