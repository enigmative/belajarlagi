# Redis — Caching & Session

## Learning Objective

- Memahami Redis sebagai database in-memory
- Operasi dasar: set, get, expire (TTL), del, incr
- Menggunakan cache untuk query berulang
- Session store & rate limiter dengan Redis
- Menghindari stale cache & RAM penuh

---

## Theory

### Redis

Database in-memory (RAM) untuk data yang sering dibaca — jauh lebih cepat dari disk.

```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
redis-cli
```

```text
SET cache:user:1 "John"
GET cache:user:1
EXPIRE cache:user:1 3600      # TTL 1 jam
DEL cache:user:1
INCR counter:visits
```

- **TTL** (time-to-live) membuat key otomatis dihapus — kunci menghindari RAM penuh & stale.
- `INCR` cocok untuk counter (rate limiter, hit).

### Kapan cache

- Query yang dijalankan berulang dengan data jarang berubah.
- Hasil komputasi mahal.
- Baca jauh lebih sering daripada tulis.

### Laravel

```php
$users = Cache::remember('users.all', 600, fn () => User::all());
```

- `600` = detik TTL; kunci `users.all`.
- FastAPI: library seperti `redis-py` / `aioredis`.

---

## Analogy

Redis = "catatan tempel instan" di RAM dekat tangan — super cepat dibaca/ditulis, beda dari lemari dokumen (disk DB) yang lambat dibuka. TTL = catatan tempel yang otomatis dibuang setelah waktu tertentu, supaya tidak menumpuk dan tidak usang.

---

## Examples

```python
import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

r.set("cache:profile:1", "John", ex=600)
print(r.get("cache:profile:1"))   # "John"
```

```php
// Laravel — session di Redis
// config/session.php 'driver' => 'redis'
$request->session()->put('user_id', 1);
```

```text
# rate limiter — 5 request per 60 detik per user
INCR rate:user:1
EXPIRE rate:user:1 60
# jika nilai > 5 → tolak
```

---

## Code — pola cache-aside

```text
1. Cek cache (key = ...)
2. Ada? → kembalikan (cache hit)
3. Tidak → query DB
4. Simpan hasil ke cache dengan TTL
5. Kembalikan
```

```python
key = f"profile:{user_id}"
data = r.get(key)
if data is not None:
    return data
data = db.query(...)
r.set(key, data, ex=600)
return data
```

---

## Explanation

- Redis dipuji untuk: cache query berulang, session store, rate limiter, queue backend.
- Cache mengurangi beban DB untuk data baca sering, tapi harus dengan TTL → kalau tidak stale & RAM penuh.
- **Cache invalidation** saat data berubah: hapus key (`DEL`) atau update agar tidak menampilkan data lama.
- Jangan cache data yang berubah tiap detik & sensitif tanpa kontrol.
- Counter (`INCR` + `EXPIRE`) jadi dasar rate limiter ringan.

---

## Common Mistakes

1. Cache tanpa TTL → RAM penuh / data stale.
2. Cache data yang sering berubah tanpa invalidation → user lihat data lama.
3. Mencache dalam semua hal termasuk data unik per-user yang jarang dipakai.
4. Tidak mengukur hot path — cache di tempat yang tidak perlu.
5. Key tidak konsisten/berantakan (sulit di-debug & dibersihkan).

---

## Manual Exercises

### Exercise 1
Jalankan Redis via docker; `set`, `get`, `expire` 60 detik.

### Exercise 2
Cache query profil user selama 10 menit (Laravel `Cache::remember` atau redis-py).

### Exercise 3
Buat counter `INCR` untuk hit endpoint dan cek nilainya.

### Exercise 4
Buat rate limiter sederhana (5 request/60s per user) pakai `INCR`+`EXPIRE`.

### Exercise 5
Hapus key saat data di-update (invalidation) dan jelaskan kenapa perlu.

---

## Challenge — Minimal Exercise

Endpoint `/api/user/{id}` sering diakses; gunakan Redis cache-aside dengan TTL 600 detik dan **invalidation saat user di-update**. Tulis implementasinya (Laravel atau FastAPI) di Notes.

---

## Reflection

1. Kenapa Redis lebih cepat dari DB disk?
2. Mengapa cache perlu TTL?
3. Apa itu cache invalidation & mengapa penting?
4. Bagaimana `INCR` membantu rate limiting?
5. Kapan cache sebaiknya TIDAK dipakai?

---

## Checklist

- [ ] Bisa `set`/`get`/`expire`/`del`/`incr`
- [ ] Bisa cache-aside
- [ ] Bisa session store
- [ ] Bisa rate limiter sederhana
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
redis-cli
SET cache:user:1 "John"
EXPIRE cache:user:1 60
GET cache:user:1
```

Exercise 4

```text
INCR rate:user:1
EXPIRE rate:user:1 60
# nilai > 5 → tolak
```

</details>
