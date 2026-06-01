#!/usr/bin/env python3
"""Standalone no-provider EchoMedia Ad Studio HTTP API.

This host exposes the framework-neutral EMAS route handlers over HTTP without
introducing FastAPI or provider dependencies. It is intended for dashboard wiring,
local demos, and CI-safe integration tests.
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from services.emas import route_emas

ROOT = Path(__file__).resolve().parents[1]
EMAS_ROOT = Path(os.environ.get("EMAS_ROOT", ROOT))


class EmasHandler(BaseHTTPRequestHandler):
    def _json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("content-length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _send(self, status: int, body: dict[str, Any]) -> None:
        raw = json.dumps(body, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, {"status": "ok", "service": "emas", "noProviderMode": True})
            return
        result = route_emas("GET", self.path, {}, root_path=str(EMAS_ROOT))
        self._send(result.status, result.body)

    def do_POST(self) -> None:  # noqa: N802
        result = route_emas("POST", self.path, self._json_body(), root_path=str(EMAS_ROOT))
        self._send(result.status, result.body)

    def log_message(self, format: str, *args: Any) -> None:
        if os.environ.get("EMAS_LOG_LEVEL", "info") == "debug":
            super().log_message(format, *args)


def run_server() -> None:
    host = os.environ.get("EMAS_API_HOST", "127.0.0.1")
    port = int(os.environ.get("EMAS_API_PORT", "8081"))
    server = ThreadingHTTPServer((host, port), EmasHandler)
    print(f"EMAS API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
