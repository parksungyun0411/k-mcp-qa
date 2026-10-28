# korean-dart-mcp

- 저장소: https://github.com/aesthetic-legalism5470/korean-dart-mcp @ `4b2e072491f193833efb01c7fc76af1699ec176f`
- 실행 시각: 2026-10-03T11:05:40+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc
- 실행 명령: `node build/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.29.0
- 툴 수: 15, 원본 로그: `reports/raw/korean-dart-mcp/`

## 서버 코드

### I3 · 자리 표시자 키로 시작한 뒤 요청 없이 5초 안에 프로세스가 종료됨 — 발생 1건

- 툴: -
- 소스 위치: `build/lib/corp-code.js:55`, `build/lib/dart-client.js:49`
- 예시 입력: `-`
- 응답: 'exit 1: triggerUncaughtException(err, true /* fromPromise */); | Error: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
- 재현: `uv run python -m kmcpqa.runner --only korean-dart-mcp`

### E2 · 기관 API 실패를 JSON-RPC 내부 오류(-32603)로 응답 — 발생 44건

- 툴: buffett_quality_snapshot, disclosure_anomaly, download_document, get_attachments, get_company, get_corporate_event, get_executive_compensation, get_financials 외
- 소스 위치: `src/lib/dart-client.ts:67`, `src/server/mcp-server.ts:45`, `node_modules/@modelcontextprotocol/sdk/dist/esm/shared/protocol.js:398` — 서버의 low-level CallTool 핸들러가 던진 예외를 SDK 프로토콜 계층이 -32603 으로 바꿈
- 예시 입력: `{}`
- 응답: 'missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
- 재현: `uv run python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "resolve_corp_code", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

