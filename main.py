"""Punkt wejścia aplikacji: uruchamia serwer rejestracji wizyt."""

from __future__ import annotations

import argparse

from backend.server import create_server

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_DB = "appointments.db"


def parse_args(argv=None) -> argparse.Namespace:
    """Parsuje argumenty wiersza poleceń (host, port, ścieżka bazy)."""
    parser = argparse.ArgumentParser(
        description="System rejestracji wizyt w placówce medycznej."
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Adres nasłuchu serwera."
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port nasłuchu."
    )
    parser.add_argument(
        "--db", default=DEFAULT_DB, help="Ścieżka do pliku bazy SQLite."
    )
    return parser.parse_args(argv)


def main(argv=None) -> None:
    """Uruchamia serwer i obsługuje zatrzymanie przez Ctrl+C."""
    args = parse_args(argv)
    httpd = create_server(args.host, args.port, args.db)
    print(
        f"Serwer działa na http://{args.host}:{args.port} "
        "(Ctrl+C kończy)."
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nZatrzymywanie serwera...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
