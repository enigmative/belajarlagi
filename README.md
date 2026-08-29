# Belajar Lagi

Personal programming academy — local learning platform untuk membangun kembali kemampuan programming manual.

## What is Belajar Lagi?

Platform belajar programming pribadi yang berjalan lokal di komputer kamu. Tujuannya bukan sekadar menampilkan materi, tapi membangun sistem latihan yang mendorong `pahami → pikirkan → tulis sendiri → uji → debug → ulangi`, mengurangi ketergantungan terhadap AI.

## Why it exists

Kamu adalah fresh graduate S.Kom yang bekerja sebagai Fullstack Developer (PHP/CodeIgniter/Laravel). Terlalu sering memakai AI membuat kemampuan reasoning, debugging, dan problem solving menurun. Platform ini dirancang agar AI membantu **belajar**, bukan **menggantikan berpikir**.

## Stack

- Backend: Python + FastAPI
- Database: SQLite
- Frontend: HTML + CSS + Vanilla JavaScript (Tanpa React/Vue)
- Konten: Markdown

## Install & Run

Prasyarat: Python 3.11+.

Di Windows, cukup jalankan:

```
run.bat
```

Script akan otomatis: membuat venv → install dependencies → seed database → membuka browser → menjalankan server di `http://127.0.0.1:8000`.

Secara manual:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\seed.py
uvicorn app.main:app --reload
```

## Run tests

```bash
.venv\Scripts\python.exe -m pytest -q
```

## Project structure

```text
BelajarLagi/
├── belajar.txt            # kurikulum utama (WAJIB dibaca, jangan dihapus)
├── roadmap.md, progress.md
├── app/
│   ├── main.py            # FastAPI entry
│   ├── api/routes/        # endpoint API
│   ├── services/          # db, content, runner, challenges
│   ├── data/              # definisi challenge (solusi tersembunyi di sini)
├── database/schema.sql    # skema SQLite
├── content/               # materi markdown
├── frontend/              # SPA (index.html, css, js)
├── scripts/seed.py        # inisialisasi database
├── tests/                 # pytest
└── run.bat
```

## How learning works

Setiap lesson membawa kamu melalui: Objective → Theory → Analogy → Example → Code → Explanation → Common Mistakes → Manual Exercises → Challenge → Reflection → Checklist.

Materi dikembangkan bertahap dari `belajar.txt`. Tersedia Day 01–28: Python Fundamentals (materi dasar → set & tuple), Python Intermediate (exception, file, module, OOP, typing, decorator, generator, context manager), Python Problem Solving (Big-O, searching, sorting, data structures), Python Software Engineering (pytest, Git, debugging), Python Backend (HTTP & REST, FastAPI, project Employee API).

## How challenges work

1. Klik **Start Challenge** di halaman `/challenges`.
2. Pikirkan dan tulis fungsi `solve(...)` sendiri.
3. Tekan **Run & Test**. Sistem menjalankan kode di sandbox isolasi (timeout, temp dir, tanpa network) lalu mengetes **hidden test case**.
4. Lihat hasil pass/fail + expected vs received.
5. Gunakan **Hint 1 / Hint 2** jika buntu — solusi penuh **tidak** ditampilkan di frontend.

## How progress works

Progress tersimpan di SQLite (tidak hanya checkbox frontend). Database mencatat:
- `lessons` + `lesson_progress` (status + `completed_at`)
- `challenges` + `challenge_attempts` (result, time, hints, attempt number)
- `learning_sessions` (untuk streak & total waktu belajar)
- `notes`, `mistakes`, `projects`, `project_tasks`

Semua statistik di dashboard/progress **berasal dari data nyata** — mulai dari 0%, bukan data palsu.

## Security (code runner)

- Eksekusi Python lewat `subprocess` dengan mode isolasi `-I` di temporary directory.
- Timeout 5 detik, limit output, tanpa `shell=True`, tanpa arbitrary shell command.
- Challenge solution & hidden tests disimpan di backend, bukan frontend.
- `eval()` tidak digunakan untuk menjalankan kode user.
- Untuk sandbox penuh (Docker) akan menyusul di tahap lanjut.

## Fitur

Dashboard, Roadmap, Lessons, Challenges, Python Playground, Projects, Notes, Mistake Journal, Progress, Weekly Review, Search (Ctrl+K), Dark Mode.

Shorcut: `Ctrl+K` = search, `Ctrl+Enter` = run code.

## AI Usage Policy

```
TRY FIRST.
THINK BEFORE ASKING AI.
USE AI TO LEARN, NOT TO AVOID THINKING.
```
