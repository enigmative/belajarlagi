# CI/CD — Continuous Delivery & Deployment

## Learning Objective

- Memahami Continuous Delivery vs Continuous Deployment (CD)
- Pipeline deploy: build artifact → staging → production
- Mengelola environment & secrets dengan aman
- Strategi rollback & pemulihan saat deploy gagal
- Mengenal strategi deploy lanjutan (blue/green, canary, rolling)

---

## Theory

### CD vs CD

- **Continuous Delivery** — kode siap dirilis kapan saja; deploy ke production tetap keputusan manual/trigger.
- **Continuous Deployment** — setiap code yang lulus test **otomatis** di-deploy ke production.

### Alur deploy

```text
CI (build + test lulus)
   ↓
Build artifact (sekali)
   ↓
Deploy ke Staging
   ↓
(Verifikasi manual/auto)
   ↓
Deploy ke Production
```

### Environment

- **Staging** — replika mendekati produksi untuk uji aman.
- **Production** — dipakai user sungguhan.
- Env var per environment (`.env.staging`, `.env.production`) atau **secret manager**.
- Secrets (`DEPLOY_KEY`, DB password) disimpan di CI Secrets, **bukan** di YAML.

### Rollback

- Kembalikan ke versi sebelumnya bila deploy gagal.
- Cara sederhana: deploy ulang commit/tag lama.

---

## Analogy

CD = jalur pengiriman dari pabrik ke gudang (staging) lalu toko (production). Rollback = menarik kembali barang dan menaruh yang versi lama di etalase saat barang baru ternyata cacat — bukan memperbaiki di tengah toko. Environment = toko percobaan (staging) vs toko asli (production); kunci gudang (secrets) disimpan di brankas terpisah.

---

## Examples — deploy step GitHub Actions

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy via SSH
        env:
          SSH_PRIVATE_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          ssh-keyscan server.example.com >> ~/.ssh/known_hosts
          echo "$SSH_PRIVATE_KEY" > key && chmod 600 key
          ssh -i key user@server.example.com 'cd /app && git pull && docker compose up -d --build'
```

---

## Code — rollback sederhana

```yaml
- name: Rollback ke versi sebelumnya
  run: ssh ... 'cd /app && git checkout HEAD~1 && docker compose up -d --build'
  if: failure()
```

- `if: failure()` menjalankan step ini hanya bila step deploy sebelumnya gagal.
- Alternatif: tag versi (`v1.0.1`, `v1.0.2`) lalu deploy ulang ke tag lama.

---

## Explanation

- Build **sekali** → artefak yang sama dipakai di staging & production (konsistensi).
- CD yang baik = reproducible: hasil deploy dari kode+config deterministik.
- Secrets dikelola via CI secret manager / cloud secret — tidak pernah di-YAML atau repo.
- Rollback plan wajib ada sebelum deploy ke production.
- Strategi lanjutan:
  - **Blue/green** — dua environment; pindah traffic saat green siap.
  - **Canary** — rilis ke sebagian user dulu, lalu penuh.
  - **Rolling** — perbarui server satu per satu.
  - Mulai dari yang simpel, naikkan saat kebutuhan muncul.

---

## Common Mistakes

1. Deploy langsung ke production tanpa staging.
2. Secret hardcode di pipeline YAML.
3. Deploy manual dari laptop (tidak traceable, rawan salah).
4. Tidak punya rollback plan.
5. Artifact dibuild ulang beda di staging & production (inkonsisten).

---

## Manual Exercises

### Exercise 1
Buat workflow deploy yang hanya jalan saat `main` (condition `github.ref`).

### Exercise 2
Simpan kunci SSH di **Secrets** (bukan YAML) dan baca via `${{ secrets.XXX }}`.

### Exercise 3
Deploy ke staging via SSH/rsync; verifikasi aplikasi.

### Exercise 4
Tulis step rollback (`git checkout HEAD~1` + build ulang).

### Exercise 5
Jelaskan kapan memilih blue/green vs canary vs rolling untuk proyekmu.

---

## Challenge — Minimal Exercise

Tulis alur deploy lengkap untuk proyekmu: dari CI lulus → staging → verifikasi → production, plus skenario rollback bila staging gagal. Simpan di Notes.

---

## Reflection

1. Apa beda Continuous Delivery dan Continuous Deployment?
2. Mengapa build sekali untuk semua environment?
3. Di mana secrets disimpan dengan aman?
4. Mengapa rollback plan wajib?
5. Kapan blue/green atau canary layak?

---

## Checklist

- [ ] Paham CD (delivery vs deployment)
- [ ] Bisa deploy step ke staging/prod
- [ ] Bisa kelola secrets
- [ ] Bisa rollback
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 4

```yaml
- name: Deploy
  id: deploy
  run: ssh ... 'cd /app && git pull && docker compose up -d --build'

- name: Rollback
  if: failure()
  run: ssh ... 'cd /app && git checkout HEAD~1 && docker compose up -d --build'
```

</details>
