#!/bin/sh
set -e

# Twoje initial.py zawiera już czekanie na DB
if [ ! -f "/test_app/data/.initialized" ]; then
  echo "🚀 Uruchamiam initial_populate..."
  python3 app/initial_populate/initial.py
  touch /test_app/data/.initialized
else
  echo "✔️ Baza już zainicjalizowana, pomijam."
fi
# Uruchom FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
