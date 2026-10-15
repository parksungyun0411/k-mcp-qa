# 결과

실행: 2026-10-03T11:05:40+00:00 (UTC) · 요청한 프로토콜 버전 2025-11-25 · node v26.0.0 · npm 11.12.1 · uv 0.12.22 (Homebrew 2026-10-01 aarch64-apple-darwin) · macOS-15.7.9-arm64-arm-64bit

스펙 스키마: `modelcontextprotocol/modelcontextprotocol@75db1e987cbbba6d170315dc99d0dfc440754aef:schema/2025-11-25/schema.json`  
공식 conformance: `@modelcontextprotocol/conformance@0.1.16` (server-initialize, ping, tools-list)  
mcp-audit: `Alpha-W0lf/mcp-audit@b14487ff9af2ea539fa946755949173459c2cbb9` (SCHEMA001, RUNTIME001, HYGIENE001)

모든 서버는 실제 키 없이 실행했다. 키 변수에는 자리 표시자 문자열을 넣었다. 따라서 기관 API 를 실제로 부르는 호출은 인증 오류를 받는 것이 정상이며, 아래 표는 그 상황에서의 동작이다.

관찰은 출처별로 나눈다. **서버 코드**: 응답 문구·스택이 서버 저장소 소스에서 확인되었거나 툴 핸들러가 만든 응답. **SDK 기본 동작(확인)**: 응답 문구·스택이 설치된 MCP SDK 소스에서만 확인됨 — 서버에 대한 관찰이 아니다. **출처 미확인**: 어느 쪽에서도 위치를 찾지 못함.

## 서버별 요약

| 서버 | 커밋 (날짜) | 라이선스 | MCP SDK | 설치 | 키 없이 시작 | initialize (협상 버전) | 툴 수 | 공식 conformance | mcp-audit |
|---|---|---|---|---|---|---|---|---|---|
| [assembly-api-mcp](findings/assembly-api-mcp.md) | `f74c6b452c` (2026-05-02) | MIT | @modelcontextprotocol/sdk 1.29.0 | 성공 | 종료(코드 1) | 응답 (2025-11-25) | 6 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 18 / fail 0 / skip 0 |
| [dart-mcp-server](findings/dart-mcp-server.md) | `7fdc7c472c` (2025-07-07) | MIT | mcp 1.6.0 | 성공 | 시작함 | 응답 (2024-11-05) | 89 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 176 / fail 91 / skip 0 |
| [data-go-nts-business-verification-mcp1](findings/data-go-nts-business-verification-mcp1.md)<br>(변형: mcp<2 고정) | `dd27f99490` (2025-09-17) | Apache-2.0 | mcp 1.30.0 | 성공 | 시작함 | 응답 (2025-11-25) | 3 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 9 / fail 0 / skip 0 |
| [data-go-nts-business-verification](findings/data-go-nts-business-verification.md) | `dd27f99490` (2025-09-17) | Apache-2.0 | mcp 2.3.0 | 성공 | 종료(코드 1) | closed | - | - | - |
| [data4library-mcp](findings/data4library-mcp.md) | `5708f84552` (2026-09-02) | MIT | @modelcontextprotocol/sdk 1.30.0 | 성공 | 종료(코드 1) | 응답 (2025-11-25) | 27 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 55 / fail 0 / skip 26 |
| [korea-stats-mcp](findings/korea-stats-mcp.md) | `cf8af3dc52` (2026-10-01) | MIT | @modelcontextprotocol/sdk 1.32.0 | 성공 | 시작함 | 응답 (2025-11-25) | 14 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 35 / fail 0 / skip 7 |
| [korea-stock-mcp](findings/korea-stock-mcp.md) | `210595eec7` (2026-08-04) | ISC | @modelcontextprotocol/sdk 1.29.0 | 성공 | 시작함 | 응답 (2025-11-25) | 8 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 12 / fail 0 / skip 12 |
| [korean-dart-mcp](findings/korean-dart-mcp.md) | `4b2e072491` (2026-10-03) | MIT | @modelcontextprotocol/sdk 1.29.0 | 성공 | 종료(코드 1) | 응답 (2025-11-25) | 15 | server-initialize 측정 불가(서버 프로세스 종료)<br>ping 측정 불가(서버 프로세스 종료)<br>tools-list 측정 불가(서버 프로세스 종료) | pass 16 / fail 0 / skip 29 |
| [korean-law-mcp](findings/korean-law-mcp.md) | `ff33a71397` (2026-10-02) | MIT | @modelcontextprotocol/sdk 1.30.0 | 성공 | 시작함 | 응답 (2025-11-25) | 10 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 17 / fail 2 / skip 11 |
| [mcp-korea-tourism-api](findings/mcp-korea-tourism-api.md) | `c4d4585cb8` (2025-08-12) | MIT | mcp 1.9.4, fastmcp 2.9.0 | 성공 | 시작함 | 응답 (2025-03-26) | 8 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 10 / fail 1 / skip 13 |
| [real-estate-mcp](findings/real-estate-mcp.md) | `1119eb1069` (2026-07-18) | MIT | mcp 1.26.0 | 성공 | 시작함 | 응답 (2025-11-25) | 16 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 48 / fail 0 / skip 0 |

