#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/pip install --quiet -r requirements.txt
.venv/bin/python seed.py

echo
echo "Gotowe. Uruchom aplikację:  .venv/bin/python run.py"
echo "Uruchom testy:              .venv/bin/python -m pytest"
