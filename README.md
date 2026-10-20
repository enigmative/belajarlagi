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
- Aset UI: lokal (font, CSS, dan Feather icons ikut tersimpan di repo; tidak butuh CDN)

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

Test memakai database sementara lewat environment variable `BELAJAR_LAGI_DB`, jadi `learning.db` milikmu tidak tersentuh. Untuk mengarahkan aplikasi ke database lain secara manual:

```powershell
$env:BELAJAR_LAGI_DB = "C:\path\ke\database.db"
```

## Project structure

```text
BelajarLagi/
├── belajar.txt            # kurikulum utama (WAJIB dibaca, jangan dihapus)
├── roadmap.md, progress.md
├── app/
│   ├── main.py            # FastAPI entry
│   ├── api/routes/        # endpoint API (termasuk courses.py)
│   ├── services/          # db, content, runner, challenges
│   ├── data/              # definisi challenge & katalog kursus (courses_def.py)
├── database/schema.sql    # skema SQLite
├── content/               # materi markdown
├── frontend/              # SPA (index.html, css, js)
│   └── js/vendor/         # Feather icons (lokal)
├── scripts/seed.py        # inisialisasi database + mapping course/module/lesson
├── tests/                 # pytest (memakai database sementara)
└── run.bat
```

> **UI:** antarmuka memakai tema editorial lokal. CSS, font, dan Feather icons dimuat dari folder `frontend/`; tidak ada dependency CDN. Logika SPA (router, halaman, aksi) ada di `frontend/js/app.js`.

## How learning works

Belajar diorganisasi per **kelas**, seperti course platform: **Course → Module → Lesson**. Setiap lesson tetap membawa kamu melalui: Objective → Theory → Analogy → Example → Code → Explanation → Common Mistakes → Manual Exercises → Challenge → Reflection → Checklist.

Materi dikembangkan bertahap dari `belajar.txt`. Tersedia **19 kelas** dan **68 lesson**:

- **Python Fundamentals** (9): dasar Python + struktur data.
- **Python Intermediate** (9): error/file/module, OOP/typing, decorator/generator/context manager.
- **Python Problem Solving** (4): kompleksitas, searching, sorting, struktur data.
- **Python Engineering** (3): testing, Git, debugging.
- **Python Backend & FastAPI** (3): HTTP/REST, FastAPI, project API.
- **SQL for Developers** (5): CRUD, JOIN, desain, transaksi, optimasi.
- **PHP Fundamentals** (4): dasar, function/array, OOP, Composer/PSR/SOLID.
- **CodeIgniter** (3): MVC/routing, model/DB, auth/filter/REST.
- **Laravel** (3): dasar, Eloquent, fitur produksi.
- **JavaScript** (4): dasar, DOM, async/fetch, framework.
- **Web Security** (3), **Docker** (2), **Linux** (3), **Redis & Queue** (2), **CI/CD** (2), **Software Architecture** (2), **System Design** (2), **Observability** (2).
- **Interview Prep** (3): sprint Java/Spring Boot, JavaScript/React, live coding.

Halaman **Kelas** menampilkan katalog dan filter kategori. Halaman detail kelas berisi modul, daftar materi, progres, dan tombol mulai/lanjut. Progres dihitung per kelas; **Kelas Saya** menampilkan kelas yang sudah dimulai.

## How challenges work

1. Klik **Start Challenge** di halaman `/challenges`.
2. Pikirkan dan tulis fungsi `solve(...)` sendiri.
3. Tekan **Run & Test**. Sistem menjalankan kode lewat runner lokal dengan timeout, temp dir, dan `-I`, lalu mengetes **hidden test case**.
4. Lihat hasil pass/fail + expected vs received.
5. Gunakan **Hint 1 / Hint 2** jika buntu — solusi penuh **tidak** ditampilkan di frontend.

## How progress works

Progress tersimpan di SQLite (tidak hanya checkbox frontend). Database mencatat:
- `courses` → `course_modules` → `course_lessons` (katalog dan urutan materi)
- `course_enrollments` (kelas yang diikuti/dimulai)
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

Dashboard, **Kelas** (katalog + detail + modul), **Kelas Saya**, lesson dengan outline kelas, Roadmap, Challenges, Python Playground, Projects, Notes, Mistake Journal, Progress per kelas, Weekly Review, Search (Ctrl+K), Dark Mode.

Shorcut: `Ctrl+K` = search, `Ctrl+Enter` = run code.

## AI Usage Policy

```
TRY FIRST.
THINK BEFORE ASKING AI.
USE AI TO LEARN, NOT TO AVOID THINKING.
```
