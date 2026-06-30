#!/usr/bin/env bash
# formatowanie kodu
cd "$(dirname "$0")/.." || exit 1
ruff format .
