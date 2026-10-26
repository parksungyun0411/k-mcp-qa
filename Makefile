PY ?= uv run python
WORKDIR ?= /tmp/kmcp-work

.PHONY: install probe external report agreement test lint

install:
	uv sync --extra dev

probe:  ## 받기·설치·키 없는 공통 시험 (servers.toml 전체)
	$(PY) -m kmcpqa.runner --reinstall --workdir $(WORKDIR)

external:  ## 공식 conformance 와 mcp-audit 을 같은 격리 환경에서 실행
	$(PY) -m kmcpqa.external --workdir $(WORKDIR)

report:  ## reports/RESULTS.md, findings/, upstream-drafts/ 생성
	$(PY) -m kmcpqa.report --workdir $(WORKDIR)

agreement:  ## MCP 응답 대 기관 API 직접 호출 (키 필요, .env 를 읽는다. make probe 로 설치된 서버를 띄운다)
	uv run $(if $(wildcard .env),--env-file .env,) python -m kmcpqa.agreement --workdir $(WORKDIR)

test:
	uv run pytest -q

lint:
	uv run ruff check .
