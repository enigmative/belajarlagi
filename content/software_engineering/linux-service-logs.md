# Linux — Service, Logs & Environment

## Learning Objective

- Mengelola service dengan systemd (status, start, stop, restart, enable)
- Membaca log service (`journalctl`) dan file log
- Memahami lingkungan environment variables
- Menghindari credential hardcode via config/env
- Melihat struktur filesystem Linux (/, /etc, /var, /home, /tmp)

---

## Theory

### Service (systemd)

```bash
systemctl status nginx          # status & log terakhir
systemctl start nginx
systemctl stop nginx
systemctl restart php8.3-fpm
systemctl enable nginx          # auto-start saat boot
systemctl disable nginx
systemctl --failed              # service yang gagal
```

- `enable` membuat service hidup otomatis setelah reboot.
- Perintah system service umumnya butuh `sudo`.

### Logs

```bash
journalctl -u nginx -f          # log service systemd, follow
journalctl -u myapp --since "1 hour ago"
tail -f /var/log/nginx/error.log   # log file klasik
tail -n 100 /var/log/nginx/access.log
```

- `-f` = follow (ikuti terus); `-n 100` = 100 baris terakhir.
- Log adalah sumber pertama fakta saat produksi bermasalah.

### Environment variables

```bash
export DB_HOST=localhost        # sementara (session)
echo $DB_HOST
env | grep DB                   # lihat env var
source .env                     # muat file .env
```

- Dalam kode baca via `os.environ.get("DB_HOST")` (Python) / `env('DB_HOST')` (Laravel).
- Secrets (password, key) diambil dari env/secret manager, **bukan** di-commit.

### Filesystem

```text
/        root
/etc/    konfigurasi sistem
/var/    data berubah (log, upload)
/home/   data user
/tmp/    file temporer
/opt/    software opsional
/usr/    software sistem
```

---

## Analogy

Service = departemen yang selalu buka (nginx = pintu depan, DB = gudang). `systemctl` = manajer yang menyalakan/mematikan departemen dan memastikannya buka saat gedung menyala (enable). Log = buku catatan semua kejadian tiap departemen. Env var = papan pengaturan umum yang dibaca semua, supaya kredensial tidak tertulis di dinding (hardcode).

---

## Examples

```bash
# service down setelah reboot?
systemctl status nginx
journalctl -u nginx --since "10 minutes ago"
```

```bash
# cek log error aplikasi
tail -n 100 /var/log/nginx/error.log
```

```bash
# cek env var DB
env | grep DB
```

---

## Code — skenario deploy aman

```bash
cd /var/www/myapp
git pull origin main
composer install --no-dev
php artisan migrate --force
chown -R www-data:www-data storage/
systemctl reload nginx    # muat config tanpa restart total
```

Kredensial berasal dari `.env`/secret manager, tidak pernah di hardcode:

```bash
export DB_PASSWORD=...   # dari secret manager, bukan di repo
````

---

## Explanation

- `systemctl reload` vs `restart`: reload hanya baca ulang config (lebih ringan, tidak putus koneksi); restart mulai dari nol.
- `journalctl` adalah log bawa-an systemd; cukup `-u <service>` untuk fokus satu service.
- Jangan hardcode config — baca dari env var/service config agar bisa ganti antar environment tanpa edit kode.
- Jangan pernah meng-commit file berisi `password`/`API_KEY`; gunakan `.env` yang di-gitignore.
- Memahami path filesystem membantu menemukan file konfigurasi & data.

---

## Common Mistakes

1. Lupa `sudo` untuk `systemctl` / file sistem.
2. Meng-commit config berisi credential.
3. `tail` file log kosong padahal service pakai `journalctl`.
4. `systemctl restart` padahal cukup `reload` (downtime tak perlu).
5. Env var diset manual di tiap terminal tapi tidak dipersist di service config.

---

## Manual Exercises

### Exercise 1
`systemctl status` satu service (nginx/mysql) dan baca log error terakhir.

### Exercise 2
Baca 50 baris terakhir file log nginx dengan `tail -n 50`.

### Exercise 3
Set `export DB_HOST=localhost`, lalu `echo $DB_HOST` dan `env | grep DB`.

### Exercise 4
Muat `.env` dengan `source` dan pastikan variabelnya terbaca.

### Exercise 5
Jalankan aplikasi yang membaca `DB_HOST` dari env var (Python: `os.environ.get`).

---

## Challenge — Minimal Exercise

Tulis di Notes: bagaimana kamu men-debug "aplikasi hidup tapi tidak bisa konek DB" menggunakan (a) `systemctl status`, (b) log service, dan (c) pengecekan env var.

---

## Reflection

1. Apa peran `systemctl enable`?
2. Bedakan `journalctl` dan `tail file`.
3. Bedakan `reload` vs `restart`.
4. Mengapa credential tidak boleh hardcode?
5. Apa fungsi path `/etc/` dan `/var/`?

---

## Checklist

- [ ] Bisa `systemctl` status/start/restart/enable
- [ ] Bisa baca log dengan `journalctl` & `tail`
- [ ] Bisa set/muat env var
- [ ] Paham filesystem Linux dasar
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```bash
export DB_HOST=localhost
echo $DB_HOST          # localhost
env | grep DB          # DB_HOST=localhost
```

Exercise 4

```bash
echo "DB_PORT=5432" >> .env
source .env
echo $DB_PORT          # 5432
```

Exercise 5

```python
import os
print(os.environ.get("DB_HOST"))
```

</details>
