# CI/CD — Build, Test, Deploy

## Learning Objective

- Memahami CI (Continuous Integration) & CD (Continuous Delivery/Deployment)
- Pipeline: build, test, deploy
- Environment: staging vs production, rollback
- Membuat pipeline GitHub Actions sederhana

---

## Theory

### CI vs CD

- **CI** — setiap push di-test + di-build otomatis (integrasi terus-menerus).
- **CD** — build yang lulus otomatis/deploy ke staging/production.

### Pipeline

```text
Git Push
  ↓
CI: jalankan test
  ↓
Build artifact
  ↓
Deploy ke Staging
  ↓
(Verifikasi)
  ↓
Deploy ke Production
```

### Environment

- **Staging** — mirip produksi untuk uji aman sebelum rilis.
- **Production** — yang dipakai user.
- Variabel env dibedakan per environment (`.env.staging`, `.env.production`, secret manager).
- **Rollback** — kembalikan ke versi sebelumnya jika deploy gagal.

---

## Analogy

CI/CD = "pabrik perakitan + QC" untuk kode: setiap perubahan produk masuk jalur, otomatis dites, dibangun, lalu dikirim ke gudang (staging) dan toko (production). Kalau ada cacat, kamu bisa tarik kembali versi lama (rollback) — bukan perbaikan dadakan di tengah produksi.

---

## Examples — GitHub Actions

```yaml
# .github/workflows/tests.yml
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
      - run: pytest -q
```

---

## Code — deploy step (sederhana)

```yaml
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy via SSH
        env:
          SSH_PRIVATE_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          ssh-keyscan server.example.com >> ~/.ssh/known_hosts
          echo "$SSH_PRIVATE_KEY" > key && chmod 600 key
          ssh -i key user@server.example.com 'cd /app && git pull && docker compose up -d --build'
```

---

## Explanation

- Test gagal → deploy berhenti (guard).
- Build sekali → artifact dipakai di staging & production (konsistensi).
- Secrets (`DEPLOY_KEY`, DB password) disimpan di CI secret, bukan di YAML.
- Rollback: deploy ulang tag/commit lama, atau `docker compose up --build` versi sebelumnya.
- Blue/green, canary, rolling = strategi deploy lanjutan — mulai dari simpel dulu.

---

## Common Mistakes

1. Deploy langsung ke production tanpa staging.
2. Secret hardcode di pipeline YAML.
3. Test tidak jalan di CI (lupa install deps).
4. Deploy manual dari laptop (kurang traceable, mudah salah.
5. Tidak ada rollback plan.

---

## Manual Exercises

### Exercise 1
Buat `.github/workflows/ci.yml` dengan job test.

### Exercise 2
Jalankan pipeline, lihat hasil di tab Actions.

### Exercise 3
Tambahkan step lint (ruff/flake8).

### Exercise 4
Tulis deploy step ke staging (SSH/rsync).

### Exercise 5
Buat langkah rollback (deploy commit `HEAD~1`).

---

## Challenge — Minimal Exercise

Buat workflow CI untuk repo ini: setup Python, install requirements, `pytest -q`. Push dan pastikan hijau.

---

## Reflection

1. Apa beda CI dan CD?
2. Kenapa staging penting?
3. Bagaimana pipeline menghentikan deploy saat gagal?
4. Di mana secrets disimpan dengan aman?
5. Apa rencana rollback-mu?

---

## Checklist

- [ ] Bisa jelaskan CI/CD
- [ ] Bisa membuat GitHub Actions
- [ ] Bisa build→test→deploy
- - [ ] Bisa mengelola env staging/prod
- - [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 5

```yaml
- name: Rollback ke versi sebelumnya
  run: ssh ... 'cd /app && git checkout HEAD~1 && docker compose up -d --build'
  if: failure()
```

</details>