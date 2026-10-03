# korean-dart-mcp

- 저장소: https://github.com/aesthetic-legalism5470/korean-dart-mcp @ `96315645798697abec785bc7204c237e0f0f0618`
- 실행 시각: 2026-10-03T07:10:35+00:00 (UTC), 샌드박스: True
- 설치: npm ci --ignore-scripts --no-audit --no-fund && npx --no-install tsc
- 실행 명령: `node build/index.js`, MCP SDK: @modelcontextprotocol/sdk 1.29.0
- 원본 로그: `reports/raw/korean-dart-mcp/`

## I3 · 자리 표시자 키로 시작한 뒤 요청 없이 5초 안에 프로세스가 종료됨 (1건)

- 툴 `-` · 입력 `-`
  - 응답: 'exit 1: Error: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result> |     at DartClient.getZip (file:///private/tmp/kmcp-work/korean-dart-mcp/src/build/lib/dart-client.js:49:15) |     at pr'
  - 재현: `python -m kmcpqa.runner --only korean-dart-mcp`

## E2 · 툴 실행 오류를 JSON-RPC 내부 오류(-32603)로 답함 (스펙은 isError 결과로 규정) (44건)

- 툴 `resolve_corp_code` · 입력 `{}`
  - 응답: 'missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "resolve_corp_code", "arguments": {}}'`
- 툴 `resolve_corp_code` · 입력 `{"query": 12345, "limit": "not-a-number"}`
  - 응답: 'wrong_type: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "resolve_corp_code", "arguments": {"query": 12345, "limit": "not-a-number"}}'`
- 툴 `resolve_corp_code` · 입력 `{"query": "서울"}`
  - 응답: 'valid: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "resolve_corp_code", "arguments": {"query": "서울"}}'`
- 툴 `search_disclosures` · 입력 `{"corp": 12345, "begin": 12345, "end": 12345, "days": "not-a-number", "kind": 12345, "preset": 12345, "final_only": "not-a-boolean", "include_corrections": "not-a-boolean", "all_pages": "not-a-boolean", "page": "not-a-number", "size": "not-a-number", "limit": "not-a-number", "concurrency": "not-a-number"}`
  - 응답: 'wrong_type: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "search_disclosures", "arguments": {"corp": 12345, "begin": 12345, "end": 12345, "days": "not-a-number", "kind": 12345, "preset": 12345, "final_only": "not-a-boolean", "include_corrections": "not-a-boolean", "all_pages": "not-a-boolean", "page": "not-a-number", "size": "not-a-number", "limit": "not-a-number", "concurrency": "not-a-number"}}'`
- 툴 `search_disclosures` · 입력 `{}`
  - 응답: 'valid: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "search_disclosures", "arguments": {}}'`
- 툴 `get_company` · 입력 `{}`
  - 응답: 'missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_company", "arguments": {}}'`
- 툴 `get_company` · 입력 `{"corp": 12345}`
  - 응답: 'wrong_type: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_company", "arguments": {"corp": 12345}}'`
- 툴 `get_company` · 입력 `{"corp": "test"}`
  - 응답: 'valid: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_company", "arguments": {"corp": "test"}}'`
- 툴 `get_financials` · 입력 `{}`
  - 응답: 'missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_financials", "arguments": {}}'`
- 툴 `get_financials` · 입력 `{"corps": "not-an-array", "year": "not-a-number", "report": 12345, "scope": 12345, "fs": 12345, "sj_div": "not-an-array"}`
  - 응답: 'wrong_type: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_financials", "arguments": {"corps": "not-an-array", "year": "not-a-number", "report": 12345, "scope": 12345, "fs": 12345, "sj_div": "not-an-array"}}'`
- 툴 `get_financials` · 입력 `{"corps": ["test"], "year": 2015}`
  - 응답: 'valid: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_financials", "arguments": {"corps": ["test"], "year": 2015}}'`
- 툴 `download_document` · 입력 `{}`
  - 응답: 'missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "download_document", "arguments": {}}'`
- 툴 `download_document` · 입력 `{"rcept_no": 12345, "format": 12345, "truncate_at": "not-a-number"}`
  - 응답: 'wrong_type: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "download_document", "arguments": {"rcept_no": 12345, "format": 12345, "truncate_at": "not-a-number"}}'`
- 툴 `download_document` · 입력 `{"rcept_no": "20240312000736"}`
  - 응답: 'valid: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "download_document", "arguments": {"rcept_no": "20240312000736"}}'`
- 툴 `get_xbrl` · 입력 `{}`
  - 응답: 'missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_xbrl", "arguments": {}}'`
- 툴 `get_xbrl` · 입력 `{"rcept_no": 12345, "report": 12345, "format": 12345, "fs_div": 12345, "sections": "not-an-array", "out_dir": 12345}`
  - 응답: 'wrong_type: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_xbrl", "arguments": {"rcept_no": 12345, "report": 12345, "format": 12345, "fs_div": 12345, "sections": "not-an-array", "out_dir": 12345}}'`
- 툴 `get_xbrl` · 입력 `{"rcept_no": "20240312000736"}`
  - 응답: 'valid: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_xbrl", "arguments": {"rcept_no": "20240312000736"}}'`
- 툴 `get_periodic_report` · 입력 `{}`
  - 응답: 'missing_required: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_periodic_report", "arguments": {}}'`
- 툴 `get_periodic_report` · 입력 `{"corp": 12345, "year": "not-a-number", "report": 12345, "report_type": 12345}`
  - 응답: 'wrong_type: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_periodic_report", "arguments": {"corp": 12345, "year": "not-a-number", "report": 12345, "report_type": 12345}}'`
- 툴 `get_periodic_report` · 입력 `{"corp": "test", "year": 2015, "report_type": "largest_shareholder"}`
  - 응답: 'valid: DART corpCode.xml → 비-ZIP 응답 (150B): <?xml version="1.0" encoding="UTF-8" standalone="yes"?><result><status>010</status><message>등록되지 않은 인증키입니다.</message></result>'
  - 재현: `python -m kmcpqa.repro korean-dart-mcp tools/call '{"name": "get_periodic_report", "arguments": {"corp": "test", "year": 2015, "report_type": "largest_shareholder"}}'`
- 외 24건은 `reports/results/korean-dart-mcp.json` 참고
