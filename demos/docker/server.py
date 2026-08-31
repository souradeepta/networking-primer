"""Local-only HTTP server for the Compose networking lab."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    """Return a deterministic health response."""

    def do_GET(self) -> None:  # noqa: N802 - stdlib callback name
        """Serve a health endpoint and reject other paths."""
        if self.path != "/health":
            self.send_error(404)
            return
        body = b"ok\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        """Keep the lab output compact."""
        print(format % args)


ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
