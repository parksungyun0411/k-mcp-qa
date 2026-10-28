# dart-mcp-server

- 저장소: https://github.com/snaiws/DART-mcp-server @ `7fdc7c472c99aef1a0536e43ee4c7963bf4bf4bb`
- 실행 시각: 2026-10-03T11:06:00+00:00 (UTC), 샌드박스: True
- 설치: uv sync --frozen --no-dev
- 실행 명령: `.venv/bin/python run_server.py`, MCP SDK: mcp 1.6.0
- 툴 수: 89, 원본 로그: `reports/raw/dart-mcp-server/`

## 서버 코드

### P4 · 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 — 발생 1건

- 툴: kmcpqa_no_such_tool
- 소스 위치: `dart/mcp_factory.py:81`
- 예시 입력: `{}`
- 응답: "tool_error: Function 'kmcpqa_no_such_tool' not found in any module"
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "kmcpqa_no_such_tool", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 79건

- 툴: get_asset_acquisition_disposal, get_audit_service_contract, get_board_approved_compensation, get_board_compensation_by_type, get_board_total_compensation, get_bond_with_warrants_issuance, get_business_suspension, get_business_transfer_acquisition 외
- 소스 위치: `dart/mcp_factory.py:96`
- 예시 입력: `{"corp_code": "00126380", "bgn_de": "20250101", "end_de": "20250131"}`
- 응답: 'marker=\'등록되지 않은\': [Execution result]\n---\nerror : Traceback (most recent call last):\n  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/mcp_factory.py", line 98, in dynamic_function\n    responses = await function(*args, **kwargs)\n  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/caller'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_disclosurelist", "arguments": {"corp_code": "00126380", "bgn_de": "20250101", "end_de": "20250131"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E1 · 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) — 발생 8건

- 툴: get_auditor_opinion, get_disclosure, get_xbrl_financial_statements, update_corplist, xmlparser_get_table_csv, xmlparser_step1_structure, xmlparser_step2_contents, xmlparser_step3_query
- 소스 위치: `dart/mcp_factory.py:96`
- 예시 입력: `{"path_xml": "test", "max_depth": 1}`
- 응답: 'marker=\'error\': [Execution result]\n---\nerror : Traceback (most recent call last):\n  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/mcp_factory.py", line 98, in dynamic_function\n    responses = await function(*args, **kwargs)\n  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/parser'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "xmlparser_step1_structure", "arguments": {"path_xml": "test", "max_depth": 1}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 78건

- 툴: get_asset_acquisition_disposal, get_audit_service_contract, get_auditor_opinion, get_board_approved_compensation, get_board_compensation_by_type, get_board_total_compensation, get_bond_with_warrants_issuance, get_business_suspension 외
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{}`
- 응답: 'missing_required: ERROR: You provided invalid Tool inputs: 3 validation errors for Schema_get_disclosurelist\ncorp_code\n  Field required [type=missing, input_value={}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.11/v/missing\nbgn_de\n  Field required [type=missing, input_value={}, in'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_disclosurelist", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 78건

- 툴: get_asset_acquisition_disposal, get_audit_service_contract, get_auditor_opinion, get_board_approved_compensation, get_board_compensation_by_type, get_board_total_compensation, get_bond_with_warrants_issuance, get_business_suspension 외
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{"corp_code": 12345, "bgn_de": 12345, "end_de": 12345, "last_reprt_at": 12345, "pblntf_ty": 12345, "pblntf_detail_ty": 12345, "corp_cls": 12345, "sort": 12345, "sort_mth": 12345, "page_no": "not-a-number", "page_count": "not-a-number"}`
- 응답: 'wrong_type: ERROR: You provided invalid Tool inputs: 11 validation errors for Schema_get_disclosurelist\ncorp_code\n  Input should be a valid string [type=string_type, input_value=12345, input_type=int]\n    For further information visit https://errors.pydantic.dev/2.11/v/string_type\nbgn_de\n  Input should be a val'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_disclosurelist", "arguments": {"corp_code": 12345, "bgn_de": 12345, "end_de": 12345, "last_reprt_at": 12345, "pblntf_ty": 12345, "pblntf_detail_ty": 12345, "corp_cls": 12345, "sort": 12345, "sort_mth": 12345, "page_no": "not-a-number", "page_count": "not-a-number"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 4건

