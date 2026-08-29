# Progress — Belajar Lagi

Status dan progres pengembangan platform ini. Data belajar user tersimpan di SQLite (`learning.db`), **tidak dicatat di file ini** — file ini untuk progres pembangunan platform.

## Milestone

- [x] **M1 — Project setup** (venv, git, requirements, struktur folder)
- [x] **M2 — Dashboard** (`/api/dashboard`, dashboard UI)
- [x] **M3 — Lesson system** (render markdown, prev/next, mark as complete)
- [x] **M4 — Progress tracking** (SQLite: lessons, lesson_progress, streak, sessions)
- [x] **M5 — Challenge system** (5 challenge Python, hidden tests, hints, attempts)
- [x] **M6 — Python playground** (safe subprocess runner, timeout, isolasi)
- [x] **M7 — Notes + Mistake Journal**
- [ ] **M8 — Weekly Review** (halaman dasar sudah ada, perbaiki rekomendasi data)
- [x] **M9 — Project tracker** (Employee Management, 9 stages)
- [ ] **M10 — AI Mentor** (ditunda: butuh LLM API key)
- [x] **M11 — Testing** (pytest)
- [ ] **M12 — Polish** (lanjutan)

## Fitur

- [x] Dashboard dengan statistik nyata
- [x] Roadmap UI (✓ → ○)
- [x] Lesson system + Day 01 (Variable & Data Types)
- [x] Mark as Complete (server-side)
- [x] Python Playground (run kode)
- [x] 5 Python challenges (easy) dengan hidden tests + hint 1/2
- [x] Notes & Mistake Journal (CRUD)
- [x] Progress per topik
- [x] Dark mode + search (Ctrl+K) + Ctrl+Enter run
- [x] Project tracker (9 stage Employee Management)

## Konten

- [x] Day 01 — Variable & Data Types (`content/daily/day01.md`)
- [ ] Day 02 — Operator & I/O
- [ ] Day 03 — Conditional
- [ ] Day 04 — Loop
- [ ] ... lanjut sesuai `belajar.txt`

## Catatan

- Semua statistik dashboard berasal dari data nyata DB (mulai 0%).
- AI Mentor ditunda sampai MVP stabil & ada cara menyediakan LLM.
- Challenge solution & hidden tests tersimpan di backend (`app/data/challenges_def.py`), tidak bocor ke frontend.
