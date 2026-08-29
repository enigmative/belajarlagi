# Queue & Worker — Job Asinkron

## Learning Objective

- Memahami Queue, Job, Worker, Retry
- Alur User → Request → Queue → Worker → Proses
- Implementasi job di Laravel (dan konsep di FastAPI)
- Menangani kegagalan: retry, backoff, failed jobs
- Menjalankan worker di produksi & idempotensi job

---

## Theory

### Konsep

```text
User
  ↓
Request (disimpan ke Queue)
  ↓
Worker (proses antrean)
  ↓
Finish (kirim email / generate report / notif)
```

- **Queue** = daftar kerja yang menunggu.
- **Job** = satu unit kerja.
- **Worker** = konsumen yang menjalankan job.
- **Retry** = ulangi job yang gagal (sementara).
- **Failed job** = job yang buntu total setelah percobaan.

### Kenapa queue?

Kerja lambat (kirim email, generate laporan, resize gambar) dipindah dari request → respons API tetap cepat, tidak menunggu selesai.

### Laravel

```php
dispatch(new SendWelcomeEmail($user));

// .env
QUEUE_CONNECTION=database   // atau redis

php artisan queue:work       // jalankan worker
```

---

## Analogy

Queue = antrean kasir: pelanggan (job) masuk antrean, kasir (worker) melayani satu-satu. Kalau transaksi bermasalah (gagal), dipanggil lagi (retry) beberapa kali; kalau tetap gagal, dicatat (failed jobs) untuk ditangani manual. Request user tidak menunggu — sudah "diantrekan" dan langsung dapat respons.

---

## Examples

```php
// Laravel job dengan retry & backoff
class SendReport implements ShouldQueue {
    public $tries = 3;                 // retry 3x
    public $backoff = [5, 15, 60];     // jeda antar coba (detik)
    public function handle() {
        // generate & kirim laporan
    }
}
dispatch(new SendReport($employeeId));
```

```python
# FastAPI: pakai library rq / celery
# from redis import Redis
# from rq import Queue
# q = Queue(connection=Redis())
# q.enqueue(send_email, user_id=1)
```

---

## Code — alur worker (Laravel)

```text
1. Request → dispatch(new Job)   (respons cepat, tanpa menunggu)
2. Queue backend menyimpan job
3. `php artisan queue:work` menarik & menjalankan job
4. Sukses → hapus dari antrean
5. Gagal → retry sampai `$tries`, lalu masuk ke failed jobs
```

```bash
QUEUE_CONNECTION=database
php artisan queue:work
php artisan queue:failed   # daftar failed jobs
```

---

## Explanation

- Queue memindahkan kerja lambat dari request → respons tetap cepat.
- **Idempotensi**: job harus aman dijalankan ulang (retry) tanpa efek ganda — misal cek sudah terkirim sebelum kirim email.
- Error sementara (DB timeout, API down) → retry dengan backoff.
- Error permanen (input invalid) → jangan retry selamanya; tandai failed.
- Worker di prod dijalankan via **supervisor/systemd** agar auto-restart, bukan manual.
- Scheduler memicu job berkala (laporan harian) — Laravel Scheduler / cron.

---

## Common Mistakes

1. `QUEUE_CONNECTION` tetap `sync` → job jalan sinkron (meniadakan manfaat queue).
2. Worker tidak berjalan → antrean menumpuk tak diproses.
3. Job tidak idempotent → retry = operasi ganda (email ganda, transfer dobel).
4. Retry tanpa batas untuk error permanen → antrean macet.
5. Worker manual di prod → mati saat server restart.

---

## Manual Exercises

### Exercise 1
Buat job `SendNotifier` (ShouldQueue) dan `dispatch`-nya.

### Exercise 2
Jalankan worker `php artisan queue:work` dan amati antrean terproses.

### Exercise 3
Set `$tries = 3` + `$backoff`; buat job yang gagal sementara lalu sukses — amati retry.

### Exercise 4
Cek `failed jobs` setelah job buntu total dan pahami cara menanganinya.

### Exercise 5
Konfigurasi `QUEUE_CONNECTION=redis` (atau database) dan bedakan dengan `sync`.

---

## Challenge — Minimal Exercise

Buat job `SendNotifier` (ShouldQueue, tries 3, backoff [5,15,60]) yang idempotent (cek sudah terkirim sebelum kirim), lalu `dispatch`. Tulis cara menjalankan worker & menangani failed job di Notes.

---

## Reflection

1. Apa perbedaan Queue vs Cache?
2. Mengapa job harus idempotent saat retry?
3. Peran worker dalam memproses antrean?
4. Bagaimana menangani job yang gagal permanen?
5. Bagaimana worker dijalankan di produksi?

---

## Checklist

- [ ] Paham queue/job/worker
- [ ] Bisa buat & dispatch job
- [ ] Bisa set retry + backoff
- [ ] Bisa kelola failed jobs
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1-2

```php
php artisan make:job SendNotifier
dispatch(new SendNotifier($user));
```

```bash
QUEUE_CONNECTION=database
php artisan queue:work
```

Exercise 3

```php
public $tries = 3;
public $backoff = [5, 15, 60];
```

</details>
