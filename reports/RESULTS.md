# 결과

실행: 2026-10-03T07:09:45+00:00 (UTC) · 요청한 프로토콜 버전 2025-11-25 · node v26.0.0 · npm 11.12.1 · uv 0.12.22 (Homebrew 2026-10-01 aarch64-apple-darwin) · macOS-15.7.9-arm64-arm-64bit

스펙 스키마: `modelcontextprotocol/modelcontextprotocol@75db1e987cbbba6d170315dc99d0dfc440754aef:schema/2025-11-25/schema.json`  
공식 conformance: `@modelcontextprotocol/conformance@0.1.16` (server-initialize, ping, tools-list)  
mcp-audit: `Alpha-W0lf/mcp-audit@b14487ff9af2ea539fa946755949173459c2cbb9` (SCHEMA001, RUNTIME001, HYGIENE001)

모든 서버는 실제 키 없이 실행했다. 키 변수에는 자리 표시자 문자열을 넣었다. 따라서 기관 API 를 실제로 부르는 호출은 인증 오류를 받는 것이 정상이며, 아래 표는 그 상황에서의 동작이다.

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
| [korean-dart-mcp](findings/korean-dart-mcp.md) | `9631564579` (2026-10-01) | MIT | @modelcontextprotocol/sdk 1.29.0 | 성공 | 종료(코드 1) | 응답 (2025-11-25) | 15 | server-initialize 통과<br>ping 실패<br>tools-list 실패 | pass 16 / fail 0 / skip 29 |
| [korean-law-mcp](findings/korean-law-mcp.md) | `ff33a71397` (2026-10-02) | MIT | @modelcontextprotocol/sdk 1.30.0 | 성공 | 시작함 | 응답 (2025-11-25) | 10 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 17 / fail 2 / skip 11 |
| [mcp-korea-tourism-api](findings/mcp-korea-tourism-api.md) | `c4d4585cb8` (2025-08-12) | MIT | mcp 1.9.4, fastmcp 2.9.0 | 성공 | 시작함 | 응답 (2025-03-26) | 8 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 10 / fail 1 / skip 13 |
| [real-estate-mcp](findings/real-estate-mcp.md) | `1119eb1069` (2026-07-18) | MIT | mcp 1.26.0 | 성공 | 시작함 | 응답 (2025-11-25) | 16 | server-initialize 통과<br>ping 통과<br>tools-list 통과 | pass 48 / fail 0 / skip 0 |

## 관찰 유형별 건수

툴 하나에서 여러 입력으로 같은 유형이 나오면 각각 센다. 유형 정의는 아래 표.

| 서버 | I2 | I3 | P3 | P4 | P6 | R3 | E1 | E2 | E3 | H1 |
|---|---|---|---|---|---|---|---|---|---|---|
| assembly-api-mcp | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| dart-mcp-server | 0 | 0 | 1 | 0 | 1 | 0 | 87 | 0 | 176 | 87 |
| data-go-nts-business-verification-mcp1 | 0 | 0 | 1 | 1 | 0 | 0 | 3 | 0 | 0 | 0 |
| data-go-nts-business-verification | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| data4library-mcp | 0 | 0 | 0 | 1 | 0 | 0 | 13 | 0 | 0 | 0 |
| korea-stats-mcp | 0 | 0 | 0 | 1 | 0 | 1 | 7 | 0 | 0 | 0 |
| korea-stock-mcp | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| korean-dart-mcp | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 44 | 0 | 0 |
| korean-law-mcp | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 |
| mcp-korea-tourism-api | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| real-estate-mcp | 0 | 0 | 1 | 1 | 0 | 0 | 12 | 0 | 0 | 0 |

## 관찰 유형

| 코드 | 분류 | 내용 |
|---|---|---|
| I1 | 설치·기동 | 고정한 커밋에서 문서의 설치 절차가 실패함 |
| I2 | 설치·기동 | 자리 표시자 키를 넣어도 initialize 응답이 오지 않음 |
| I3 | 설치·기동 | 자리 표시자 키로 시작한 뒤 요청 없이 5초 안에 프로세스가 종료됨 |
| P1 | 프로토콜 | stdout 에 JSON-RPC 가 아닌 줄을 씀 |
| P2 | 프로토콜 | 응답이 MCP 2025-11-25 스키마를 어김 |
| P3 | 프로토콜 | 알 수 없는 메서드에 -32601 오류로 답하지 않음 |
| P4 | 프로토콜 | 알 수 없는 툴 호출을 JSON-RPC 오류가 아닌 isError 결과로 답함 |
| P5 | 프로토콜 | tools/call 이 제한 시간 안에 응답하지 않음 |
| P6 | 프로토콜 | 요청 하나를 처리한 뒤 서버 프로세스가 종료됨 |
| S1 | 스키마 | inputSchema/outputSchema 가 메타스키마 검증을 통과하지 못함 |
| S2 | 스키마 | required 에 properties 에 없는 이름이 있음 |
| S3 | 스키마 | outputSchema 를 선언했지만 structuredContent 가 없거나 스키마와 다름 |
| R1 | 스키마-런타임 불일치 | 선언된 필수 인자를 빼고 호출해도 오류 없이 결과를 돌려줌 |
| R2 | 스키마-런타임 불일치 | 선언과 다른 타입의 인자로 호출해도 오류 없이 결과를 돌려줌 |
| R3 | 스키마-런타임 불일치 | 스키마를 만족하는 입력을 인자 누락·형식 문제로 거부함 |
| E1 | 오류 처리 | 기관 API·실행 오류를 isError 없는 결과로 돌려줌 (자리 표시자 키 호출) |
| E2 | 오류 처리 | 툴 실행 오류를 JSON-RPC 내부 오류(-32603)로 답함 (스펙은 isError 결과로 규정) |
| E3 | 오류 처리 | 입력 검증 오류를 isError 없는 결과로 돌려줌 |
| H1 | 오류 처리 | 응답 본문에 Python traceback 과 서버 파일 경로가 담김 |

## 시험하지 않은 서버

| 저장소 | 커밋 | 이유 |
|---|---|---|
| aeriis-kr/opendata-mcp | `5be040fd5a` | stdio 진입점이 없다. src/index.ts 가 Smithery 런타임용 createStatelessServer 만 내보내며 실행에는 @smithery/cli 가 필요하다. 목록의 저장소 주소는 aeriis-kr/opendata-mcp 로 옮겨져 있다. |
| worker-ants/korea-weather-mcp | `2b76e5dc42` | 표본을 10개로 제한하면서 제외했다. 실행 위험 때문이 아니다. |
