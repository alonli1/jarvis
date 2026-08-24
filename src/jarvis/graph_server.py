from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .graph_view import render_graph_html
from .literature_graph import build_graph


def graph_response(root: Path, route: str) -> tuple[int, str, bytes]:
    if route == "/health":
        return 200, "application/json; charset=utf-8", b'{"status":"ok"}\n'
    graph = build_graph(root, manuscript_neighbors=75)
    if route == "/api/graph":
        body = (json.dumps(graph, separators=(",", ":")) + "\n").encode()
        return 200, "application/json; charset=utf-8", body
    if route == "/":
        origin = next(
            (node for node in graph["nodes"] if node["kind"] == "manuscript"),
            graph["nodes"][0] if graph["nodes"] else None,
        )
        if origin is None:
            return 503, "text/plain; charset=utf-8", b"No graph nodes; add references first\n"
        body = render_graph_html(
            graph, origin, limit=len(graph["nodes"]), full_graph=True
        ).encode()
        return 200, "text/html; charset=utf-8", body
    return 404, "text/plain; charset=utf-8", b"Not found\n"


def create_graph_server(
    root: Path, host: str = "127.0.0.1", port: int = 8765
) -> ThreadingHTTPServer:
    class GraphHandler(BaseHTTPRequestHandler):
        server_version = "JarvisGraph/1.0"

        def _send(self, body: bytes, content_type: str) -> None:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; style-src 'unsafe-inline'; "
                "script-src 'unsafe-inline'; connect-src 'self'; img-src data:",
            )
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            route = urlsplit(self.path).path
            status, content_type, body = graph_response(root, route)
            if status != 200:
                self.send_error(status, body.decode().strip())
                return
            self._send(body, content_type)

        def log_message(self, format: str, *args: object) -> None:
            return

    return ThreadingHTTPServer((host, port), GraphHandler)
