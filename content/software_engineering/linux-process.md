# Linux — Process, Port & Resources

## Learning Objective

- Melacak process (ps, top/htop, pgrep)
- Memahami status process (running, stopped, zombie)
- Membunuh process dengan benar (kill vs kill -9 / SIGTERM vs SIGKILL)
- Mendiagnosis resource (CPU, memori) yang dipakai process
- Menemukan process yang memegang port tertentu (ss, lsof)

---

## Theory

### Melihat process

```bash
ps aux                # semua process + pemakai + CPU/mem
ps -ef | grep php     # filter berdasar nama
pgrep -f uvicorn      # dapatkan PID dari nama
top                   # realtime, tekan q untuk keluar
htop                  # versi interaktif (lebih nyaman)
```

Kolom `PID` = identitas process; `USER` = pemilik; `%CPU`/`%MEM` = pemakaian; `STAT` = status.

### Status process (`STAT`)

| Kode | Arti |
|------|------|
| `S` | sleeping (menunggu) — normal |
| `R` | running |
| `Z` | zombie (sudah mati, belum dibersihkan induknya) |
| `T` | stopped |
| `D` | uninterruptible (biasanya I/O) |

### Menghentikan process

```bash
kill 1234             # default SIGTERM — minta berhenti rapi
kill -15 1234         # sama, SIGTERM
kill -9 1234          # SIGKILL — paksa, tidak bisa ditolak
```

- `SIGTERM` (15): memberi kesempatan membersihkan (save, close).
- `SIGKILL` (9): langsung di-terminate OS — jalan terakhir, bisa merusak data.
- Selalu coba SIGTERM dulu; `-9` hanya bila benar-benar buntu.

### Port & koneksi

```bash
ss -tlnp              # port yang listening (tcp) + process
ss -tunlp | grep 8000 # port 8000 dijabat siapa
lsof -i :8000         # process yang memakai 8000
```

- `ss` menggantikan `netstat` lama.
- Satu port hanya boleh dipakai satu process pada satu waktu.
- "Address already in use" = port masih dipegang process lama.

---

## Analogy

Process = pekerja di gedung server. `ps` = daftar absen semua pekerja; `top` = papan skor siapa yang paling sibuk (CPU) & paling banyak bawa barang (mem). `kill` = menyuruh pekerja berhenti; `kill -9` = mengeluarkan paksa tanpa memberi waktu merapikan meja. `ss -tlnp` = daftar pintu (port) dan siapa yang menjaga tiap pintu.

---

## Examples

```bash
# kenapa API lambat? cek process makan CPU
top
# lalu sempitkan ke worker app
ps aux | grep -i uvicorn
```

```bash
# port 8000 sudah dipakai, siapa?
ss -tlnp | grep 8000
```

```bash
# matikan process dengan lembut lalu paksa bila perlu
kill 4321
sleep 2
kill -9 4321   # hanya jika masih hidup
```

---

## Code — skenario diagnosa

```bash
# 1. cek keseluruhan
top

# 2. process php worker
ps aux | grep -i php

# 3. port yang dipakai app
ss -tlnp

# 4. matikan yang buntu
kill -9 <PID>
```

---

## Explanation

- Sebuah request aplikasi = satu atau lebih process; `php-fpm`, `nginx`, `uvicorn` masing-masing berjalan sebagai process.
- `-9` menghilangkan kesempatan menulis buffer/state → resiko korup data; pakai sebagai last resort.
- Zombie process (STAT `Z`) normal sementara; kalau menumpuk, biasanya induknya bug.
- Ketika "port 8000 dipakai", jangan paksa random — identifikasi PID-nya dulu dengan `ss -tlnp`.
- Melihat CPU vs memori membantu menebak: CPU tinggi = kerja berat; memori tinggi = boros/bocor.

---

## Common Mistakes

1. Langsung `kill -9` tanpa `kill` lembut dulu.
2. Membunuh process sistem (nginx/php-fpm) tanpa sadar dampak layanan.
3. Pakai `netstat` lama padahal `ss` lebih tepat.
4. Tidak melihat PID: `kill 8000` salah, harus nomor PID.
5. Mengira `top` = proses tak berhenti; perlu `q` untuk keluar.

---

## Manual Exercises

### Exercise 1
Jalankan `top` sejenak, catat 3 process dengan `%CPU` tertinggi dan statusnya.

### Exercise 2
Jalankan server kecil (mis. `python -m http.server 8000`), lalu cari process yang memegang port 8000 dengan `ss -tlnp`.

### Exercise 3
Temukan PID process `http.server` dan hentikan dengan `kill` (SIGTERM), verifikasi dengan `ps`.

### Exercise 4
Gunakan `ps aux | grep` untuk melihat berapa banyak worker `php/python` berjalan.

### Exercise 5
Jika SIGTERM tidak berhenti, gunakan `kill -9` — tulis di Notes kenapa itu jalan terakhir.

---

## Challenge — Minimal Exercise

Diagnosis singkat: aplikasi lokal di port 8000 tidak merespons. Tulis langkah untuk (a) menemukan PID-nya, (b) melihat pemakaian CPU/mem, dan (c) menghentikannya. Simpan langkahnya di Notes.

---

## Reflection

1. Apa beda `SIGTERM` dan `SIGKILL`?
2. Kapan memakai `kill -9`?
3. Apa arti kolom `STAT` di `ps`?
4. Bagaimana menemukan process yang memegang port 8000?
5. Mengapa membunuh process sistem harus hati-hati?

---

## Checklist

- [ ] Bisa `ps`/`top`/`pgrep`
- [ ] Bisa `ss -tlnp`/`lsof`
- [ ] Bisa `kill` (SIGTERM) & `kill -9`
- [ ] Bisa membaca status & resource process
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```bash
python -m http.server 8000 &
ss -tlnp | grep 8000
```

Exercise 3

```bash
pgrep -f http.server
kill <PID>
ps -ef | grep http.server   # harus sudah hilang
```

Exercise 5

```bash
kill -9 <PID>   # karena SIGTERM diabaikan/buntu
```

</details>
