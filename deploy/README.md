# Deploy Belajar Lagi ke Server Linux

Panduan menjalankan Belajar Lagi di server Linux, dengan sandbox Docker dan akses HTTPS.

Path contoh di dokumen ini: **`/mount/hdd/belajar-lagi`**. Silakan sesuaikan dengan servermu.

## Prasyarat

- Linux (Ubuntu/Debian disarankan)
- Python 3.11+
- Docker (untuk sandbox code runner)
- `sudo`/akses root
- Untuk HTTPS: domain di Cloudflare (Tunnel) atau reverse proxy (Nginx/Caddy)

## Langkah

### 1. Pasang dependensi sistem

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
# Docker: https://docs.docker.com/engine/install/
```

**Catatan Python 3.11.** Ubuntu 20.04 (focal) memakai Python 3.8 dan PPA `deadsnakes`
tidak punya build ARM64. Untuk server ARM64, pakai Miniconda:

```bash
cd /mount/hdd/belajar-lagi
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
bash Miniconda3-latest-Linux-aarch64.sh -b -p /mount/hdd/belajar-lagi/miniconda3
/mount/hdd/belajar-lagi/miniconda3/bin/conda create -y -n py311 python=3.11 --override-channels -c conda-forge
```

### 2. Salin kode & buat virtual environment

```bash
sudo mkdir -p /mount/hdd/belajar-lagi
sudo chown "$USER":"$USER" /mount/hdd/belajar-lagi
git clone <repo-url> /mount/hdd/belajar-lagi
cd /mount/hdd/belajar-lagi

# Dengan Python 3.11 sistem:
python3.11 -m venv .venv

# Atau dari Miniconda:
/mount/hdd/belajar-lagi/miniconda3/envs/py311/bin/python -m venv .venv

.venv/bin/python --version          # pastikan 3.11+
.venv/bin/pip install -r requirements.txt
```

### 3. Database fresh + admin pertama

```bash
export BELAJAR_LAGI_DB=/mount/hdd/belajar-lagi/learning.db
.venv/bin/python scripts/seed.py
.venv/bin/python scripts/manage_users.py setup-admin --email admin@example.com --name Admin
```

Semua kelas/lesson terisi, progres mulai dari 0%.

### 4. Siapkan sandbox Docker

```bash
docker pull python:3.11-slim
docker version
```

User yang menjalankan service harus bisa mengakses Docker socket (biasanya grup `docker`):

```bash
sudo usermod -aG docker "$USER"
newgrp docker
```

### 5. Pasang service systemd

```bash
sudo cp deploy/systemd/belajar-lagi.service /etc/systemd/system/belajar-lagi.service
sudo systemctl daemon-reload
sudo systemctl enable --now belajar-lagi
sudo systemctl status belajar-lagi
```

Sesuaikan `User=`/`Group=` dan path di file service dengan servermu.

### 6. Akses HTTPS

#### Opsi A (direkomendasikan): Cloudflare Tunnel

Cocok untuk server di belakang NAT/tanpa IP publik. Tidak perlu port forwarding.

```bash
# Install cloudflared (ARM64)
cd /tmp
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb

# Login (buka URL yang muncul di browser, pilih zone domain, lalu Authorize)
cloudflared tunnel login

# Buat tunnel
cloudflared tunnel create belajar-lagi
```

Buat `~/.cloudflared/config.yml` (contoh: `deploy/cloudflared/config.yml.example`):

```yaml
tunnel: <TUNNEL-UUID>
credentials-file: /home/<USER>/.cloudflared/<TUNNEL-UUID>.json

ingress:
  - hostname: belajarlagi.enigmative.web.id
    service: http://localhost:8000
  - service: http_status:404
