#!/usr/bin/env bash
# sprawdzenie kodu linterem
cd "$(dirname "$0")/.." || exit 1
ruff check .