`측정 불가(서버 프로세스 종료)`: 시나리오 도중 서버 프로세스가 이미 종료되어, 응답을 k-mcp-qa 중계기가 대신 만든 경우다(중계기 오류 코드 -32099). 서버의 conformance 실패로 세지 않는다.

## 서버 코드에서 나온 관찰

칸의 값은 `문구 유형 수/발생 수`. 같은 코드·같은 출처·같은 문구(입력 값·숫자 제거)를 한 문구 유형으로 묶었다. 근본 원인 수가 아니며, 같은 소스 줄에서 나온 응답도 입력 종류나 응답 모양에 따라 여러 유형으로 나뉠 수 있다. 발생 수는 툴 수에 비례해 늘어나므로 서버 사이 비교에는 문구 유형 수나 툴당 발생 수를 본다.

| 서버 | 툴 수 | 문구 유형 수 | 발생 수 | 툴당 발생 | I2 | I3 | P4 | S4 | R3 | E1 | E2 | E3 | H1 |
|---|---:|---:|---:|---:|---|---|---|---|---|---|---|---|---|
| assembly-api-mcp | 6 | 0 | 0 | 0.00 |  |  |  |  |  |  |  |  |  |
| dart-mcp-server | 89 | 16 | 351 | 3.94 |  |  | 1/1 |  |  | 2/87 |  | 12/176 | 1/87 |
| data-go-nts-business-verification-mcp1 | 3 | 3 | 3 | 1.00 |  |  |  |  |  | 2/2 |  | 1/1 |  |
| data-go-nts-business-verification | - | 1 | 1 | - | 1/1 |  |  |  |  |  |  |  |  |
| data4library-mcp | 27 | 1 | 13 | 0.48 |  |  |  |  |  | 1/13 |  |  |  |
| korea-stats-mcp | 14 | 8 | 8 | 0.57 |  |  |  | 1/1 |  | 7/7 |  |  |  |
| korea-stock-mcp | 8 | 1 | 1 | 0.12 |  |  |  |  | 1/1 |  |  |  |  |
| korean-dart-mcp | 15 | 2 | 45 | 3.00 |  | 1/1 |  |  |  |  | 1/44 |  |  |
| korean-law-mcp | 10 | 3 | 3 | 0.30 |  |  | 1/1 |  | 2/2 |  |  |  |  |
| mcp-korea-tourism-api | 8 | 0 | 0 | 0.00 |  |  |  |  |  |  |  |  |  |
| real-estate-mcp | 16 | 3 | 12 | 0.75 |  |  |  |  |  | 3/12 |  |  |  |

## SDK 기본 동작으로 확인된 관찰 (서버에 대한 관찰이 아님)

| 서버 | 코드 | SDK | SDK 소스 위치 | 응답 |
|---|---|---|---|---|
| assembly-api-mcp | P4 | @modelcontextprotocol/sdk 1.29.0 | `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:104` | 'tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found' |
| dart-mcp-server | P3 | mcp 1.6.0 | `.venv/lib/python3.10/site-packages/mcp/shared/session.py:307`, `.venv/lib/python3.10/site-packages/mcp/shared/session.py:210`, `.venv/lib/python3.10/site-packages/mcp/server/lowlevel/server.py:121` | 'method=kmcpqa/unknown_method → timeout code=None' |
| dart-mcp-server | P6 | mcp 1.6.0 | `.venv/lib/python3.10/site-packages/mcp/shared/session.py:307`, `.venv/lib/python3.10/site-packages/mcp/shared/session.py:210`, `.venv/lib/python3.10/site-packages/mcp/server/lowlevel/server.py:121` | 'method=kmcpqa/unknown_method → 이후 응답 없음/종료. stderr: | Traceback (most recent call last): | | pydantic_core._pydantic_cor' |
| data-go-nts-business-verification-mcp1 | P3 | mcp 1.30.0 | `.venv/lib/python3.12/site-packages/mcp/shared/session.py:390` | 'method=kmcpqa/unknown_method → error code=-32602 Invalid request parameters' |
| data-go-nts-business-verification-mcp1 | P4 | mcp 1.30.0 | `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/tool_manager.py:78`, `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/tool_manager.py:91` | 'tool_error: Unknown tool: kmcpqa_no_such_tool' |
| data4library-mcp | P4 | @modelcontextprotocol/sdk 1.30.0 | `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:104` | 'tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found' |
| korea-stats-mcp | P4 | @modelcontextprotocol/sdk 1.32.0 | `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:144` | 'tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found' |
| korea-stock-mcp | P4 | @modelcontextprotocol/sdk 1.29.0 | `node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:104` | 'tool_error: MCP error -32602: Tool kmcpqa_no_such_tool not found' |
| mcp-korea-tourism-api | P3 | mcp 1.9.4, fastmcp 2.9.0 | `.venv/lib/python3.12/site-packages/mcp/shared/session.py:367` | 'method=kmcpqa/unknown_method → error code=-32602 Invalid request parameters' |
| mcp-korea-tourism-api | P4 | mcp 1.9.4, fastmcp 2.9.0 | `.venv/lib/python3.12/site-packages/fastmcp/server/server.py:348`, `.venv/lib/python3.12/site-packages/fastmcp/server/server.py:609`, `.venv/lib/python3.12/site-packages/fastmcp/server/server.py:611` | 'tool_error: Unknown tool: kmcpqa_no_such_tool' |
| real-estate-mcp | P3 | mcp 1.26.0 | `.venv/lib/python3.12/site-packages/mcp/shared/session.py:390` | 'method=kmcpqa/unknown_method → error code=-32602 Invalid request parameters' |
| real-estate-mcp | P4 | mcp 1.26.0 | `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/tool_manager.py:78`, `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/tool_manager.py:91` | 'tool_error: Unknown tool: kmcpqa_no_such_tool' |

