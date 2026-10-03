<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] data4library-mcp: 공통 시험에서 관찰한 동작

한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.

## 환경

- 커밋: `5708f84552076359847ae9ba4b912383c6cf6183`
- 실행 명령: `node dist/src/index.js`
- MCP SDK: @modelcontextprotocol/sdk 1.30.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 13건, 원인 1개)

- 예시: 툴 `search_libraries`, 입력 `{}`
- 응답: `marker='error': {
  "response": {
    "errCode": "authErr",
    "error": "인증정보가 일치하지 않습니다."
  }
}`
- 소스 위치: 소스 위치 미확인
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.
