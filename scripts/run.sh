#!/usr/bin/env bash
# uruchomienie aplikacji
cd "$(dirname "$0")/.." || exit 1
python main.py "$@"
