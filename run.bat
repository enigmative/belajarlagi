@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [BelajarLagi] Membuat virtual environment...
    python -m venv .venv
)

echo [BelajarLagi] Menginstall dependensi...
".venv\Scripts\python.exe" -m pip install -r requirements.txt >nul

echo [BelajarLagi] Inisialisasi database...
".venv\Scripts\python.exe" scripts\seed.py

echo [BelajarLagi] Membuka browser...
start "" http://127.0.0.1:8000

echo [BelajarLagi] Menjalankan server di http://127.0.0.1:8000  (Ctrl+C untuk berhenti)
".venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
