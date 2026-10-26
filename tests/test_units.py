"""매니페스트, 샌드박스 프로파일, 입력 합성, 스키마 검사, 보고서 생성."""

import json
from pathlib import Path

from kmcpqa.manifest import ServerSpec, load
from kmcpqa.report import render
from kmcpqa.sandbox import PLACEHOLDER, Workspace, node_prefix, sandbox_profile
from kmcpqa.specschema import check_json_schema, spec_errors
from kmcpqa.synth import valid_args, wrong_type_args

ROOT = Path(__file__).parent.parent


def test_manifest_loads_and_pins_full_shas():
    servers, skipped = load(ROOT / "servers.toml")
    assert len(servers) >= 8
    assert all(len(s.sha) == 40 for s in servers)
    assert all(s.install and s.command for s in servers)
    assert skipped and all(s.reason for s in skipped)
    npm_installs = [step for s in servers for step in s.install if step[:1] == ["npm"]]
    assert all("--ignore-scripts" in step for step in npm_installs)


def test_env_has_no_host_secrets_and_uses_placeholder(tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "should-not-leak")
    spec = ServerSpec("x", "o/r", "0" * 40, "MIT", "node", "-", [["true"]], ["node"], ["SOME_KEY"])
    ws = Workspace(tmp_path, use_sandbox=False)
    env = ws.env(spec, "placeholder")
    assert env["SOME_KEY"] == PLACEHOLDER
    assert "GITHUB_TOKEN" not in env
    assert env["HOME"].startswith(str(tmp_path))
    assert "SOME_KEY" not in ws.env(spec, "none")


def test_sandbox_profile_denies_home_and_outside_writes(tmp_path):
    prof = sandbox_profile(tmp_path, Path("/Users/someone"), Path("/Users/someone/.local/share/uv/python"))
    assert '(deny file-read* (subpath "/Users/someone"))' in prof
    assert "(deny file-write*)" in prof
    assert str(tmp_path.resolve()) in prof
    node = Path("/Users/someone/.nvm/versions/node/v20.20.2")
    prof2 = sandbox_profile(tmp_path, Path("/Users/someone"), Path("/Users/someone/.local/share/uv/python"),
                            (node,))
    assert f'(subpath "{node}")' in prof2


def test_node_prefix_never_opens_home(tmp_path, monkeypatch):
    import kmcpqa.sandbox as sb
    monkeypatch.setattr(sb.Path, "home", lambda: tmp_path)
    monkeypatch.setattr(sb.shutil, "which", lambda n: None)
    assert node_prefix() is None
    (tmp_path / "bin").mkdir()
    (tmp_path / "bin" / "node").touch()
    monkeypatch.setattr(sb.shutil, "which", lambda n: str(tmp_path / "bin" / "node"))
    assert node_prefix() is None
    nvm = tmp_path / ".nvm/versions/node/v20/bin"
    nvm.mkdir(parents=True)
    (nvm / "node").touch()
    monkeypatch.setattr(sb.shutil, "which", lambda n: str(nvm / "node"))
    assert node_prefix() == nvm.parent.resolve()


def test_synth_valid_and_wrong_type():
    schema = {"type": "object", "properties": {"corp_code": {"type": "string"},
                                               "n": {"type": "integer", "minimum": 3},
                                               "kind": {"type": "string", "enum": ["A", "B"]}},
              "required": ["corp_code", "n", "kind"]}
    assert valid_args(schema) == {"corp_code": "00126380", "n": 3, "kind": "A"}
    assert wrong_type_args(schema) == {"corp_code": 12345, "n": "not-a-number", "kind": 12345}
    assert valid_args({"type": "object", "properties": {"d": {"type": "string", "pattern": "^x$"}},
                       "required": ["d"]}) is None


def test_schema_checks():
    assert check_json_schema({"type": "object", "properties": {}, "required": ["a"]}) == [
        "required not in properties: ['a']"]
    assert check_json_schema({"type": "objekt"})[0].startswith("metaschema")
    assert check_json_schema({"$schema": "http://json-schema.org/draft-07/schema#", "type": "object"}) == []
    assert spec_errors("InitializeResult", {"protocolVersion": "2025-11-25"})  # capabilities 등 누락
    assert spec_errors("CallToolResult", {"content": [{"type": "text", "text": "x"}]}) == []


def test_render_writes_results_findings_and_drafts(tmp_path):
    record = {
        "id": "korea-stock-mcp", "repo": "jjlabsio/korea-stock-mcp", "sha_tested": "a" * 40,
        "started_at": "2026-10-03T00:00:00+00:00", "protocol_version_requested": "2025-11-25",
        "command": ["node", "dist/index.js"], "install_steps": [["npm", "ci"]], "sandbox": True,
        "install": {"ok": True}, "sdk": {"@modelcontextprotocol/sdk": "1.29.0"},
        "start_without_key": {"initialize": "result"},
        "probe": {"initialize": {"outcome": "result", "protocolVersion": "2025-11-25", "spec_violations": []},
                  "tools_list": {"count": 1, "spec_violations": []}, "ping": {"spec_violations": []},
                  "unknown_method": {"outcome": "error", "error_code": -32601, "alive_after": True},
                  "unknown_tool": {"outcome": "tool_error", "text_excerpt": "Tool x not found",
                                   "alive_after": True},
                  "idle_alive": True, "stdout_noise": {"count": 0}, "tools": []},
    }
    results = tmp_path / "results"
    results.mkdir()
    (results / "korea-stock-mcp.json").write_text(json.dumps(record))
    render({"run_at": "2026-10-03", "tools": {}}, {"korea-stock-mcp": record}, ROOT / "servers.toml",
           tmp_path / "work", tmp_path)
    md = (tmp_path / "RESULTS.md").read_text()
    assert "korea-stock-mcp" in md and "출처를 확인하지 못한 관찰" in md  # 소스 트리가 없으면 출처 미확인
    assert "P4" in (tmp_path / "findings" / "korea-stock-mcp.md").read_text()
    assert not (tmp_path / "upstream-drafts" / "korea-stock-mcp.md").exists()  # 서버 코드 관찰만 초안


def test_redact_tree_replaces_home_path(tmp_path):
    from kmcpqa.report import redact_tree

    (tmp_path / "a.jsonl").write_text('{"line": "/Users/me/.local/x"}')
    (tmp_path / "b.png").write_bytes(b"/Users/me")
    assert redact_tree(tmp_path, "/Users/me") == 1
    assert (tmp_path / "a.jsonl").read_text() == '{"line": "~/.local/x"}'
