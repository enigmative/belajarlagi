# Redis & Queue

## Learning Objective

- Memahami Redis: cache, session store
- Queue, Job, Worker, Retry
- Alur User → Request → Queue → Worker → Process
- Implementasi di Laravel (dan konsep di FastAPI)

---

## Theory

### Redis

Database in-memory (cepat) untuk data yang sering dibaca:

```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
redis-cli
```

```text
SET cache:user:1 "Amir"
GET cache:user:1
EXPIRE cache:user:1 3600      # TTL
DEL cache:user:1
INCR counter:visits
```

Dipuji untuk: cache query berulang, session store, rate limiter, queue backend.

### Queue & Job

```text
User
  ↓
Request (disimpan ke Queue)
  ↓
Worker (proses antrean)
  ↓
Finish (kirim email / generate report / notif)
```

Queue = daftar kerja; Job = unit kerja; Worker = konsumen; Retry = ulangi gagal.

```php
// Laravel — kirim job ke antrean
dispatch(new SendWelcomeEmail($user));

// .env
QUEUE_CONNECTION=database   // atau redis
php artisan queue:work       // jalankan worker
```

---

## Analogy

Redis = "catatan tempel instan" yang super cepat dibaca ditulis (di RAM), beda dari disk DB. Queue = antrean kasir: pelanggan (job) masuk antrean, kasir (worker) melayani satu-satu; kalau ada masalah (gagal), dipanggil lagi (retry). Request user tidak menunggu selesai — sudah "diantrekan".

---

## Examples

```php
// Laravel job
class SendReport implements ShouldQueue {
    public $tries = 3;                 // retry 3x
    public $backoff = [5, 15, 60];     // jeda detik antar coba
    public function handle() {
        // generate & kirim laporan
    }
}
dispatch(new SendReport($employeeId));
```

```python
# batasan konsep di FastAPI: pakai library seperti rq/celery
# dari rq import Queue
# q = Queue(connection=redis); q.enqueue(send_email, user_id=1)
```

---

## Code — alur worker (Laravel)

```text
1. Request → dispatch(new Job)   (respons cepat, tanpa menunggu)
2. Queue backend menyimpan job
3. `php artisan queue:work` menarik & menjalankan job
4. Sukses → hapus dari antrean
5. Gagal → retry sampai `$tries`, lalu masukkan ke failed jobs
```

---

## Explanation

- Queue memindahkan kerja lambat dari request → response tetap cepat.
- Redis nyaman untuk cache (TTL) & tempat queue.
- Retry meng-handle kegagalan sementara; `failed_jobs` mencatat yang buntu total.
- Worker: `queue:work` di dev; di prod pakai supervisor/systemd supaya auto-restart.
- Scheduler meng-trigger job berkala (mis. laporan harian).

---

## Common Mistakes

1. Queue misconfigured (`QUEUE_CONNECTION` tetap sync) → job jalan sinkron.
2. Worker tidak berjalan → antrean menumpuk.
3. Cache tanpa TTL → RAM penuh/stale data.
4. Job berisi operasi mutating yang tidak idempotent (retry jadi double).
5. Log di worker buang-buang resource.

---

## Manual Exercises

### Exercise 1
Jalankan Redis via docker & set/get + expire.

### Exercise 2
Laravel: buat job + dispatch + `queue:work`.

### Exercise 3
Cache query user 10 menit.

### Exercise 4
Set `$tries` + `$backoff` + tes gagal.

### Exercise 5
Scheduler: job harian (laporan).

---

## Challenge — Minimal Exercise

Buat job `SendNotifier` (ShouldQueue, tries 3, backoff) dan panggil via `dispatch`. Tulis cara menjalankan worker-nya.

---

## Reflection

1. Kenapa Redis lebih cepat dari disk DB?
2. Apa peran queue dalam kestabilan respons API?
3. Mengapa job perlu idempotent saat retry?
4. Apa beda cache vs queue?
5. Bagaimana worker dijalankan di produksi?

---

## Checklist

- [ ] Bisa Redis set/get/expire
- [ ] Bisa job + queue
- [ ] Bisa worker + retry
- - [ ] Paham alur User → Queue → Worker
- - [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```php
php artisan make:job SendWelcomeEmail

app/Exceptions/... maupun service provider yang memanggil:
dispatch(new SendWelcomeEmail($user));
```

```bash
QUEUE_CONNECTION=database
php artisan queue:work
```

Exercise 3

```php
$users = Cache::remember('users.all', 600, fn () => User::all());
```

</details>