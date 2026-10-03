# korea-stats-mcp

- 저장소: https://github.com/Dayoooun/korea-stats-mcp @ `cf8af3dc52eee8f3085f947adc43bb7f65c8ea9b`
- 실행 시각: 2026-10-03T10:58:40+00:00 (UTC), 샌드박스: True
- 설치: npm install --ignore-scripts --no-audit --no-fund --no-package-lock && npx --no-install tsc
- 실행 명령: `node dist/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.32.0
- 툴 수: 14, 원본 로그: `reports/raw/korea-stats-mcp/`

## 서버 코드

### S4 · inputSchema 의 properties 가 비어 있는데 런타임은 특정 인자를 요구함 — 발생 1건

- 툴: get_indicator
- 소스 위치: `src/tools/indicators.ts:121`, `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:222` — tools/list 의 inputSchema 는 properties 가 비어 있고, 검증은 서버가 등록한 스키마로 SDK 가 수행함. 스키마를 JSON Schema 로 바꾸는 과정에서 생겼을 수 있음(확인하지 않음)
- 예시 입력: `{}`
- 응답: 'properties=[] → MCP error -32602: Input validation error: Invalid arguments for tool get_indicator: Required at indicatorId\nRequired at kind'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "get_indicator", "arguments": {}}'`

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: search_statistics
- 소스 위치: `src/utils/errorHandler.ts:41`
- 예시 입력: `{"query": "서울"}`
- 응답: 'marker=\'"success": false\': {\n  "totalCount": 0,\n  "results": [],\n  "queryAnalysis": {\n    "topics": [],\n    "regions": [\n      "11"\n    ],\n    "intent": "search"\n  },\n  "success": false,\n  "error": "알 수 없는 오류가 발생했습니다.",\n  "code": "11"\n}'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "search_statistics", "arguments": {"query": "서울"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: get_statistics_data
- 소스 위치: 소스 위치 미확인
- 예시 입력: `{"orgId": "test", "tableId": "test", "objL1": "test", "periodType": "Y"}`
- 응답: 'marker=\'"success": false\': {\n  "providerTotalCount": null,\n  "providerSnapshot": "unproven",\n  "snapshotScope": "active_partition",\n  "completionScope": "requested_period_traversal",\n  "success": false,\n  "data": [],\n  "validationLevel": "unverified",\n  "metadata": {\n    "orgId": "test",\n    "tableId": "test",\n    "periodType'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "get_statistics_data", "arguments": {"orgId": "test", "tableId": "test", "objL1": "test", "periodType": "Y"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: compare_statistics
- 소스 위치: 소스 위치 미확인
- 예시 입력: `{"orgId": "test", "tableId": "test", "compareType": "period", "periodType": "Y"}`
- 응답: 'marker=\'"success": false\': {\n  "success": false,\n  "compareType": "period",\n  "validationLevel": "unverified",\n  "errorCode": "11",\n  "provenance": {\n    "provider": "kosis",\n    "orgId": "test",\n    "tableId": "test",\n    "sourceUrl": "https://kosis.kr/openapi/Param/statisticsParameterData.do?format=json&jsonVD=Y&method=getL'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "compare_statistics", "arguments": {"orgId": "test", "tableId": "test", "compareType": "period", "periodType": "Y"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: analyze_time_series
- 소스 위치: 소스 위치 미확인
- 예시 입력: `{"orgId": "test", "tableId": "test", "objL1": "test", "periodType": "Y"}`
- 응답: 'marker=\'"success": false\': {\n  "success": false,\n  "validationLevel": "unverified",\n  "errorCode": "11",\n  "provenance": {\n    "provider": "kosis",\n    "orgId": "test",\n    "tableId": "test",\n    "sourceUrl": "https://kosis.kr/openapi/Param/statisticsParameterData.do?format=json&jsonVD=Y&method=getList&newEstPrdCnt=10&objL1=t'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "analyze_time_series", "arguments": {"orgId": "test", "tableId": "test", "objL1": "test", "periodType": "Y"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: get_table_info
- 소스 위치: `src/utils/errorHandler.ts:41`
- 예시 입력: `{"orgId": "test", "tableId": "test"}`
- 응답: 'marker=\'"success": false\': {\n  "success": false,\n  "orgId": "test",\n  "tableId": "test",\n  "infoType": "ITM",\n  "errorCode": "11",\n  "errorMessage": "알 수 없는 오류가 발생했습니다.",\n  "usageHint": "알 수 없는 오류가 발생했습니다."\n}'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "get_table_info", "arguments": {"orgId": "test", "tableId": "test"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: quick_stats
- 소스 위치: 소스 위치 미확인
- 예시 입력: `{"query": "서울"}`
- 응답: 'marker=\'"success": false\': {\n  "success": false,\n  "answer": "\\"서울\\"에 대한 빠른 조회가 지원되지 않습니다.",\n  "note": "📊 지원 키워드 (카테고리별 대표 예시):\\n• 인구/출산: 인구, 출산율, 출생아수, 사망률, 기대수명\\n• 고령화: 고령인구, 노인인구, 노령화지수, 65세이상인구\\n• 고용/노동: 실업률, 고용률, 취업자수, 임금\\n• 경제: GDP, GRDP, 경제성장률, 물가\\n• 무역: 수출, 수입, 무역수지\\n• 혼인/이혼: 혼인율, 이혼율, 초혼연령, 여성초혼연령\\n• 부동산: 주택가격, 아파트가격'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "quick_stats", "arguments": {"query": "서울"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 1건

- 툴: quick_trend
- 소스 위치: 소스 위치 미확인
- 예시 입력: `{"keyword": "서울"}`
- 응답: 'marker=\'"success": false\': {\n  "success": false,\n  "keyword": "서울",\n  "region": "전국",\n  "trend": "stable",\n  "trendDescription": "",\n  "summary": "\\"서울\\"에 대한 추세 분석이 지원되지 않습니다.",\n  "dataPoints": [],\n  "insights": [],\n  "note": "지원 키워드: 인구, 총인구, 출산율, 합계출산율, 실업률, 고용률, GDP, 국내총생산, 물가, 소비자물가, 소비자물가지수, 혼인율, 기대수명, 기대여명, 평균수명, 수출액, 수'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "quick_trend", "arguments": {"keyword": "서울"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

## SDK 기본 동작(확인)

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:144`
- 예시 입력: `{}`
- 응답: 'tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found'
- 재현: `python -m kmcpqa.repro korea-stats-mcp tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

