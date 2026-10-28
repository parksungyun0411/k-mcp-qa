<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] korean-law-mcp: 공통 시험에서 관찰한 동작

한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.

## 환경

- 커밋: `ff33a713970d7b504bb08cd1fc3b03944aca5757`
- 설치: `npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc`
- 실행 명령: `node build/index.js`
- 키 변수: `LAW_OC` (실제 키가 아닌 값)
- MCP SDK: @modelcontextprotocol/sdk 1.30.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 (발생 1건)

- 예시: 툴 `kmcpqa_no_such_tool`, 입력 `{}`
- 응답: `tool_error: Unknown tool: kmcpqa_no_such_tool`
- 소스 위치: `src/tool-registry.ts:884`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 스키마를 만족하는 입력을 스키마에 없는 인자 조건으로 거부함 (발생 1건)

- 예시: 툴 `get_law_text`, 입력 `{}`
- 응답: `[INVALID_PARAMETER] : mst 또는 lawId 중 하나는 필수입니다
도구: get_law_text
제안:
  1. 파라미터 형식과 필수 값을 확인하세요.`
- 소스 위치: `src/tools/law-text.ts:28`, `src/tools/batch-articles.ts:43`, `src/tools/article-link-parser.ts:18`

### 스키마를 만족하는 입력을 스키마에 없는 인자 조건으로 거부함 (발생 1건)

- 예시: 툴 `ordinance_radar`, 입력 `{}`
- 응답: `[INVALID_PARAMETER] : ordinSeq(또는 별칭 id)·ordinanceName·query 중 하나는 필수입니다
도구: ordinance_radar
제안:
  1. 파라미터 형식과 필수 값을 확인하세요.`
- 소스 위치: `src/tools/ordinance-radar.ts:30`

## 재현

1. 위 커밋을 받아 설치 명령을 실행합니다.
2. 키 변수에 실제 키가 아닌 값을 넣고 실행 명령으로 서버를 stdio 로 띄웁니다.
3. `initialize` 를 보낸 뒤 관찰마다 적은 툴과 입력으로 `tools/call` 을 보냅니다. 툴이 `-` 인 관찰은 툴 호출 전, 서버 시작이나 initialize 단계에서 나타납니다.

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.
