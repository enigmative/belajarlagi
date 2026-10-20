# Deploy Belajar Lagi ke Server Linux

Contoh konfigurasi untuk menjalankan Belajar Lagi di server Linux di belakang reverse proxy HTTPS.

## Prasyarat

- Linux (Ubuntu/Debian disarankan)
- Python 3.11+
- Docker (untuk sandbox code runner)
- Nginx atau Caddy
- `sudo`/akses root

## Langkah

### 1. Pasang dependensi sistem

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx
# atau pasang Caddy sesuai dokumentasi resmi
# Docker: https://docs.docker.com/engine/install/
```

### 2. Salin kode & buat virtual environment

```bash
sudo mkdir -p /srv/belajar-lagi
sudo chown "$USER":"$USER" /srv/belajar-lagi
git clone <repo-url> /srv/belajar-lagi
cd /srv/belajar-lagi
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3. Database fresh + admin pertama

```bash
export BELAJAR_LAGI_DB=/srv/belajar-lagi/learning.db
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
```

### 5. Pasang service systemd

```bash
sudo cp deploy/systemd/belajar-lagi.service /etc/systemd/system/belajar-lagi.service
sudo systemctl daemon-reload
sudo systemctl enable --now belajar-lagi
sudo systemctl status belajar-lagi
```

### 6. Reverse proxy HTTPS

- Caddy: salin `deploy/caddy/Caddyfile` ke `/etc/caddy/Caddyfile` (sesuaikan domain).
- Nginx: salin `deploy/nginx/belajar-lagi.conf` ke `/etc/nginx/sites-available/`, lalu `ln -s` ke `sites-enabled/` dan `nginx -t && systemctl reload nginx`.

### 7. Backup terjadwal

Tambahkan ke crontab (`crontab -e`):

```cron
30 3 * * * cd /srv/belajar-lagi && .venv/bin/python scripts/backup_db.py
```

Perintah di atas memakai nama file default `backups/learning-<timestamp>.db` (relatif terhadap folder proyek). Untuk nama berdasar tanggal, jalankan manual:

```bash
cd /srv/belajar-lagi && .venv/bin/python scripts/backup_db.py --output /srv/backups/belajar-lagi-$(date +%F).db
```

### 8. Buat akun teman

```bash
cd /srv/belajar-lagi
.venv/bin/python scripts/manage_users.py create --email teman@example.com --name "Nama Teman"
```

## Verifikasi

1. Buka `https://<domain>` → katalog kelas bisa dilihat tanpa login.
2. Login sebagai admin → dashboard tampil.
3. Coba Playground → kode jalan di sandbox Docker.
4. Coba Challenges → submit berjalan.
5. Login sebagai akun teman → progres mulai 0% dan tidak bisa melihat data admin.

## Catatan keamanan

- `BELAJAR_LAGI_RUNNER_BACKEND=docker` wajib untuk server. Jangan pakai `subprocess` di server.
- Akses Docker socket itu kuat. Untuk isolasi lebih kuat, pertimbangkan gVisor (`runsc`) atau rootless Docker.
- `BELAJAR_LAGI_RUNNER=0` mematikan eksekusi kode total jika ingin paling konservatif.
