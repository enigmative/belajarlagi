# Belajar Lagi

Local-first programming academy — platform belajar multi-user untuk membangun kembali kemampuan programming manual.

## What is Belajar Lagi?

Platform belajar programming yang bisa berjalan lokal atau di server. Katalog kelas dapat dilihat publik, tetapi lesson, progres, catatan, dan latihan terikat ke akun masing-masing. Tujuannya bukan sekadar menampilkan materi, tapi membangun sistem latihan yang mendorong `pahami → pikirkan → tulis sendiri → uji → debug → ulangi`, mengurangi ketergantungan terhadap AI.

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

Script akan otomatis: membuat venv → install dependencies → seed database → memastikan akun admin → membuka browser → menjalankan server di `http://127.0.0.1:8000`.

Secara manual:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\seed.py
python scripts\manage_users.py setup-admin --email admin@example.com --name Admin
uvicorn app.main:app --reload
```

> **Database lama:** `seed.py`/`init_db()` otomatis memigrasikan skema single-user ke multi-user. Data lama (lesson, progres, challenge, sesi belajar, dan checklist project) dipindahkan ke akun terkunci `owner@local`. Jalankan `python scripts/manage_users.py setup-admin --email ... --name ...` untuk mengklaim akun itu sebagai admin. Backup `learning.db` sebelum migrasi pertama.

## Akun & akses

- **Tidak ada registrasi publik.** Admin membuat akun lewat CLI.
- Katalog `/api/courses` dan detail kelas bisa diakses tanpa login.
- Lesson, dashboard, progres, notes, challenges, interview, projects, search, dan playground membutuhkan login.
- Setiap user punya progres, catatan, attempt challenge, interview progress, sesi belajar, dan checklist project sendiri.

Perintah admin:

```bash
# Buat admin pertama (atau klaim owner@local hasil migrasi)
python scripts/manage_users.py setup-admin --email admin@example.com --name "Admin"

# Buat akun siswa
python scripts/manage_users.py create --email siswa@example.com --name "Siswa"

# Reset password (semua sesi user tersebut langsung logout)
python scripts/manage_users.py reset-password --email siswa@example.com

# Aktifkan / nonaktifkan akun
python scripts/manage_users.py activate --email siswa@example.com
python scripts/manage_users.py deactivate --email siswa@example.com

# Lihat semua akun
python scripts/manage_users.py list
```

Password menggunakan `hashlib.scrypt`. Login membuat cookie `bl_session` (HttpOnly, SameSite=Lax, berlaku 30 hari). Di belakang HTTPS, set `BELAJAR_LAGI_HTTPS=1` agar cookie diberi flag `Secure`. Logout dan reset password menghapus sesi di server.

## Run tests

```bash
.venv\Scripts\python.exe -m pytest -q
```

Test memakai database sementara lewat environment variable `BELAJAR_LAGI_DB`, jadi `learning.db` milikmu tidak tersentuh. Untuk mengarahkan aplikasi ke database lain secara manual:

```powershell
$env:BELAJAR_LAGI_DB = "C:\path\ke\database.db"
```

## Deployment (server)

SQLite hanya cocok untuk **satu worker**. Jangan jalankan beberapa proses uvicorn yang menulis database yang sama.

### 1. Siapkan database (fresh) dan admin pertama

```bash
export BELAJAR_LAGI_DB=/srv/belajar-lagi/learning.db
python scripts/seed.py
python scripts/manage_users.py setup-admin --email admin@example.com --name Admin
```

`seed.py` membuat katalog kelas/lesson (68 lesson) tanpa progres. Semua user mulai dari 0%.

### 2. Siapkan sandbox Docker (untuk Playground & Challenges)

```bash
docker pull python:3.11-slim
docker version   # pastikan daemon jalan dan user app bisa mengakses socket
```

Runner menjalankan kode user di container sekali pakai yang diperkeras: `--network none`, `--cap-drop ALL`, `--read-only`, batas memori/CPU, tanpa akses jaringan.

### 3. Jalankan di belakang reverse proxy HTTPS

```bash
export BELAJAR_LAGI_HTTPS=1
export BELAJAR_LAGI_RUNNER=1
export BELAJAR_LAGI_RUNNER_BACKEND=docker
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

Contoh systemd (ringkas):

```ini
[Service]
WorkingDirectory=/srv/belajar-lagi
Environment=BELAJAR_LAGI_DB=/srv/belajar-lagi/learning.db
Environment=BELAJAR_LAGI_HTTPS=1
Environment=BELAJAR_LAGI_RUNNER=1
Environment=BELAJAR_LAGI_RUNNER_BACKEND=docker
ExecStart=/srv/belajar-lagi/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
Restart=on-failure
```

### 4. Backup konsisten

Aman meskipun server berjalan (memakai SQLite backup API):

```bash
python scripts/backup_db.py
python scripts/backup_db.py --output /srv/backups/belajar-lagi-$(date +%F).db
```

Folder `backups/` dan `learning.db` sudah di-ignore Git. Jangan commit database atau backup.

### 5. Buat akun teman

```bash
python scripts/manage_users.py create --email teman@example.com --name "Nama Teman"
```

### Catatan runner

- `BELAJAR_LAGI_RUNNER=0` mematikan eksekusi kode total.
- `BELAJAR_LAGI_RUNNER_BACKEND=subprocess` hanya untuk dev lokal (tidak aman).
- `BELAJAR_LAGI_RUNNER_BACKEND=docker` adalah pilihan aman untuk server.
- Detail lengkap ada di **Security (code runner)** di bawah.

