"""Logika API — czysta, niezależna od warstwy HTTP (łatwa do testowania)."""

from __future__ import annotations

import re
import sqlite3
from typing import Any

from backend import database

_VISIT_ID_RE = re.compile(r"^/api/visits/(\d+)$")


def handle_api(
    method: str,
    path: str,
    payload: dict[str, Any] | None,
    conn: sqlite3.Connection,
) -> tuple[int, dict]:
    """Rozdziela żądanie API na właściwą operację.

    Zwraca krotkę (kod_http, dane_odpowiedzi).
    """
    if method == "GET" and path == "/api/doctors":
        return 200, {"doctors": database.list_doctors(conn)}

    if method == "GET" and path == "/api/visits":
        return 200, {"visits": database.list_visits(conn)}

    if method == "POST" and path == "/api/visits":
        return _create_visit(conn, payload or {})

    match = _VISIT_ID_RE.match(path)
    if method == "DELETE" and match:
        return _cancel_visit(conn, int(match.group(1)))

    return 404, {"error": "Nie znaleziono zasobu."}


def _create_visit(conn: sqlite3.Connection, payload: dict) -> tuple[int, dict]:
    try:
        visit_id = database.add_visit(
            conn,
            patient_name=payload.get("patient_name", ""),
            doctor_id=payload.get("doctor_id"),
            visit_date=payload.get("visit_date", ""),
        )
    except ValueError as exc:
        return 400, {"error": str(exc)}
    return 201, {"id": visit_id}


def _cancel_visit(conn: sqlite3.Connection, visit_id: int) -> tuple[int, dict]:
    if database.cancel_visit(conn, visit_id):
        return 200, {"status": "cancelled"}
    return 404, {"error": "Wizyta nie istnieje lub jest już odwołana."}
