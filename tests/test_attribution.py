"""출처 가리기(서버 코드 / SDK 기본 동작)와 분류 규칙. 합성 소스 트리를 만들어 확인한다."""

from pathlib import Path

from kmcpqa.attribution import from_stderr, from_text
from kmcpqa.defects import findings, group_causes


def make_tree(root: Path) -> Path:
    (root / "src").mkdir(parents=True)
    (root / "src" / "registry.ts").write_text(
        "// Unknown tool: comment lines are ignored\n"
        "return { content: [{ type: 'text', text: `Unknown tool: ${name}` }], isError: true }\n")
    (root / "src" / "client.ts").write_text("throw new Error(`DART ${path} → 비-ZIP 응답 (${n}B)`);\n")
    sdk = root / "node_modules" / "@modelcontextprotocol" / "sdk" / "dist" / "esm" / "server"
    sdk.mkdir(parents=True)
    (sdk / "mcp.js").write_text("x\nthrow new McpError(ErrorCode.InvalidParams, `Tool ${request.params.name} "
                                "not found`);\n")
    py = root / ".venv" / "lib" / "python3.12" / "site-packages" / "mcp" / "shared"
    py.mkdir(parents=True)
    (py / "session.py").write_text("code=INVALID_PARAMS,\nmessage=\"Invalid request parameters\",\n")
    return root


def test_server_code_wins_and_comments_are_skipped(tmp_path):
    root = make_tree(tmp_path)
    a = from_text("Unknown tool: kmcpqa_no_such_tool", ["kmcpqa_no_such_tool"], root)
    assert a["origin"] == "server" and a["where"] == ["src/registry.ts:2"]


def test_sdk_template_is_found(tmp_path):
    root = make_tree(tmp_path)
    a = from_text("MCP error -32602: Tool kmcpqa_no_such_tool not found", ["kmcpqa_no_such_tool"], root)
    assert a["origin"] == "sdk"
    assert a["where"] == ["node_modules/@modelcontextprotocol/sdk/dist/esm/server/mcp.js:2"]
    b = from_text("Invalid request parameters", [], root)
    assert b["origin"] == "sdk" and b["where"][0].endswith("mcp/shared/session.py:2")


def test_message_fragment_with_dynamic_parts(tmp_path):
    root = make_tree(tmp_path)
    a = from_text("DART corpCode.xml → 비-ZIP 응답 (150B): <?xml", [], root)
    assert a["origin"] == "server" and a["where"] == ["src/client.ts:1"]


def test_unknown_when_not_found(tmp_path):
    root = make_tree(tmp_path)
    assert from_text("completely different words here", [], root)["origin"] == "unknown"


def test_stderr_frames_in_sdk(tmp_path):
    root = make_tree(tmp_path)
    lines = [f'  File "{root}/.venv/lib/python3.12/site-packages/mcp/shared/session.py", line 307, '
             "in _receive_loop", "pydantic_core.ValidationError: 1 validation error"]
    a = from_stderr(lines, root)
    assert a["origin"] == "sdk" and a["where"] == [".venv/lib/python3.12/site-packages/mcp/shared/session.py:307"]
    js = [f"    at DartClient.getZip (file://{root}/build/lib/dart-client.js:49:15)"]
    assert from_stderr(js, root)["origin"] == "server"


def _record(tools: list[dict], **probe) -> dict:
    base = {"initialize": {"outcome": "result", "spec_violations": []}, "tools_list": {"count": len(tools)},
            "unknown_method": {"outcome": "error", "error_code": -32601, "responsive_after": True},
            "unknown_tool": {"outcome": "error", "error_code": -32602, "responsive_after": True},
            "idle_alive": True, "tools": tools}
    return {"install": {"ok": True}, "probe": base | probe}


def test_empty_properties_runtime_requirement_is_s4_not_r3():
    tool = {"name": "get_indicator", "required": [], "properties": [],
            "probes": {"valid": {"outcome": "tool_error", "text_excerpt": "Required at indicatorId",
                                 "args": {}, "responsive_after": True}}}
    codes = [f["code"] for f in findings(_record([tool]))]
    assert codes == ["S4"]


def test_parse_error_on_synthesized_input_is_e3_not_e1():
    tool = {"name": "batch", "required": ["items"], "properties": ["items"],
            "probes": {"valid": {"outcome": "ok", "text_excerpt": '{"error": "JSON 파싱 오류"}',
                                 "error_marker": "오류", "auth_marker": None, "args": {"items": "test"},
                                 "responsive_after": True}}}
    assert [f["code"] for f in findings(_record([tool]))] == ["E3"]


def test_same_message_on_many_tools_is_one_cause():
    msg = "DART corpCode.xml → 비-ZIP 응답 (150B)"
    tools = [{"name": f"t{i}", "required": ["q"], "properties": ["q"],
              "probes": {"missing_required": {"outcome": "error", "error_code": -32603, "error_message": msg,
                                              "args": {}, "responsive_after": True},
                         "valid": {"outcome": "error", "error_code": -32603, "error_message": msg,
                                   "args": {"q": f"x{i}"}, "responsive_after": True}}} for i in range(22)]
    fs = findings(_record(tools))
    assert len(fs) == 44
    groups = group_causes(fs)
    assert len(groups) == 1 and groups[0]["count"] == 44
