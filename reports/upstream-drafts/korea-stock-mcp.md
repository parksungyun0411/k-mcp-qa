<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] korea-stock-mcp: 공통 시험에서 관찰한 동작

한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.

## 환경

- 커밋: `210595eec73a39cd04e2fb175f6e69b1516f0dd4`
- 설치: `npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc`
- 실행 명령: `node dist/index.js`
- 키 변수: `DART_API_KEY`, `KRX_API_KEY` (실제 키가 아닌 값)
- MCP SDK: @modelcontextprotocol/sdk 1.29.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 스키마를 만족하는 입력을 스키마에 없는 인자 조건으로 거부함 (발생 1건)

- 예시: 툴 `get_corp_code`, 입력 `{}`
- 응답: `corp_name 또는 stock_code 중 하나를 입력해주세요.`
- 소스 위치: `src/dart/get-corp-code.ts:69`

## 재현

1. 위 커밋을 받아 설치 명령을 실행합니다.
2. 키 변수에 실제 키가 아닌 값을 넣고 실행 명령으로 서버를 stdio 로 띄웁니다.
3. `initialize` 를 보낸 뒤 관찰마다 적은 툴과 입력으로 `tools/call` 을 보냅니다. 툴이 `-` 인 관찰은 툴 호출 전, 서버 시작이나 initialize 단계에서 나타납니다.

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.
