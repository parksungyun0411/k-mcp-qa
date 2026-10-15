<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] korea-stats-mcp: 공통 시험에서 관찰한 동작

한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.

## 환경

- 커밋: `cf8af3dc52eee8f3085f947adc43bb7f65c8ea9b`
- 실행 명령: `node dist/index.js`
- MCP SDK: @modelcontextprotocol/sdk 1.32.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### inputSchema 의 properties 가 비어 있는데 런타임은 특정 인자를 요구함 (발생 1건)

- 예시: 툴 `get_indicator`, 입력 `{}`
- 응답: `properties=[] → MCP error -32602: Input validation error: Invalid arguments for tool get_indicator: Required at indicatorId
Required at kind`
- 소스 위치: `src/tools/indicators.ts:121`, `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:222` — tools/list 의 inputSchema 는 properties 가 비어 있고, 검증은 서버가 등록한 스키마로 SDK 가 수행함. 스키마를 JSON Schema 로 바꾸는 과정에서 생겼을 수 있음(확인하지 않음)

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `search_statistics`, 입력 `{"query": "서울"}`
- 응답: `marker='"success": false': {
  "totalCount": 0,
  "results": [],
  "queryAnalysis": {
    "topics": [],
    "regions": [
      "11"
    ],
    "intent": "search"
  },
  "success": false,
  "error": "알 수 없는 오류가 발생했습니다.",
  "code": "11"
}`
- 소스 위치: `src/utils/errorHandler.ts:41`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `get_statistics_data`, 입력 `{"orgId": "test", "tableId": "test", "objL1": "test", "periodType": "Y"}`
- 응답: `marker='"success": false': {
  "providerTotalCount": null,
  "providerSnapshot": "unproven",
  "snapshotScope": "active_partition",
  "completionScope": "requested_period_traversal",
  "success": false,
  "data": [],
  "validationLevel": "u`
- 소스 위치: 소스 위치 미확인
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `compare_statistics`, 입력 `{"orgId": "test", "tableId": "test", "compareType": "period", "periodType": "Y"}`
- 응답: `marker='"success": false': {
  "success": false,
  "compareType": "period",
  "validationLevel": "unverified",
  "errorCode": "11",
  "provenance": {
    "provider": "kosis",
    "orgId": "test",
    "tableId": "test",
    "sourceUrl": "htt`
- 소스 위치: 소스 위치 미확인
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `analyze_time_series`, 입력 `{"orgId": "test", "tableId": "test", "objL1": "test", "periodType": "Y"}`
- 응답: `marker='"success": false': {
  "success": false,
  "validationLevel": "unverified",
  "errorCode": "11",
  "provenance": {
    "provider": "kosis",
    "orgId": "test",
    "tableId": "test",
    "sourceUrl": "https://kosis.kr/openapi/Param`
- 소스 위치: 소스 위치 미확인
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `get_table_info`, 입력 `{"orgId": "test", "tableId": "test"}`
- 응답: `marker='"success": false': {
  "success": false,
  "orgId": "test",
  "tableId": "test",
  "infoType": "ITM",
  "errorCode": "11",
  "errorMessage": "알 수 없는 오류가 발생했습니다.",
  "usageHint": "알 수 없는 오류가 발생했습니다."
}`
- 소스 위치: `src/utils/errorHandler.ts:41`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `quick_stats`, 입력 `{"query": "서울"}`
- 응답: `marker='"success": false': {
  "success": false,
  "answer": "\"서울\"에 대한 빠른 조회가 지원되지 않습니다.",
  "note": "📊 지원 키워드 (카테고리별 대표 예시):\n• 인구/출산: 인구, 출산율, 출생아수, 사망률, 기대수명\n• 고령화: 고령인구, 노인인구, 노령화지수, 65세이상인구\n• 고용/노동: 실업률, 고용률, 취업자수, 임금\n• 경제: GDP, G`
- 소스 위치: 소스 위치 미확인
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 1건)

- 예시: 툴 `quick_trend`, 입력 `{"keyword": "서울"}`
- 응답: `marker='"success": false': {
  "success": false,
  "keyword": "서울",
  "region": "전국",
  "trend": "stable",
  "trendDescription": "",
  "summary": "\"서울\"에 대한 추세 분석이 지원되지 않습니다.",
  "dataPoints": [],
  "insights": [],
  "note": "지원 키워드: 인구, 총`
- 소스 위치: 소스 위치 미확인
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.
