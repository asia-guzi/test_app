#!/bin/sh
set -e

if [ ! -f "/test_app/data/.initialized" ]; then
  echo "Initiate initial_populate..."
  python3 app/initial_populate/initial.py
  touch /test_app/data/.initialized
else
  echo "Db prepared, starting server..."
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
