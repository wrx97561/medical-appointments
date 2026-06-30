"""Serwer HTTP oparty o bibliotekę standardową (http.server)."""

from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from backend import api, database

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")


class AppRequestHandler(BaseHTTPRequestHandler):
    """Obsługuje żądania: API pod /api/*, resztę jako pliki frontendu."""

    server_version = "MedicalAppointments/1.0"

    def do_GET(self) -> None:
        if self.path.startswith("/api/"):
            self._handle_api("GET")
        else:
            self._serve_static()

    def do_POST(self) -> None:
        self._handle_api("POST")

    def do_DELETE(self) -> None:
        self._handle_api("DELETE")

    def _handle_api(self, method: str) -> None:
        payload = self._read_json_body()
        conn = database.connect(self.server.db_path)
        try:
            status, body = api.handle_api(method, self.path, payload, conn)
        finally:
            conn.close()
        self._send_json(status, body)

    def _read_json_body(self) -> dict | None:
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def _serve_static(self) -> None:
        rel_path = "index.html" if self.path == "/" else self.path.lstrip("/")
        file_path = os.path.normpath(os.path.join(FRONTEND_DIR, rel_path))

        # Ochrona przed wyjściem poza katalog frontendu (path traversal).
        if not file_path.startswith(FRONTEND_DIR):
            self._send_json(403, {"error": "Brak dostępu."})
            return

        if not os.path.isfile(file_path):
            self._send_json(404, {"error": "Nie znaleziono pliku."})
            return

        content_type, _ = mimetypes.guess_type(file_path)
        with open(file_path, "rb") as handle:
            data = handle.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, status: int, body: dict) -> None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt: str, *args) -> None:
        # Zwięzły log: jedna linia na żądanie.
        print(f"{self.address_string()} - {fmt % args}")


def create_server(host: str, port: int, db_path: str) -> ThreadingHTTPServer:
    """Tworzy serwer, inicjalizuje bazę i zwraca gotowy obiekt serwera."""
    conn = database.connect(db_path)
    try:
        database.init_db(conn)
    finally:
        conn.close()

    httpd = ThreadingHTTPServer((host, port), AppRequestHandler)
    httpd.db_path = db_path
    return httpd