## 관찰 유형

| 코드 | 분류 | 내용 | 근거 |
|---|---|---|---|
| I1 | 설치·기동 | 고정한 커밋에서 문서의 설치 절차가 실패함 | - |
| I2 | 설치·기동 | 자리 표시자 키를 넣어도 initialize 응답이 오지 않음 | - |
| I3 | 설치·기동 | 자리 표시자 키로 시작한 뒤 요청 없이 5초 안에 프로세스가 종료됨 | - |
| P1 | 프로토콜 | stdout 에 JSON-RPC 가 아닌 줄을 씀 | - |
| P2 | 프로토콜 | 응답이 MCP 2025-11-25 JSON 스키마를 어김 | - |
| P3 | 프로토콜 | 알 수 없는 메서드에 -32601 이 아닌 응답(또는 무응답) | JSON-RPC 2.0 오류 코드 표 — https://www.jsonrpc.org/specification#error_object |
| P4 | 프로토콜 | 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 | 서술적 설명(규범 키워드 없음) — https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling |
| P5 | 프로토콜 | tools/call 이 제한 시간 안에 응답하지 않음 | - |
| P6 | 프로토콜 | 요청 하나를 받은 뒤 서버가 종료되거나 ping 에 응답하지 않음 | - |
| S1 | 스키마 | inputSchema/outputSchema 가 메타스키마 검증을 통과하지 못함 | - |
| S2 | 스키마 | required 에 properties 에 없는 이름이 있음 | - |
| S3 | 스키마 | outputSchema 를 선언했지만 structuredContent 가 없거나 스키마와 다름 | - |
| S4 | 스키마 | inputSchema 의 properties 가 비어 있는데 런타임은 특정 인자를 요구함 | - |
| R1 | 스키마-런타임 불일치 | 선언된 필수 인자를 빼고 호출해도 오류 없이 결과를 돌려줌 | - |
| R2 | 스키마-런타임 불일치 | 선언과 다른 타입의 인자로 호출해도 오류 없이 결과를 돌려줌 | - |
| R3 | 스키마-런타임 불일치 | 스키마를 만족하는 입력을 스키마에 없는 인자 조건으로 거부함 | - |
| E1 | 오류 처리 | 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) | 서술적 설명(규범 키워드 없음) — https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling |
| E2 | 오류 처리 | 기관 API 실패를 JSON-RPC 내부 오류(-32603)로 응답 | 서술적 설명(규범 키워드 없음) — https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling |
| E3 | 오류 처리 | 입력 검증·파싱 오류를 isError 없는 결과로 응답 | 서술적 설명(규범 키워드 없음) — https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling |
| H1 | 오류 처리 | 응답 본문에 Python traceback 과 서버 파일 경로가 담김 | - |

## 근거 문장 (원문 그대로)

MCP 2025-11-25, Tools › Error Handling — https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling

> Tools use two error reporting mechanisms:
> 1. **Protocol Errors**: Standard JSON-RPC errors for issues like:
>    - Unknown tools
>    - Malformed requests (requests that fail to satisfy CallToolRequest schema)
>    - Server errors
> 2. **Tool Execution Errors**: Reported in tool results with `isError: true`:
>    - API failures
>    - Input validation errors (e.g., date in wrong format, value out of range)
>    - Business logic errors

이 절에는 MUST/SHOULD 같은 규범 키워드가 없다. P4·E1·E2·E3 은 이 서술과 다른 동작을 기록한 것이며 스펙 위반 판정이 아니다.

JSON-RPC 2.0, Error object — https://www.jsonrpc.org/specification#error_object

> -32601 | Method not found | The method does not exist / is not available.

## 시험하지 않은 서버

| 저장소 | 커밋 | 이유 |
|---|---|---|
| aeriis-kr/opendata-mcp | `5be040fd5a` | stdio 진입점이 없다. src/index.ts 가 Smithery 런타임용 createStatelessServer 만 내보내며 실행에는 @smithery/cli 가 필요하다. 목록의 저장소 주소는 aeriis-kr/opendata-mcp 로 옮겨져 있다. |
| worker-ants/korea-weather-mcp | `2b76e5dc42` | 표본을 10개로 제한하면서 제외했다. 실행 위험 때문이 아니다. |
