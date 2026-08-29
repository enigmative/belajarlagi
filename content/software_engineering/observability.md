# Observability — Logging, Metrics, Tracing, Monitoring, Alerting

## Learning Objective

- Memahami Logging, Metrics, Tracing, Monitoring, Alerting
- Diagnosa "produksi API lambat"
- Menulis log yang berguna
- Metrik kunci (latency, error, saturation)

---

## Theory

### Lima pilar (praktik)

| Pilar | Apa | Contoh |
|-------|-----|--------|
| **Logging** | peristiwa tekstual | error stack, request detail |
| **Metrics** | angka terukur waktu-rutin | QPS, latency, error rate |
| **Tracing** | jejak satu request lintas service | span "db.query", "api.call" |
| **Monitoring** | visualisasi + dashboard | Grafana panel |
| **Alerting** | notif saat ambang dilanggar | Slack "error rate > 5%" |

### Metrik golden signals

```text
Latency   — berapa lama request
Traffic   — berapa banyak request
Errors    — berapa yang gagal
Saturation— seberapa penuh resource (CPU/mem/connection)
```

---

## Analogy

GPS untuk sistem: tanpa logging kamu buta apa yang terjadi; metrics = speedometer; tracing = rute yang diambil mobil; dashboard = papan navigasi; alert = pemberitahuan "menyimpang dari rute". Kamu tahu persis di mana lambat, bukan menebak.

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

---

## Code — struktur log yang berguna

```json
{"level":"WARN","msg":"slow query","query":"SELECT ...","duration_ms":1200,"correlation_id":"abc123"}
```

- Sertakan `correlation_id` agar satu request terlacak di semua service/log.
- Log di key value/JSON, bukan narasi panjang.
- Level: DEBUG < INFO < WARN < ERROR.

---

## Explanation

- Diagnosis dimulai: **lihat metrik** (latency naik sejak kapan & untuk endpoint mana?).
- Lalu **tracing**: request mana yang lambat, komponen mana (DB? network? app code?).
- Sigra **log**: baris mana error, kode status, message.
- Jangan langsung "tambah server" — mungkin hanya query N+1, cache miss, atau deadlock.
- Alert harus actionable: threshold jelas, channel (email/pager), owner.

---

## Common Mistakes

1. Log tanpa struct — tidak bisa di-query/parse.
2. Tidak ada metrics — menebak tanpa data.
3. Alert too banyak (alert fatigue) → diabaikan saat benar-benar penting.
4. Tanpa trace id — jejak tersebar di banyak service tak cocok.
5. Menambahkan resource sebelum menganalisis penyebab.

---

## Manual Exercises

### Exercise 1
Tambahkan middleware logging durasi di FastAPI.

### Exercise 2
Tambah metrik sederhana (count request per path) di store in-memory.

### Exercise 3
Struktur log JSON dengan correlation_id.

### Exercise 4
Rancang dashboard: 3 grafik (latency, error, cpu).

### Exercise 5
Buat alert rule "error rate > 5% dalam 5 menit".

---

## Challenge — Minimal Exercise

Tulis runbook singkat untuk "API lambat": langkah diagnosis (metrik → tracing → log → perbaiki) dan apa yang kamu periksa dulu. Simpan di Notes.

---

## Reflection

1. Apa beda logging, metrics, tracing?
2. Apa golden signals itu?
3. Kenapa log harus terstruktur?
4. Kenapa alert harus sedikit?
5. Apa langkah pertama saat API lambat?

---

## Checklist

- [ ] Bisa log terstruktur
- [ ] Paham metric & tracing
- [ ] Bisa monitoring dashboard
- [ ] Bisa alerting
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

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

Exercise 5

```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status="5xx"}[5m]) > 0.05
for: 5m
```

</details>