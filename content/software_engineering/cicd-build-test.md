# CI/CD — Continuous Integration: Build & Test

## Learning Objective

- Memahami Continuous Integration (CI) dan mengapa otomatis
- Menulis pipeline GitHub Actions: trigger, jobs, steps
- Menyiapkan environment build (install deps, cache)
- Menjalankan lint & unit test secara otomatis
- Menjadikan test sebagai guard sebelum lanjut ke deploy

---

## Theory

### Apa itu CI?

> **Continuous Integration** — setiap perubahan kode (push/PR) otomatis ditarik, di-build, dan dites. Tujuannya mendeteksi masalah sedini mungkin, sebelum masuk ke produksi.

### Pipeline dasar

```text
Git Push / Pull Request
   ↓
Checkout code
   ↓
Setup runtime (Python/Node/PHP)
   ↓
Install dependencies
   ↓
Lint
   ↓
Run tests
   ↓
(PASS → artefak siap / FAIL → berhenti)
```

### GitHub Actions building block

- **workflow** — file YAML di `.github/workflows/`.
- **on** — pemicu (`[push, pull_request]`).
- **jobs** — kumpulan pekerjaan; bisa `needs` antar job.
- **steps** — perintah/action dalam satu job.
- **runs-on** — mesin virtual (ubuntu-latest).

---

## Analogy

CI = jalur QC otomatis di pabrik: setiap produk (commit) yang masuk otomatis diperiksa mesin (lint + test) sebelum boleh lanjut ke gudang/deploy. Kalau ada cacat, langsung ditolak — tidak menunggu ditemukan user di toko.

---

## Examples — GitHub Actions minimal

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest -q
```

---

## Code — dengan cache dependency

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}
      - run: pip install -r requirements.txt
      - run: pytest -q
```

Cache mempercepat install dependency & menghemat waktu pipeline.

---

## Explanation

- Test gagal → pipeline merah → deploy berhenti (guard). Ini inti CI.
- Setup environment yang **konsisten**: versi Python/PHP/Node sama di semua develop.
- Lint (ruff/flake8/phpcs) menangkap gaya/kutu statis sebelum runtime.
- `hashFiles('requirements.txt')` membuat key cache berubah saat dependency berubah.
- CI yang baik = cepat memberi feedback; jangan biarkan pipeline jadi bottleneck.

---

## Common Mistakes

1. Lupa install dependencies → test "tidak jalan" bukan "gagal".
2. Versi runtime beda antara lokal & CI → "works on my machine".
3. Tidak ada lint → masalah gaya baru terdeteksi belakangan.
4. Test menyentuh kredensial/produksi → tidak aman di CI.
5. Pipeline lambat karena tanpa cache dependency.

---

## Manual Exercises

### Exercise 1
Buat `.github/workflows/ci.yml` dengan trigger `[push, pull_request]`.

### Exercise 2
Setup Python 3.11, install `requirements.txt`, jalankan `pytest -q`.

### Exercise 3
Tambahkan step lint `ruff check .` (atau lint PHP/JS sesuai stack).

### Exercise 4
Push dan lihat hasilnya di tab **Actions**; buat satu test yang sengaja gagal untuk melihat merah.

### Exercise 5
Tambahkan cache dependency (`actions/cache`).

---

## Challenge — Minimal Exercise

Buat workflow CI untuk repo ini: setup Python, install requirements, `pytest -q`, plus lint. Push ke GitHub dan pastikan status hijau. Catat langkahnya di Notes.

---

## Reflection

1. Mengapa CI penting?
2. Apa peran `on:` dalam workflow?
3. Kenapa test perlu jadi guard sebelum deploy?
4. Bagaimana lint membantu?
5. Apa manfaat caching dependency?

---

## Checklist

- [ ] Paham Continuous Integration
- [ ] Bisa buat GitHub Actions (on/jobs/steps)
- [ ] Bisa setup build & install deps
- [ ] Bisa tambah lint & test
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1-3

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest -q
```

</details>