```

Buat DNS record otomatis:

```bash
cloudflared tunnel route dns belajar-lagi belajarlagi.enigmative.web.id
```

Jalankan sebagai service (contoh: `deploy/cloudflared/cloudflared-belajar.service`):

```bash
sudo cp deploy/cloudflared/cloudflared-belajar.service /etc/systemd/system/cloudflared-belajar.service
# sesuaikan User/Group dan path di file tersebut
sudo systemctl daemon-reload
sudo systemctl enable --now cloudflared-belajar
sudo systemctl status cloudflared-belajar
sudo journalctl -u cloudflared-belajar -n 30 --no-pager
```

> Kalau server sudah punya service `cloudflared` lain (mis. untuk Nextcloud), **jangan**
> menimpa service itu. Buat service kedua seperti contoh di atas.

#### Opsi B: Reverse proxy (Nginx/Caddy)

Kalau server punya IP publik:

- Caddy: salin `deploy/caddy/Caddyfile` ke `/etc/caddy/Caddyfile` (sesuaikan domain).
- Nginx: salin `deploy/nginx/belajar-lagi.conf` ke `/etc/nginx/sites-available/`, lalu `ln -s` ke `sites-enabled/` dan `nginx -t && systemctl reload nginx`.

Jangan lupa buka port 80/443 (`sudo ufw allow 80/tcp && sudo ufw allow 443/tcp`).

### 7. Backup terjadwal

Tambahkan ke crontab (`crontab -e`):

```cron
30 3 * * * cd /mount/hdd/belajar-lagi && .venv/bin/python scripts/backup_db.py
```

Perintah di atas memakai nama file default `backups/learning-<timestamp>.db` (relatif terhadap folder proyek). Untuk nama berdasar tanggal, jalankan manual:

```bash
cd /mount/hdd/belajar-lagi && .venv/bin/python scripts/backup_db.py --output /mount/hdd/backups/belajar-lagi-$(date +%F).db
```

### 8. Buat akun teman

```bash
cd /mount/hdd/belajar-lagi
.venv/bin/python scripts/manage_users.py create --email teman@example.com --name "Nama Teman"
```

## Verifikasi

1. Buka `https://belajarlagi.enigmative.web.id` → katalog kelas bisa dilihat tanpa login.
2. Login sebagai admin → dashboard tampil.
3. Coba Playground → `print('hello')` jalan; `open('/etc/passwd')` **gagal**.
4. Coba Challenges → submit berjalan.
5. Login sebagai akun teman → progres mulai 0% dan tidak bisa melihat data admin.

## Catatan keamanan

- `BELAJAR_LAGI_RUNNER_BACKEND=docker` wajib untuk server. Jangan pakai `subprocess` di server.
- Akses Docker socket itu kuat. Untuk isolasi lebih kuat, pertimbangkan gVisor (`runsc`) atau rootless Docker.
- `BELAJAR_LAGI_RUNNER=0` mematikan eksekusi kode total jika ingin paling konservatif.
- `BELAJAR_LAGI_HTTPS=1` wajib agar cookie `Secure` (aman dikirim lewat HTTPS).
- Pastikan `/mount/hdd` (atau mount point-mu) auto-mount saat reboot (`/etc/fstab`).

## GitHub Actions (CI/CD) — auto-deploy dari push ke `main`

Workflow ada di `.github/workflows/deploy.yml`. Trigger: push ke `main` atau manual (`workflow_dispatch`).

### Setup self-hosted runner (sekali)

1. GitHub → repo → Settings → Actions → Runners → **New self-hosted runner** → pilih Linux ARM64.
2. Jalankan perintah yang diberikan GitHub di server (sebagai `LAB-02`):
   ```bash
   mkdir -p ~/actions-runner && cd ~/actions-runner
   curl -o actions-runner-linux-arm64-2.319.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.319.0/actions-runner-linux-arm64-2.319.0.tar.gz
   tar xzf *.tar.gz
   ./config.sh --url https://github.com/enigmative/belajarlagi --token <TOKEN_DARI_GITHUB>
   sudo ./svc.sh install LAB-02
   sudo ./svc.sh start
   ```
3. Pasang sudoers terbatas:
   ```bash
   sudo cp deploy/sudoers/belajar-deploy /etc/sudoers.d/belajar-deploy
   sudo chmod 440 /etc/sudoers.d/belajar-deploy
   sudo visudo -cf /etc/sudoers.d/belajar-deploy
   ```
4. Pastikan `LAB-02` punya akses git ke repo (SSH key atau credential helper).

### Alur deploy

```
git push origin main
  → GitHub Actions
    → backup DB
    → git pull origin main
    → pip install -r requirements.txt
    → docker pull python:3.11-slim
    → sudo systemctl restart belajar-lagi
    → health check (curl /api/courses, max 30x2s)
```

### Deploy manual (tanpa GitHub Actions)

```bash
bash scripts/deploy.sh
```

### Rollback

```bash
cd /mount/hdd/belajar-lagi
git log --oneline -5
git reset --hard <commit-sebelumnya>
sudo systemctl restart belajar-lagi
```

## Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| `docker pull` gagal | Daemon tidak jalan | `sudo systemctl start docker` / cek `journalctl -u docker` |
| `python3.11` tidak ada | Python terlalu lama | Miniconda / deadsnakes / pyenv |
| `Cannot connect to the Docker daemon` | Grup docker belum aktif | `newgrp docker` atau logout/login |
| `Silakan masuk` padahal sudah login | Cookie `Secure` + HTTP | Pastikan `BELAJAR_LAGI_HTTPS=1` dan akses lewat HTTPS |
| Halaman tidak bisa diakses | Tunnel belum jalan | `sudo systemctl status cloudflared-belajar` |
