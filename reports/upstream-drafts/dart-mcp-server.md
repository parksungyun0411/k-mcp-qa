<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] dart-mcp-server: 공통 시험에서 관찰한 동작

한국 공공데이터 MCP 서버 여러 개에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다. SDK 기본 동작으로 확인된 항목은 뺐습니다.

## 환경

- 커밋: `7fdc7c472c99aef1a0536e43ee4c7963bf4bf4bb`
- 실행 명령: `.venv/bin/python run_server.py`
- MCP SDK: mcp 1.6.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 알 수 없는 툴 호출에 JSON-RPC 오류가 아닌 isError 결과로 응답 (발생 1건, 원인 1개)

- 예시: 툴 `kmcpqa_no_such_tool`, 입력 `{}`
- 응답: `tool_error: Function 'kmcpqa_no_such_tool' not found in any module`
- 소스 위치: `dart/mcp_factory.py:81`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 8건, 원인 1개)

- 예시: 툴 `xmlparser_step1_structure`, 입력 `{"path_xml": "test", "max_depth": 1}`
- 응답: `marker='error': [Execution result]
---
error : Traceback (most recent call last):
  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/mcp_factory.py", line 98, in dynamic_function
    responses = await function(*args, **kwarg`
- 소스 위치: `dart/mcp_factory.py:96`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 실행 실패(기관 API 오류·처리 불가)를 isError 없는 결과로 응답 (자리 표시자 키 호출) (발생 79건, 원인 1개)

- 예시: 툴 `get_disclosurelist`, 입력 `{"corp_code": "00126380", "bgn_de": "20250101", "end_de": "20250131"}`
- 응답: `marker='등록되지 않은': [Execution result]
---
error : Traceback (most recent call last):
  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/mcp_factory.py", line 98, in dynamic_function
    responses = await function(*args, **kwa`
- 소스 위치: `dart/mcp_factory.py:96`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 1건, 원인 1개)

- 예시: 툴 `get_corpcode`, 입력 `{}`
- 응답: `missing_required: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpcode
corp_name
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 1건, 원인 1개)

- 예시: 툴 `get_corpcode`, 입력 `{"corp_name": 12345}`
- 응답: `wrong_type: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpcode
corp_name
  Input should be a valid string [type=string_type, input_value=12345, input_type=int]
    For further information visit https://error`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 1건, 원인 1개)

- 예시: 툴 `get_corp_candidates`, 입력 `{}`
- 응답: `missing_required: ERROR: You provided invalid Tool inputs: 2 validation errors for Schema_get_corp_candidates
corp_name
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydant`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 1건, 원인 1개)

- 예시: 툴 `get_corp_candidates`, 입력 `{"corp_name": 12345, "n": "not-a-number"}`
- 응답: `wrong_type: ERROR: You provided invalid Tool inputs: 2 validation errors for Schema_get_corp_candidates
corp_name
  Input should be a valid string [type=string_type, input_value=12345, input_type=int]
    For further information visit https`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 4건, 원인 1개)

- 예시: 툴 `xmlparser_step1_structure`, 입력 `{}`
- 응답: `missing_required: ERROR: You provided invalid Tool inputs: 2 validation errors for Schema_xmlparser_step1_structure
path_xml
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.p`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 4건, 원인 1개)

- 예시: 툴 `xmlparser_step1_structure`, 입력 `{"path_xml": 12345, "max_depth": "not-a-number"}`
- 응답: `wrong_type: ERROR: You provided invalid Tool inputs: 2 validation errors for Schema_xmlparser_step1_structure
path_xml
  Input should be a valid string [type=string_type, input_value=12345, input_type=int]
    For further information visit `
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 78건, 원인 1개)

- 예시: 툴 `get_disclosurelist`, 입력 `{}`
- 응답: `missing_required: ERROR: You provided invalid Tool inputs: 3 validation errors for Schema_get_disclosurelist
corp_code
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydanti`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 78건, 원인 1개)

- 예시: 툴 `get_disclosurelist`, 입력 `{"corp_code": 12345, "bgn_de": 12345, "end_de": 12345, "last_reprt_at": 12345, "pblntf_ty": 12345, "pblntf_detail_ty": 12345, "corp_cls": 12345, "sort": 12345, "sort_mth": 12345, "page_no": "not-a-number", "page_count": "not-a-number"}`
- 응답: `wrong_type: ERROR: You provided invalid Tool inputs: 11 validation errors for Schema_get_disclosurelist
corp_code
  Input should be a valid string [type=string_type, input_value=12345, input_type=int]
    For further information visit https`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 3건, 원인 1개)

- 예시: 툴 `get_corpinfo`, 입력 `{}`
- 응답: `missing_required: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpinfo
corp_code
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 3건, 원인 1개)

- 예시: 툴 `get_corpinfo`, 입력 `{"corp_code": 12345}`
- 응답: `wrong_type: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpinfo
corp_code
  Input should be a valid string [type=string_type, input_value=12345, input_type=int]
    For further information visit https://error`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 1건, 원인 1개)

- 예시: 툴 `get_xbrl_taxonomy_format`, 입력 `{}`
- 응답: `missing_required: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_xbrl_taxonomy_format
sj_div
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydan`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 입력 검증·파싱 오류를 isError 없는 결과로 응답 (발생 1건, 원인 1개)

- 예시: 툴 `get_xbrl_taxonomy_format`, 입력 `{"sj_div": 12345}`
- 응답: `wrong_type: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_xbrl_taxonomy_format
sj_div
  Input should be a valid string [type=string_type, input_value=12345, input_type=int]
    For further information visit http`
- 소스 위치: `dart/mcp_factory.py:117`
- 참고: MCP 2025-11-25 Tools › Error Handling (https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) 의 서술과 다른 동작입니다. 이 절은 규범 키워드가 없는 서술이라 의도된 동작일 수 있습니다.

### 응답 본문에 Python traceback 과 서버 파일 경로가 담김 (발생 87건, 원인 1개)

- 예시: 툴 `xmlparser_step1_structure`, 입력 `{"path_xml": "test", "max_depth": 1}`
- 응답: `valid: [Execution result]
---
error : Traceback (most recent call last):
  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/mcp_factory.py", line 98, in dynamic_function
    responses = await function(*args, **kwargs)
  File`
- 소스 위치: `dart/mcp_factory.py:96`

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다.
