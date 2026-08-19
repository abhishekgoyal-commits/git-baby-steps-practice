"""Minimal stdio MCP server that exposes a structured echo tool."""

from __future__ import annotations

import json
import sys
from typing import Any, Dict


SERVER_INFO = {
    "name": "hello-genai-echo",
    "version": "1.0.0",
}


def send_message(message: Dict[str, Any]) -> None:
    """Write one MCP JSON-RPC message using Content-Length framing."""
    body = json.dumps(message, separators=(",", ":")).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    sys.stdout.buffer.write(header + body)
    sys.stdout.buffer.flush()


def send_result(request_id: Any, result: Dict[str, Any]) -> None:
    send_message({"jsonrpc": "2.0", "id": request_id, "result": result})


def send_error(request_id: Any, code: int, message: str) -> None:
    send_message(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }
    )


def read_message() -> Dict[str, Any] | None:
    """Read one Content-Length-framed JSON-RPC message from stdin."""
    headers: Dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        name, separator, value = line.decode("ascii").partition(":")
        if separator:
            headers[name.lower().strip()] = value.strip()

    length = int(headers.get("content-length", "0"))
    if length <= 0:
        raise ValueError("MCP message is missing a valid Content-Length header")
    return json.loads(sys.stdin.buffer.read(length).decode("utf-8"))


def handle_message(message: Dict[str, Any]) -> None:
    """Handle the MCP lifecycle and echo tool requests."""
    method = message.get("method")
    request_id = message.get("id")

    if method == "initialize":
        send_result(
            request_id,
            {
                "protocolVersion": message.get("params", {}).get(
                    "protocolVersion", "2024-11-05"
                ),
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        )
    elif method == "notifications/initialized":
        return
    elif method == "tools/list":
        send_result(
            request_id,
            {
                "tools": [
                    {
                        "name": "echo_message",
                        "description": "Return the supplied message and its length.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"text": {"type": "string"}},
                            "required": ["text"],
                        },
                    }
                ]
            },
        )
    elif method == "tools/call":
        params = message.get("params", {})
        if params.get("name") != "echo_message":
            send_error(request_id, -32602, "Unknown tool")
            return
        text = params.get("arguments", {}).get("text", "")
        result = {"tool": "echo_message", "parameters": {"text": text}, "result": {"text": str(text), "length": len(str(text))}}
        send_result(
            request_id,
            {"content": [{"type": "text", "text": json.dumps(result)}]},
        )
    elif request_id is not None:
        send_error(request_id, -32601, f"Unknown method: {method}")


def main() -> None:
    while True:
        message = read_message()
        if message is None:
            return
        handle_message(message)


if __name__ == "__main__":
    main()
