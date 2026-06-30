#!/usr/bin/env bash
# uruchomienie testow
cd "$(dirname "$0")/.." || exit 1
python -m pytest
