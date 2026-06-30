# Instrukcje dla agenta AI (GitHub Copilot)

To repozytorium zawiera **System rejestracji wizyt w placówce medycznej** —
prostą aplikację webową w Pythonie. Pełny opis działania i funkcjonalności
znajduje się w [README.md](../README.md) i jest źródłem prawdy przy
wprowadzaniu zmian w kodzie.

## Zasady pracy

- Backend korzysta wyłącznie z biblioteki standardowej (`http.server`,
  `sqlite3`) — nie dodawaj zewnętrznych zależności do działania aplikacji.
- Trzymaj kod zgodny z linterem i formaterem **ruff** (`ruff check`,
  `ruff format`).
- Każdą zmianę pokryj lub zaktualizuj testy w katalogu `test/` (pytest).
- Pracuj na osobnych gałęziach i przez pull requesty, nie bezpośrednio na `main`.
- Commit messages pisz krótko i z małej litery (np. `add ...`, `fix ...`).

## Struktura

- `main.py` — punkt wejścia (uruchamia serwer)
- `backend/` — serwer http, baza sqlite, logika api
- `frontend/` — interfejs webowy (html, css, js)
- `test/` — testy pytest
- `scripts/` — skrypty pomocnicze (run, test, lint, format)

## Polecenia

- Uruchomienie: `python main.py`
- Testy: `python -m pytest`
- Lint: `ruff check .`
- Format: `ruff format .`