## Project structure

```text
BelajarLagi/
├── roadmap.md, progress.md
├── app/
│   ├── main.py            # FastAPI entry
│   ├── api/deps.py        # current_user / optional_user
│   ├── api/routes/        # endpoint API (termasuk auth.py dan courses.py)
│   ├── services/          # db, auth, content, runner, challenges
│   ├── data/              # definisi challenge & katalog kursus (courses_def.py)
├── database/
│   ├── schema.sql         # skema SQLite multi-user
│   ├── migrations.py      # migrasi otomatis dari skema single-user
│   └── database.py        # koneksi + init_db
├── content/               # materi markdown
├── frontend/              # SPA (index.html, css, js)
│   └── js/vendor/         # Feather icons (lokal)
├── scripts/
│   ├── seed.py            # inisialisasi database + mapping course/module/lesson
│   ├── manage_users.py    # buat admin, akun, reset password, aktivasi
│   └── backup_db.py       # backup SQLite yang konsisten
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
3. Tekan **Run & Test**. Sistem menjalankan kode lewat runner (di server: sandbox Docker; di dev lokal: `subprocess` dengan `-I`), lalu mengetes **hidden test case**.
4. Lihat hasil pass/fail + expected vs received.
5. Gunakan **Hint 1 / Hint 2** jika buntu — solusi penuh **tidak** ditampilkan di frontend.

## How progress works

Progress tersimpan di SQLite (tidak hanya checkbox frontend). Database mencatat:
- `users` + `auth_sessions` (akun dan sesi login)
- `courses` → `course_modules` → `course_lessons` (katalog dan urutan materi)
- `course_enrollments` (kelas yang diikuti/dimulai, per user)
- `lessons` + `lesson_progress` (status + `completed_at`, per user)
- `challenges` + `challenge_attempts` (result, time, hints, attempt number, per user)
- `learning_sessions` (untuk streak & total waktu belajar, per user)
- `interview_progress` (status per user per pertanyaan)
- `notes`, `mistakes`, `project_task_progress`

Semua statistik di dashboard/progress **berasal dari data nyata** dan dihitung terpisah untuk setiap akun — mulai dari 0%, bukan data palsu.

## Security (code runner)

Runner punya dua backend, dipilih lewat `BELAJAR_LAGI_RUNNER_BACKEND`:

- `subprocess` (default, khusus dev lokal): menjalankan kode di interpreter server dengan mode isolasi `-I`. **Bukan sandbox** — `-I` tidak membatasi akses filesystem, network, memori, atau CPU. Jangan dipakai untuk user yang tidak dipercaya.
- `docker` (untuk server): menjalankan kode di container sekali pakai yang diperkeras:
  - `--network none` (tanpa internet)
  - `--cap-drop ALL`, `--read-only`, `--security-opt no-new-privileges`
  - `--memory 128m --memory-swap 128m --cpus 0.5 --pids-limit 64`
  - `--user 1000:1000`, `--pull=never`
  - timeout 20 detik, batas output 10.000 karakter
- `BELAJAR_LAGI_RUNNER=0` mematikan eksekusi kode total. Playground dan submit challenge mengembalikan error tanpa menjalankan kode.

Catatan keamanan:

- Kalau `backend=docker` tapi Docker tidak tersedia, server **menolak** menjalankan kode (tidak diam-diam fallback ke `subprocess`).
- Akses ke Docker socket itu kuat: app yang bisa memanggil Docker secara teori bisa mount filesystem host. Sandbox Docker jauh lebih aman dari `subprocess`, tapi bukan jaminan absolut. Untuk isolasi lebih kuat, pakai runtime gVisor (`runsc`) atau rootless Docker.
- Challenge solution & hidden tests tetap disimpan di backend, bukan frontend.
- `eval()` tidak digunakan untuk menjalankan kode user.
- Tanpa sandbox, opsi paling aman adalah `BELAJAR_LAGI_RUNNER=0` atau menonaktifkan endpoint `/api/playground/run` dan submit challenge di reverse proxy.

## Login & cookie

- Password di-hash dengan `hashlib.scrypt` (salt acak per password).
- Sesi memakai token acak opaque; yang disimpan di database hanya hash SHA-256 token.
- Cookie `bl_session`: HttpOnly, SameSite=Lax, umur 30 hari, `Secure` jika `BELAJAR_LAGI_HTTPS=1` atau request HTTPS.
- Logout, reset password, dan deaktivasi akun menghapus sesi terkait.
- Akun nonaktif tidak bisa login dan sesi lamanya tidak berlaku.

## Fitur

Login multi-user, dashboard, **Kelas** (katalog publik + detail + modul), **Kelas Saya**, lesson dengan outline kelas, Roadmap, Challenges, Python Playground, Projects, Notes, Mistake Journal, Progress per kelas, Weekly Review, Search (Ctrl+K), Dark Mode. Admin mengelola akun lewat CLI; registrasi publik belum tersedia.

Shortcut: `Ctrl+K` = search, `Ctrl+Enter` = run code.

## AI Usage Policy

```
TRY FIRST.
THINK BEFORE ASKING AI.
USE AI TO LEARN, NOT TO AVOID THINKING.
```
