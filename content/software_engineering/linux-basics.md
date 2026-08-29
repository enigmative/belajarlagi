# Linux — Command Line Dasar

## Learning Objective

- Navigasi & manajemen file
- Membaca/mengedit file dari terminal
- Mencari file & teks (find, grep)
- Perizinan (chmod, chown)
- Jaringan & remote singleton (curl, wget, ssh)

---

## Theory

### Navigasi & file

```bash
pwd                # path sekarang
ls -la             # list lengkap
cd /var/www
mkdir -p app/logs  # buat folder (dengan parent)
cp -r src/ backup/
mv old.php new.php # rename / pindah
rm -rf tmp/        # hapus (hati-hati!)
cat app.php        # print isi file
```

### Search

```bash
grep -rn "ERROR" /var/log/app/
find . -name "*.php" -mtime -1
find / -name "config.env" 2>/dev/null
```

### Permissions

```bash
chmod 755 script.sh       # rwxr-xr-x
chmod 644 file.txt        # rw-r--r--
chown www-data:www-data app/
```

- `r=4, w=2, x=1` per user/group/other.

### Network & remote

```bash
curl -I https://example.com       # header saja
curl -X POST -d "name=John" http://localhost:8000/api/notes
wget https://example.com/file.zip
ssh user@server "ls /var/www"
```

---

## Analogy

Terminal = "remote kontrol server" yang lebih kuat dari GUI. `grep`/`find` = fungsi pencarian raksasa. `chmod` = kunci akses file (baca/tulis/jalankan) untuk pemilik/kelompok/lain. `ssh` = masuk ke komputer lain jarak jauh dengan aman.

---

## Examples

```bash
# cari tempat memory dimakan
top
ps aux | grep php
```

```bash
# log tail realtime
tail -f /var/log/nginx/error.log
```

```bash
# pindahkan hasil ke file
find /var/www -name "*.log" > logs.txt
```

---

## Code — skenario harian dev

```bash
cd /var/www/myapp
git pull origin main
composer install --no-dev
php artisan migrate --force
chown -R www-data:www-data storage/
systemctl reload nginx
```

---

## Explanation

- Command = program; flag `-l -a` = options; argumen = target.
- `|` pipa mengalirkan output satu program ke program berikut.
- `2>/dev/null` membuang output error.
- `man <cmd>` / `cmd --help` = dokumentasi.
- Amankan: semua perintah destruktif (`rm -rf`, `DROP`) — pikir dua kali & checklist.

---

## Common Mistakes

1. `rm -rf` di folder penting tanpa backup.
2. `chmod 777` sembarangan (terbuka semua).
3. Lupa `sudo` untuk file sistem.
4. `grep` vs `find` tertukar (grep cari di isi; find cari nama file).
5. SSH tanpa key (password lemah).

---

## Manual Exercises

### Exercise 1
Navigasi: `cd`, `ls -la`, `pwd`, buat folder nested.

### Exercise 2
`grep -n "selamat" file.txt` — cari teks.

### Exercise 3
`find . -name "*.md"` — cari file.

### Exercise 4
`chmod 755` script dan jalankan.

### Exercise 5
`curl -I` ke `http://127.0.0.1:8000`.

---

## Challenge — Minimal Exercise

Tulis command untuk: cari semua file `.env` di `/home`, tampilkan 100 baris terakhir dari file log, dan ubah permission folder menjadi 755.

---

## Reflection

1. Apa fungsi `|` dalam perintah?
2. Bedakan `chmod` vs `chown`.
3. Kapan pakai `grep` vs `find`?
4. Apa risiko `rm -rf`?
5. Mengapa `chmod 777` buruk?

---

## Checklist

- [ ] Bisa navigasi & file
- [ ] Bisa grep/find
- - [ ] Bisa chmod/chown
- - [ ] Bisa curl/ssh
- - [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 4

```bash
chmod 755 myscript.sh
./myscript.sh   # jalankan
```

Exercise 5

```bash
curl -I http://127.0.0.1:8000
# HTTP/1.1 200 OK
```

</details>