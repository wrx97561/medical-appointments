# System rejestracji wizyt w placówce medycznej

Prosta aplikacja webowa w Pythonie do rejestrowania wizyt pacjentów u lekarzy.
Backend opiera się wyłącznie o bibliotekę standardową (`http.server` + `sqlite3`),
a frontend to zwykły HTML/CSS/JS. Sama aplikacja nie wymaga żadnych zewnętrznych
zależności do uruchomienia.

## Funkcjonalności

- **Lista lekarzy** — baza zawiera kilku przykładowych lekarzy (imię, specjalizacja).
- **Rezerwacja wizyty** — formularz z danymi: pacjent, lekarz, data i godzina.
- **Lista wizyt** — wszystkie zaplanowane wizyty wraz z lekarzem i terminem.
- **Odwoływanie wizyty** — zmiana statusu wizyty na „odwołana".
- **Walidacja** — wizyta wymaga nazwiska pacjenta, istniejącego lekarza i poprawnej daty.

### API

| Metoda | Ścieżka | Opis |
|--------|---------|------|
| GET | `/api/doctors` | lista lekarzy |
| GET | `/api/visits` | lista wizyt |
| POST | `/api/visits` | rezerwacja wizyty (`patient_name`, `doctor_id`, `visit_date`) |
| DELETE | `/api/visits/{id}` | odwołanie wizyty |

## Struktura projektu

```
medical-appointments/
├─ main.py               # punkt wejścia — uruchamia serwer
├─ backend/              # serwer http, baza sqlite, logika api
│  ├─ server.py
│  ├─ database.py
│  └─ api.py
├─ frontend/             # interfejs webowy (html, css, js)
├─ test/                 # testy pytest
├─ scripts/              # skrypty pomocnicze (.ps1 dla windows, .sh dla linux/ci)
├─ .github/workflows/    # konfiguracja ci (github actions)
├─ requirements-dev.txt  # zależności deweloperskie (pytest, ruff)
├─ ruff.toml             # konfiguracja lintera/formatera
└─ pytest.ini            # konfiguracja testów
```

## Wymagania

- Python 3.11 lub nowszy.
- Sama aplikacja nie ma zależności. Do testów, lintowania i formatowania
  zainstaluj zależności deweloperskie:

```
pip install -r requirements-dev.txt
```

## Uruchamianie

```
python main.py
```

Aplikacja jest dostępna pod adresem http://127.0.0.1:8000.
Opcjonalne argumenty: `--host`, `--port`, `--db` (ścieżka pliku bazy).

Skrót: `scripts/run.ps1` (Windows) lub `scripts/run.sh` (Linux/macOS).

## Testowanie

```
python -m pytest
```

Skrót: `scripts/test.ps1` lub `scripts/test.sh`.

## Lintowanie i formatowanie

Projekt używa narzędzia [ruff](https://docs.astral.sh/ruff/) jako lintera
i formatera kodu:

```
ruff check .     # lintowanie — wykrywa problemy w kodzie
ruff format .    # formatowanie — porządkuje styl kodu
```

Skróty: `scripts/lint.ps1` / `scripts/lint.sh` oraz
`scripts/format.ps1` / `scripts/format.sh`.

## CI

Przy każdym pull requeście (oraz po wypchnięciu na `main`) GitHub Actions
automatycznie instaluje zależności, uruchamia linter, sprawdza formatowanie
i odpala testy. Konfiguracja znajduje się w `.github/workflows/ci.yml`.
