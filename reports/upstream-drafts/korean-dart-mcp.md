<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] korean-dart-mcp: 공통 시험에서 관찰한 동작

한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.

## 환경

- 커밋: `4b2e072491f193833efb01c7fc76af1699ec176f`
- 실행 명령: `node build/index.js`
- MCP SDK: @modelcontextprotocol/sdk 1.29.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 자리 표시자 키로 시작한 뒤 요청 없이 5초 안에 프로세스가 종료됨 (발생 1건)

- 예시: 툴 `-`, 입력 `-`
- 응답: `exit 1: triggerUncaughtException(err, true /* fromPromise */); | Error: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>`
- 소스 위치: `build/lib/corp-code.js:55`, `build/lib/dart-client.js:49`

### 기관 API 실패를 JSON-RPC 내부 오류(-32603)로 응답 (발생 44건)

- 예시: 툴 `resolve_corp_code`, 입력 `{}`
- 응답: `missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>`
- 소스 위치: `src/lib/dart-client.ts:67`, `src/server/mcp-server.ts:45`, `node_modules/@modelcontextprotocol/sdk/dist/esm/shared/protocol.js:398` — 서버의 low-level CallTool 핸들러가 던진 예외를 SDK 프로토콜 계층이 -32603 으로 바꿈
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.
