"""Testy logiki API (bez warstwy HTTP)."""

from datetime import datetime, timedelta

import pytest

from backend import api, database

FUTURE = (datetime.now() + timedelta(days=1)).isoformat(timespec="seconds")
PAST = (datetime.now() - timedelta(days=1)).isoformat(timespec="seconds")


@pytest.fixture()
def conn():
    connection = database.connect(":memory:")
    database.init_db(connection)
    yield connection
    connection.close()


def test_get_doctors(conn):
    status, body = api.handle_api("GET", "/api/doctors", None, conn)
    assert status == 200
    assert "doctors" in body


def test_create_visit(conn):
    doctor_id = database.list_doctors(conn)[0]["id"]
    payload = {
        "patient_name": "Anna Test",
        "doctor_id": doctor_id,
        "visit_date": FUTURE,
    }
    status, body = api.handle_api("POST", "/api/visits", payload, conn)
    assert status == 201
    assert "id" in body


def test_create_visit_validation_error(conn):
    payload = {"patient_name": "", "doctor_id": 1, "visit_date": "x"}
    status, body = api.handle_api("POST", "/api/visits", payload, conn)
    assert status == 400
    assert "error" in body


def test_create_visit_in_past_returns_400(conn):
    doctor_id = database.list_doctors(conn)[0]["id"]
    payload = {
        "patient_name": "Anna Test",
        "doctor_id": doctor_id,
        "visit_date": PAST,
    }
    status, body = api.handle_api("POST", "/api/visits", payload, conn)
    assert status == 400
    assert "error" in body


def test_cancel_missing_visit(conn):
    status, body = api.handle_api("DELETE", "/api/visits/999", None, conn)
    assert status == 404


def test_unknown_route(conn):
    status, body = api.handle_api("GET", "/api/unknown", None, conn)
    assert status == 404
