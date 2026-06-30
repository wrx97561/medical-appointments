"""Warstwa dostępu do bazy danych (SQLite) dla systemu rejestracji wizyt."""

from __future__ import annotations

import sqlite3
from datetime import datetime

# Lekarze, którymi wypełniamy pustą bazę przy pierwszym uruchomieniu.
DEFAULT_DOCTORS = [
    ("Anna Kowalska", "Internista"),
    ("Piotr Nowak", "Kardiolog"),
    ("Maria Wiśniewska", "Pediatra"),
    ("Tomasz Lewandowski", "Dermatolog"),
]


def connect(db_path: str) -> sqlite3.Connection:
    """Otwiera połączenie z bazą i zwraca wiersze jako sqlite3.Row."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Tworzy tabele (jeśli nie istnieją) i dodaje domyślnych lekarzy."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS doctors (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            specialty TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS visits (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_id    INTEGER NOT NULL REFERENCES doctors(id),
            visit_date   TEXT NOT NULL,
            status       TEXT NOT NULL DEFAULT 'booked',
            created_at   TEXT NOT NULL
        );
        """
    )
    _seed_doctors(conn)
    conn.commit()


def _seed_doctors(conn: sqlite3.Connection) -> None:
    count = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO doctors (name, specialty) VALUES (?, ?)",
            DEFAULT_DOCTORS,
        )


def list_doctors(conn: sqlite3.Connection) -> list[dict]:
    """Zwraca listę wszystkich lekarzy."""
    rows = conn.execute(
        "SELECT id, name, specialty FROM doctors ORDER BY name"
    ).fetchall()
    return [dict(row) for row in rows]


def list_visits(conn: sqlite3.Connection) -> list[dict]:
    """Zwraca listę wizyt wraz z nazwą i specjalizacją lekarza."""
    rows = conn.execute(
        """
        SELECT v.id, v.patient_name, v.visit_date, v.status,
               d.name AS doctor_name, d.specialty AS doctor_specialty
        FROM visits v
        JOIN doctors d ON d.id = v.doctor_id
        ORDER BY v.visit_date
        """
    ).fetchall()
    return [dict(row) for row in rows]


def add_visit(
    conn: sqlite3.Connection,
    patient_name: str,
    doctor_id: int,
    visit_date: str,
) -> int:
    """Dodaje nową wizytę po walidacji danych. Zwraca id utworzonej wizyty."""
    patient_name = (patient_name or "").strip()
    if not patient_name:
        raise ValueError("Imię i nazwisko pacjenta jest wymagane.")

    if not _doctor_exists(conn, doctor_id):
        raise ValueError("Wybrany lekarz nie istnieje.")

    if not _is_valid_datetime(visit_date):
        raise ValueError("Nieprawidłowy format daty wizyty.")

    now = datetime.now().isoformat(timespec="seconds")
    cursor = conn.execute(
        """
        INSERT INTO visits (patient_name, doctor_id, visit_date, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (patient_name, doctor_id, visit_date, now),
    )
    conn.commit()
    return int(cursor.lastrowid)


def cancel_visit(conn: sqlite3.Connection, visit_id: int) -> bool:
    """Oznacza wizytę jako odwołaną. Zwraca True, jeśli wizyta istniała."""
    cursor = conn.execute(
        "UPDATE visits SET status = 'cancelled' WHERE id = ? AND status != 'cancelled'",
        (visit_id,),
    )
    conn.commit()
    return cursor.rowcount > 0


def _doctor_exists(conn: sqlite3.Connection, doctor_id: int) -> bool:
    row = conn.execute("SELECT 1 FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
    return row is not None


def _is_valid_datetime(value: str) -> bool:
    try:
        datetime.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False
