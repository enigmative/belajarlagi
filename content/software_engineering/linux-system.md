# Linux — Process, Service, Logs, & Environment

## Learning Objective

- Melacak process (ps, top, kill)
- Mengelola service
- Membaca logs
- Environment variable
- Memahami filesystem Linux dasar

---

## Theory

### Process

```bash
ps aux                # semua process
top / htop            # monitor realtime
kill 1234             # matikan process
kill -9 1234          # paksa (terakhir, bisa rusak data)
pgrep -f uvicorn
```

Context: setiap request app = satu atau lebih process; `php-fpm`, `nginx`, `uvicorn` berjalan sebagai service.

### Service

```bash
systemctl status nginx
systemctl start nginx
systemctl enable nginx      # auto-start saat boot
systemctl restart php8.3-fpm
journalctl -u nginx -f      # log service dalam systemd
```

### Port & koneksi

```bash
ss -tlnp                    # port yang listening
lsof -i :8000               # process yang memakai port 8000
```

### Logs

```bash
tail -f /var/log/nginx/error.log
journalctl -u myapp --since "1 hour ago"
```

### Environment variable

```bash
export DB_HOST=localhost        # sementara
echo $DB_HOST
source .env                     # memuat file env
env | grep DB                   # lihat
```

### Filesystem

```text
/         root
/etc/     konfigurasi
/var/     data berubah (log, upload)
/home/    user data
/tmp/     temporer
/opt/     software opsional
```

---

## Analogy

Server = gedung dengan: process = pekerja masing-masing; service = departemen yang selalu buka; port = pintu dengan nomor (8000 = dapur, 3306 = gudang DB); logs = buku catatan semua yang terjadi; env var = papan pengaturan umum yang dibaca semua departemen.

---

## Examples

```bash
# diagnose "server lambat"
top                          # CPU/mem tinggi?
ss -tlnp                     # port yang dipakai
tail -n 100 /var/log/nginx/error.log
journalctl -u myapp -f
ps aux | grep -i php         # apakah worker sebanyaknya?
```

---

## Code — health check sederhana

```bash
curl -fsS http://127.0.0.1:8000/api/dashboard | head -c 200 || echo "DOWN"
```

---

## Explanation

- `kill` normal menyuruh process berhenti rapi; `-9` paksa — pakai sebagai jalan terakhir.
- `systemctl` untuk service yang dikelola systemd (ubuntu modern).
- `ss -tlnp` menjawab "siapa yang pegang port 8000?".
- Log adalah detektif utama: mulai dari Error → trace waktu → temukan pemicu.
- Jangan hardcode config; baca dari env var/service config.

---

## Common Mistakes

1. `kill -9` spontan tanpa mencoba `kill` lembut dulu.
2. Lupa `sudo systemctl ...`.
3. Cari port dengan `netstat` lama padahal `ss` lebih tepat.
4. Tidak melihat logs saat "tidak ada yang salah tapi lambat".
5. Config di-commit berisi credential.

---

## Manual Exercises

### Exercise 1
`top` sejenak, catat process dengan CPU tertinggi.

### Exercise 2
Cari process yang memakai port 8000 (`ss -tlnp`).

### Exercise 3
Baca 50 baris terakhir log nginx/uvicorn.

### Exercise 4
Jalankan app dengan `DB_HOST` dari env var.

### Exercise 5
`systemctl status` satu service (nginx/mysql).

---

## Challenge — Minimal Exercise

Lacak alasan "API lambat" dengan tool di atas: tulis langkah diagnosismu (top → ss → logs) di Notes.

---

## Reflection

1. Apa beda `kill` vs `kill -9`?
2. Apa peran service `enable`?
3. Bagaimana membaca port yang dipakai?
4. Kenapa log penting untuk debugging produksi?
5. Bagaimana env var menjaga konfigurasi tetap aman?

---

## Checklist

- [ ] Bisa ps/top/kill
- [ ] Bisa systemctl service
- [ ] Bisa ss/lsof
- [ ] Bisa baca logs
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```bash
ss -tlnp | grep 8000
```

Exercise 4

```bash
export DB_HOST=localhost
python app.py
# di kode: os.environ.get("DB_HOST")
```

</details>