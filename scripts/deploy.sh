#!/usr/bin/env bash
# Manual deploy helper. Equivalent to the GitHub Actions workflow, but run by hand.
# Usage: bash scripts/deploy.sh
set -euo pipefail

APP_DIR=/mount/hdd/belajar-lagi
cd "$APP_DIR"

echo "[deploy] backup database"
.venv/bin/python scripts/backup_db.py

echo "[deploy] pull code"
git pull origin main

echo "[deploy] install dependencies"
.venv/bin/pip install -r requirements.txt

echo "[deploy] pull docker image"
docker pull python:3.11-slim || true

echo "[deploy] restart app"
sudo systemctl restart belajar-lagi

echo "[deploy] health check"
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/api/courses || true)
  if [ "$code" = "200" ]; then
    echo "[deploy] healthy (200)"
    exit 0
  fi
  sleep 2
done
echo "[deploy] health check FAILED"; exit 1
