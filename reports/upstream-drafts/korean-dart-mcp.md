<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] korean-dart-mcp: MCP 공통 시험에서 관찰한 동작

안녕하세요. 한국 공공데이터 MCP 서버들에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다.

## 환경

- 커밋: `96315645798697abec785bc7204c237e0f0f0618`
- 실행 명령: `node build/index.js`
- MCP SDK: @modelcontextprotocol/sdk 1.29.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 자리 표시자 키로 시작한 뒤 요청 없이 5초 안에 프로세스가 종료됨

- 툴 `-`, 입력 `-` (같은 유형 1건)
- 응답: `exit 1: Error: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result> |     at DartClient.g`

### 툴 실행 오류를 JSON-RPC 내부 오류(-32603)로 답함 (스펙은 isError 결과로 규정)

- 툴 `resolve_corp_code`, 입력 `{}` (같은 유형 44건)
- 응답: `missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>`

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다. MCP 2025-11-25 스펙의 해당 항목과 다르게 보이는 부분만 적었습니다. 의도된 동작이라면 알려 주세요.
