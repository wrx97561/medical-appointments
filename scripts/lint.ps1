# sprawdzenie kodu linterem
Set-Location (Join-Path $PSScriptRoot "..")
ruff check .
