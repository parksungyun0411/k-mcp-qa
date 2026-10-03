"""테스트용 stdio MCP 서버 (SYNTHETIC). 표준 라이브러리만 쓴다.

    python fixture_server.py good   # 스펙대로 동작
    python fixture_server.py bad    # 관찰 유형을 일부러 재현
    python fixture_server.py skew   # NTS 조회 결과의 사업자번호를 바꿔 돌려줌 (불일치 재현)

status 툴은 FIXTURE_NTS_BASE 의 가짜 업스트림을 부른다.
"""

import json
import os
import sys
import urllib.request

MODE = sys.argv[1] if len(sys.argv) > 1 else "good"

TOOLS = [
    {"name": "lookup", "description": "echo", "inputSchema": {
        "type": "object", "properties": {"q": {"type": "string"}}, "required": ["q"]},
     "outputSchema": {"type": "object", "properties": {"value": {"type": "string"}},
                      "required": ["value"]}},
    {"name": "status", "description": "NTS status via fake upstream", "inputSchema": {
        "type": "object", "properties": {"b_no": {"type": "string"}}, "required": ["b_no"]}},
]
if MODE == "bad":
    TOOLS += [
        {"name": "broken_schema", "description": "", "inputSchema": {
            "type": "object", "properties": {"a": {"type": "string"}}, "required": ["missing_prop"]}},
        {"name": "hang", "description": "", "inputSchema": {"type": "object", "properties": {}}},
        {"name": "internal", "description": "", "inputSchema": {
            "type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]}},
    ]


def send(msg):
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def result(mid, res):
    send({"jsonrpc": "2.0", "id": mid, "result": res})


def error(mid, code, message):
    send({"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}})


def text(t, is_error=False, structured=None):
    r = {"content": [{"type": "text", "text": t}]}
    if is_error:
        r["isError"] = True
    if structured is not None:
        r["structuredContent"] = structured
    return r


def nts(b_no):
    base = os.environ["FIXTURE_NTS_BASE"]
    req = urllib.request.Request(f"{base}/status?serviceKey=x&returnType=JSON",
                                 data=json.dumps({"b_no": [b_no]}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["data"][0]


def call(mid, name, args):
    if name == "lookup":
        if "q" not in args or not isinstance(args.get("q"), str):
            if MODE == "bad":
                return result(mid, text("validation error: q Field required"))
            return result(mid, text("q must be a string", is_error=True))
        if MODE == "bad":
            return result(mid, text("ERROR: SERVICE_KEY_IS_NOT_REGISTERED_ERROR"))
        return result(mid, text(args["q"], structured={"value": args["q"]}))
    if name == "status":
        if not isinstance(args.get("b_no"), str):
            return result(mid, text("b_no must be a string", is_error=True))
        try:
            row = nts(args["b_no"])
        except OSError as e:
            return result(mid, text(f"upstream unavailable: {e}", is_error=True))
        if MODE == "skew":
            row["b_no"] = "9999999999"
        return result(mid, text(json.dumps(row, ensure_ascii=False)))
    if MODE == "bad" and name == "broken_schema":
        return result(mid, text("ok"))
    if MODE == "bad" and name == "hang":
        return None
    if MODE == "bad" and name == "internal":
        return error(mid, -32603, "Traceback (most recent call last): boom")
    if MODE == "bad":
        return result(mid, text(f"Unknown tool: {name}", is_error=True))
    return error(mid, -32602, f"Unknown tool: {name}")


def main():
    if MODE == "bad":
        print("fixture server starting (log line on stdout)", flush=True)
    for line in sys.stdin:
        msg = json.loads(line)
        mid, method = msg.get("id"), msg.get("method")
        if mid is None:
            continue
        if method == "initialize":
            result(mid, {"protocolVersion": "2025-11-25", "capabilities": {"tools": {}},
                         "serverInfo": {"name": f"fixture-{MODE}", "version": "0"}})
        elif method == "ping":
            result(mid, {})
        elif method == "tools/list":
            result(mid, {"tools": TOOLS})
        elif method == "tools/call":
            p = msg.get("params") or {}
            call(mid, p.get("name"), p.get("arguments") or {})
        elif MODE == "bad":
            sys.exit(1)
        else:
            error(mid, -32601, f"Method not found: {method}")


if __name__ == "__main__":
    main()
