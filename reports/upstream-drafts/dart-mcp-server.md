<!-- k-mcp-qa 이슈 초안. 자동 생성. 제출하지 않았음. 올리기 전 내용을 직접 재현·검토할 것. -->
# [재현 보고] dart-mcp-server: MCP 공통 시험에서 관찰한 동작

안녕하세요. 한국 공공데이터 MCP 서버들에 같은 시험을 돌려 보다가 아래 동작을 관찰해 공유드립니다. 실제 API 키 없이(자리 표시자 값) 실행한 결과입니다.

## 환경

- 커밋: `7fdc7c472c99aef1a0536e43ee4c7963bf4bf4bb`
- 실행 명령: `.venv/bin/python run_server.py`
- MCP SDK: mcp 1.6.0, 클라이언트 요청 프로토콜 버전 2025-11-25
- 날짜: 2026-10-03

## 관찰

### 알 수 없는 메서드에 -32601 오류로 답하지 않음

- 툴 `-`, 입력 `-` (같은 유형 1건)
- 응답: `method=kmcpqa/unknown_method outcome=timeout code=None`

### 요청 하나를 처리한 뒤 서버 프로세스가 종료됨

- 툴 `kmcpqa_no_such_tool`, 입력 `{}` (같은 유형 1건)
- 응답: `process exited`

### 기관 API·실행 오류를 isError 없는 결과로 돌려줌 (자리 표시자 키 호출)

- 툴 `xmlparser_step1_structure`, 입력 `{"path_xml": "test", "max_depth": 1}` (같은 유형 87건)
- 응답: `marker='error': [Execution result]
---
error : Traceback (most recent call last):
  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/mcp_factory.py", line 98, in dynamic_function
    r`

### 입력 검증 오류를 isError 없는 결과로 돌려줌

- 툴 `get_corpcode`, 입력 `{}` (같은 유형 176건)
- 응답: `missing_required → isError 없음: ERROR: You provided invalid Tool inputs: 1 validation error for Schema_get_corpcode
corp_name
  Field required [type=missing, input_value={}, input_type=dict]
    For fu`

### 응답 본문에 Python traceback 과 서버 파일 경로가 담김

- 툴 `xmlparser_step1_structure`, 입력 `{"path_xml": "test", "max_depth": 1}` (같은 유형 87건)
- 응답: `valid: [Execution result]
---
error : Traceback (most recent call last):
  File "/private/tmp/kmcp-work/dart-mcp-server/src/mcp_server/dart/mcp_factory.py", line 98, in dynamic_function
    responses `

## 재현

요청·응답 원문 로그(JSON-RPC 송수신 기록)는 필요하시면 첨부하겠습니다. MCP 2025-11-25 스펙의 해당 항목과 다르게 보이는 부분만 적었습니다. 의도된 동작이라면 알려 주세요.