- 툴: xmlparser_get_table_csv, xmlparser_step1_structure, xmlparser_step2_contents, xmlparser_step3_query
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{}`
- 응답: 'missing_required: ERROR: You provided invalid Tool inputs: 2 validation errors for Schema_xmlparser_step1_structure\npath_xml\n  Field required [type=missing, input_value={}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.11/v/missing\nmax_depth\n  Field required [type=missing, input_val'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "xmlparser_step1_structure", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 4건

- 툴: xmlparser_get_table_csv, xmlparser_step1_structure, xmlparser_step2_contents, xmlparser_step3_query
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{"path_xml": 12345, "max_depth": "not-a-number"}`
- 응답: 'wrong_type: ERROR: You provided invalid Tool inputs: 2 validation errors for Schema_xmlparser_step1_structure\npath_xml\n  Input should be a valid string [type=string_type, input_value=12345, input_type=int]\n    For further information visit https://errors.pydantic.dev/2.11/v/string_type\nmax_depth\n  Input should '
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "xmlparser_step1_structure", "arguments": {"path_xml": 12345, "max_depth": "not-a-number"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 3건

- 툴: get_corpinfo, get_executive_major_shareholders_reports, get_major_holding_reports
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{}`
- 응답: 'missing_required: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpinfo\ncorp_code\n  Field required [type=missing, input_value={}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.11/v/missing'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_corpinfo", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 3건

- 툴: get_corpinfo, get_executive_major_shareholders_reports, get_major_holding_reports
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{"corp_code": 12345}`
- 응답: 'wrong_type: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpinfo\ncorp_code\n  Input should be a valid string [type=string_type, input_value=12345, input_type=int]\n    For further information visit https://errors.pydantic.dev/2.11/v/string_type'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_corpinfo", "arguments": {"corp_code": 12345}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 1건

- 툴: get_corpcode
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{}`
- 응답: 'missing_required: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpcode\ncorp_name\n  Field required [type=missing, input_value={}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.11/v/missing'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_corpcode", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 1건

- 툴: get_corpcode
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{"corp_name": 12345}`
- 응답: 'wrong_type: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpcode\ncorp_name\n  Input should be a valid string [type=string_type, input_value=12345, input_type=int]\n    For further information visit https://errors.pydantic.dev/2.11/v/string_type'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_corpcode", "arguments": {"corp_name": 12345}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 1건

- 툴: get_corp_candidates
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{}`
- 응답: 'missing_required: ERROR: You provided invalid Tool inputs: 2 validation errors for Schema_get_corp_candidates\ncorp_name\n  Field required [type=missing, input_value={}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.11/v/missing\nn\n  Field required [type=missing, input_value={}, input_'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_corp_candidates", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 1건

- 툴: get_corp_candidates
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{"corp_name": 12345, "n": "not-a-number"}`
- 응답: 'wrong_type: ERROR: You provided invalid Tool inputs: 2 validation errors for Schema_get_corp_candidates\ncorp_name\n  Input should be a valid string [type=string_type, input_value=12345, input_type=int]\n    For further information visit https://errors.pydantic.dev/2.11/v/string_type\nn\n  Input should be a valid in'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_corp_candidates", "arguments": {"corp_name": 12345, "n": "not-a-number"}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 1건

- 툴: get_xbrl_taxonomy_format
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{}`
- 응답: 'missing_required: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_xbrl_taxonomy_format\nsj_div\n  Field required [type=missing, input_value={}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.11/v/missing'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_xbrl_taxonomy_format", "arguments": {}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### E3 · 입력 검증·파싱 오류를 isError 없는 결과로 응답 — 발생 1건

- 툴: get_xbrl_taxonomy_format
- 소스 위치: `dart/mcp_factory.py:117`
- 예시 입력: `{"sj_div": 12345}`
- 응답: 'wrong_type: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_xbrl_taxonomy_format\nsj_div\n  Input should be a valid string [type=string_type, input_value=12345, input_type=int]\n    For further information visit https://errors.pydantic.dev/2.11/v/string_type'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "get_xbrl_taxonomy_format", "arguments": {"sj_div": 12345}}'`
- 근거: [https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) (서술적 설명(규범 키워드 없음))

### H1 · 응답 본문에 Python traceback 과 서버 파일 경로가 담김 — 발생 87건

- 툴: get_asset_acquisition_disposal, get_audit_service_contract, get_auditor_opinion, get_board_approved_compensation, get_board_compensation_by_type, get_board_total_compensation, get_bond_with_warrants_issuance, get_business_suspension 외
- 소스 위치: `dart/mcp_factory.py:96`
- 예시 입력: `{"path_xml": "test", "max_depth": 1}`
- 응답: 'valid: [Execution result]\n---\nerror : Traceback (most recent call last):\n  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/mcp_factory.py", line 98, in dynamic_function\n    responses = await function(*args, **kwargs)\n  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/parser'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server tools/call '{"name": "xmlparser_step1_structure", "arguments": {"path_xml": "test", "max_depth": 1}}'`

## SDK 기본 동작(확인)

### P3 · 알 수 없는 메서드에 -32601 이 아닌 응답(또는 무응답) — 발생 1건

- 툴: -
- 소스 위치: `.venv/lib/python3.10/site-packages/mcp/shared/session.py:307`, `.venv/lib/python3.10/site-packages/mcp/shared/session.py:210`, `.venv/lib/python3.10/site-packages/mcp/server/lowlevel/server.py:121`
- 예시 입력: `{}`
- 응답: 'method=kmcpqa/unknown_method → timeout code=None'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server kmcpqa/unknown_method '{}'`
- 근거: [https://www.jsonrpc.org/specification#error_object](https://www.jsonrpc.org/specification#error_object) (JSON-RPC 2.0 오류 코드 표)

### P6 · 요청 하나를 받은 뒤 서버가 종료되거나 ping 에 응답하지 않음 — 발생 1건

- 툴: -
- 소스 위치: `.venv/lib/python3.10/site-packages/mcp/shared/session.py:307`, `.venv/lib/python3.10/site-packages/mcp/shared/session.py:210`, `.venv/lib/python3.10/site-packages/mcp/server/lowlevel/server.py:121`
- 예시 입력: `{}`
- 응답: 'method=kmcpqa/unknown_method → 이후 응답 없음/종료. stderr: | Traceback (most recent call last): | | pydantic_core._pydantic_core.ValidationError: 24 validation errors for ClientRequest'
- 재현: `uv run python -m kmcpqa.repro dart-mcp-server kmcpqa/unknown_method '{}'`

