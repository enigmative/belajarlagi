# Observability — Structured Logging & Metrics

## Learning Objective

- Memahami Logging & Metrics sebagai dasar observability
- Menulis log terstruktur yang bisa di-query
- Level log & correlation id
- Metrik golden signals (latency, traffic, errors, saturation)
- Mengumpulkan metrik sederhana

---

## Theory

### Logging

Peristiwa tekstual: error stack, request detail, event aplikasi.

- Log harus **terstruktur** (JSON/key-value), bukan narasi panjang.
- Level: `DEBUG < INFO < WARN < ERROR`.
- Sertakan `correlation_id` agar satu request terlacak di banyak service.

### Metrics

Angka terukur waktu-rutin: QPS, latency, error rate.

### Golden signals

```text
Latency    — berapa lama request
Traffic    — berapa banyak request
Errors     — berapa yang gagal
Saturation — seberapa penuh resource (CPU/mem/connection)
```

---

## Analogy

Tanpa observability kamu buta apa yang terjadi — "mengemudi mobil tanpa dashboard". Logging = buku catatan kejadian; metrics = speedometer & odometer (kecepatan, jarak, jumlah). Kamu tahu berapa banyak yang masuk (traffic), seberapa cepat (latency), berapa yang gagal (errors), dan seberapa penuh tangki (saturation).

---

## Examples

```python
# FastAPI — log request (middleware)
import time, logging

@app.middleware("http")
async def log_req(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)
    logging.info(f"{request.method} {request.url.path} {response.status_code} {duration}s")
    return response
```

```php
// Laravel
Log::info('order created', ['order_id' => $order->id]);
```

### Log terstruktur

```json
{"level":"WARN","msg":"slow query","query":"SELECT ...","duration_ms":1200,"correlation_id":"abc123"}
```

---

## Code — metrik sederhana

```python
COUNTS = {}

@app.middleware("http")
async def count_req(request, call_next):
    resp = await call_next(request)
    p = request.url.path
    COUNTS[p] = COUNTS.get(p, 0) + 1
    return resp
```

- `COUNTS` bisa diekspos di endpoint `/metrics`.
- Untuk produksi gunakan tools proper (Prometheus + client library).

---

## Explanation

- Diagnosis dimulai dari **metrik**: latency naik sejak kapan & untuk endpoint apa?
- Lalu lihat **log** endpoint tersebut: baris error, kode status, message.
- Log terstruktur memungkinkan query/filter otomatis (grep/pipeline/elk).
- `correlation_id` menyatukan request melintasi service & log.
- Metrik tanpa cara membaca (dashboard) tidak berguna — pasangkan.

---

## Common Mistakes

1. Log tanpa struktur → tidak dapat di-query/parse.
2. Tidak ada metrics → menebak tanpa data.
3. Log berisi data sensitif (password, token).
4. Log tak ada `correlation_id` → jejak tersebar tak cocok.
5. Metrik dikumpulkan tapi tidak dipajang/dianalisis.

---

## Manual Exercises

### Exercise 1
Tambahkan middleware logging durasi di FastAPI.

### Exercise 2
Buat metrik sederhana (count request per path) di store in-memory.

### Exercise 3
Struktur log JSON dengan `correlation_id`.

### Exercise 4
Catat golden signals untuk satu endpoint (latency, error rate).

### Exercise 5
Ekspos metrik di endpoint `/metrics`.

---

## Challenge — Minimal Exercise

Tambahkan structured logging (JSON + correlation_id) dan hitung metrik per-path untuk API proyek ini. Tulis contoh log & metrik yang dihasilkan di Notes.

---

## Reflection

1. Apa beda logging dan metrics?
2. Mengapa log harus terstruktur?
3. Apa itu correlation_id & manfaatnya?
4. Apa golden signals itu?
5. Langkah pertama saat API lambat (ukuran/data)?

---

## Checklist

- [ ] Bisa log terstruktur
- [ ] Bisa level log + correlation_id
- [ ] Bisa metrik sederhana
- [ ] Paham golden signals
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```python
import time, logging
@app.middleware("http")
async def log_req(request, call_next):
    start = time.time()
    resp = await call_next(request)
    logging.info(f"{request.method} {request.url.path} {resp.status_code} {round(time.time()-start,3)}s")
    return resp
```

Exercise 2

```python
COUNTS = {}
@app.middleware("http")
async def count_req(request, call_next):
    resp = await call_next(request)
    p = request.url.path
    COUNTS[p] = COUNTS.get(p, 0) + 1
    return resp
```

</details>
