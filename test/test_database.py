"""Testy warstwy bazy danych."""

import pytest

from backend import database


@pytest.fixture()
def conn():
    connection = database.connect(":memory:")
    database.init_db(connection)
    yield connection
    connection.close()


def test_init_seeds_doctors(conn):
    doctors = database.list_doctors(conn)
    assert len(doctors) >= 1


def test_add_and_list_visit(conn):
    doctor_id = database.list_doctors(conn)[0]["id"]
    visit_id = database.add_visit(
        conn, "Jan Testowy", doctor_id, "2026-07-01T10:00:00"
    )
    visits = database.list_visits(conn)
    assert len(visits) == 1
    assert visits[0]["id"] == visit_id
    assert visits[0]["patient_name"] == "Jan Testowy"
    assert visits[0]["status"] == "booked"


def test_add_visit_requires_patient_name(conn):
    doctor_id = database.list_doctors(conn)[0]["id"]
    with pytest.raises(ValueError):
        database.add_visit(conn, "  ", doctor_id, "2026-07-01T10:00:00")


def test_add_visit_rejects_unknown_doctor(conn):
    with pytest.raises(ValueError):
        database.add_visit(conn, "Jan", 9999, "2026-07-01T10:00:00")


def test_cancel_visit(conn):
    doctor_id = database.list_doctors(conn)[0]["id"]
    visit_id = database.add_visit(
        conn, "Jan Testowy", doctor_id, "2026-07-01T10:00:00"
    )
    assert database.cancel_visit(conn, visit_id) is True
    assert database.list_visits(conn)[0]["status"] == "cancelled"
    # Druga próba odwołania tej samej wizyty zwraca False.
    assert database.cancel_visit(conn, visit_id) is False
