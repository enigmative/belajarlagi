# Progress — Belajar Lagi

Status dan progres pengembangan platform ini. Data belajar user tersimpan di SQLite (`learning.db`), **tidak dicatat di file ini** — file ini untuk progres pembangunan platform.

## Milestone

- [x] **M1 — Project setup** (venv, git, requirements, struktur folder)
- [x] **M2 — Dashboard** (`/api/dashboard`, dashboard UI)
- [x] **M3 — Lesson system** (render markdown, prev/next, mark as complete)
- [x] **M4 — Progress tracking** (SQLite: lessons, lesson_progress, streak, sessions)
- [x] **M5 — Challenge system** (70 challenge Python: 30 easy + 30 medium + 10 advanced, hidden tests, hints, attempts)
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
- [x] 70 Python challenges (30 easy + 30 medium + 10 advanced) — Problem Solving: two sum, sliding window, DP, tree, dsb.
- [x] Notes & Mistake Journal (CRUD)
- [x] Progress per topik
- [x] Dark mode + search (Ctrl+K) + Ctrl+Enter run
- [x] Project tracker (9 stage Employee Management)

## Konten

- [x] Day 01 — Variable & Data Types (`content/daily/day01.md`)
- [x] Day 02 — Operators
- [x] Day 03 — Conditional
- [x] Day 04 — Loop
- [x] Day 05 — Function
- [x] Day 06 — String
- [x] Day 07 — List
- [x] Day 08 — Dictionary
- [x] Day 09 — Set & Tuple
- [x] Day 10 — Exception (`try/except`)
- [x] Day 11 — File Handling
- [x] Day 12 — Module & Package
- [x] Day 13 — OOP: Class & Object
- [x] Day 14 — OOP: Inheritance & Polymorphism
- [x] Day 15 — Typing & Dataclass
- [x] Day 16 — Decorator
- [x] Day 17 — Generator & Iterator
- [x] Day 18 — Context Manager
- [x] Day 19 — Big-O & Complexity
- [x] Day 20 — Searching
- [x] Day 21 — Sorting
- [x] Day 22 — Data Structures
- [x] Day 23 — Testing dengan pytest
- [x] Day 24 — Git
- [x] Day 25 — Debugging
- [x] Day 26 — HTTP & REST
- [x] Day 27 — FastAPI
- [x] Day 28 — Backend Project (Employee API)
- [x] SQL — CRUD & Query Dasar
- [x] SQL — JOIN
- [x] SQL — Database Design & Normalization
- [x] SQL — Transaction & ACID
- [x] SQL — Query Optimization
- [x] PHP — Fundamentals
- [x] PHP — Function, Array, & Loop
- [x] PHP — OOP
- [x] PHP — Composer, PSR, & SOLID
- [x] CodeIgniter — MVC & Routing
- [x] CodeIgniter — Model, Database, & Validation
- [x] CodeIgniter — Session, Auth, Filter, & REST API
- [x] Laravel — Routing, Controller, Blade, & Middleware
- [x] Laravel — Eloquent ORM & Relasi
- [x] Laravel — Auth, Queue, Events, & Fitur Produksi
- [x] JavaScript — Fundamentals
- [x] JavaScript — DOM & Events
- [x] JavaScript — Async, Fetch, Promise, JSON
- [x] Frontend Framework — Vue & React
- [x] Web Security — Auth, Session, Cookie, Password
- [x] Web Security — CSRF, XSS, SQL Injection
- [x] Web Security — API Hardening
- [x] Docker — Image, Container, Dockerfile
- [x] Docker — Volume, Network, Environment, Compose
- [x] Linux — Command Line Dasar
- [x] Linux — Process, Service, & Logs
- [x] Redis & Queue — Cache, Job, Worker
- [x] CI/CD — Build, Test, Deploy
- [x] Software Architecture — MVC, Layered, Clean
- [x] System Design — Komponen & Scaling
- [x] Observability — Logging, Metrics, Alerting

## Challenge (Python Easy + Medium)

- [x] Find Largest Number
- [x] Sum of List
- [x] Is It Even?
- [x] Reverse String
- [x] Count Characters
- [x] FizzBuzz
- [x] Is Leap Year?
- [x] Factorial
- [x] Count Vowels
- [x] Second Largest
- [x] Binary Search (medium)
- [x] Two Sum (medium)
- [x] Find Missing Number (medium)
- [x] Balanced Brackets (medium)
- [x] Sort List (medium)
- [ ] ... lanjut sesuai Problem Solving (`belajar.txt` Level 2)

## Catatan

- Semua statistik dashboard berasal dari data nyata DB (mulai 0%).
- AI Mentor ditunda sampai MVP stabil & ada cara menyediakan LLM.
- Challenge solution & hidden tests tersimpan di backend (`app/data/challenges_def.py`), tidak bocor ke frontend.
