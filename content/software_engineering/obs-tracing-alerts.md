# Observability — Tracing, Monitoring & Alerting

## Learning Objective

- Memahami Tracing: jejak satu request lintas service
- Membedakan tracing dari logging/metrics
- Monitoring & dashboard (visualisasi)
- Alerting yang actionable & tidak berisik
- Menulis runbook diagnosis sistem

---

## Theory

### Tracing

Jejak (trace) satu request melintasi service/komponen: span "db.query", "api.call", "http".

```text
Request A
  ├─ span: API Gateway
  ├─ span: db.query (120ms)
  └─ span: api.call payment (340ms)
```

- **Trace** = satu request utuh.
- **Span** = satu bagian kerja dalam trace (dengan durasi).
- Menjawab "bagian mana yang lambat" dalam satu request.

### Monitoring

Visualisasi metrik + dashboards (Grafana, panel). Menjawab "apa yang terjadi sekarang / tren".

### Alerting

Notifikasi saat ambang dilanggar.

```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status="5xx"}[5m]) > 0.05
for: 5m
```

- Threshold jelas; channel (Slack/email/pager); owner.

---

## Analogy

GPS lengkap untuk sistem. Logging = buku catatan; metrics = speedometer; **tracing** = rute yang diambil mobil (urutan lampu hijau/merah = tiap span) sehingga tahu di tikungan mana mobil berhenti; monitoring = papan navigasi besar; alert = pemberitahuan "kamu menyimpang dari rute". Bedanya logging/metrics bilang "ada masalah", tracing bilang "di mana persisnya".

---

## Examples — pemisahan peran

```text
Metrik: latency endpoint /api/users naik jadi 2s sejak 14:00.
Tracing: request terlihat — ternyata span "db.query" 1.8s (query N+1).
Log: detail error/status di endpoint tsb.
```

Tanpa tracing, sulit tahu bagian mana (DB? network? code?) yang lambat.

---

## Code — konsep tracing

```python
# dengan OpenTelemetry (konsep)
with tracer.start_as_current_span("db.query") as span:
    span.set_attribute("db.system", "postgres")
    rows = db.execute(query)
    span.set_attribute("rows", len(rows))
```

```text
trace_id: abc123
 spans:
   - api /orders/list ..... 200ms
   - db.query ............. 180ms  ← bottleneck
   - cache.get .............  5ms
```

---

## Explanation

- **Pilih alat ukur sesuai pertanyaan**: metrik = "seberapa/berapa banyak", tracing = "di mana/kapan satu request", log = "detail apa yang terjadi".
- Monitoring jadi dashboard yang selalu dipantau; tanpa dashboard metrik tak berguna.
- Alert harus **actionable**: threshold, durasi (`for: 5m`), channel, owner. Terlalu banyak alert → deaf (alert fatigue).
- Aturan runbook depannya: metrik → tracing → log → perbaiki; jangan tebak.
- Jangan langsung "tambah server" — mungkin query N+1, cache miss, atau deadlock.

---

## Common Mistakes

1. Tanpa trace id → jejak request tersebar di banyak service tak cocok.
2. Alert terlalu banyak → diabaikan saat penting.
3. Alert tanpa owner/channel jelas → tak ada yang bertanggung jawab.
4. Dashboard penuh tapi tak ada yang membaca.
5. Menambah resource sebelum tracing menunjukkan penyebab.

---

## Manual Exercises

### Exercise 1
Tambahkan trace id (correlation_id) di middleware dan sertakan di semua log request.

### Exercise 2
Simulasikan satu request yang melintasi 2 "span" (app + db) dan catat durasi tiap span.

### Exercise 3
Rancang dashboard: 3 grafik (latency, error, CPU).

### Exercise 4
Buat alert rule "error rate > 5% dalam 5 menit" (Prometheus syntax).

### Exercise 5
Tulis runbook singkat untuk "API lambat".

---

## Challenge — Minimal Exercise

Tulis runbook "API lambat": langkah diagnosis (metrik → tracing → log → perbaiki), apa yang diperiksa pertama, dan alert rule yang menyertainya. Simpan di Notes.

---

## Reflection

1. Apa beda tracing dengan logging/metrik?
2. Apa itu trace & span?
3. Mengapa dashboard penting?
4. Mengapa alert harus sedikit & actionable?
5. Langkah pertama saat API lambat?

---

## Checklist

- [ ] Paham tracing (trace/span)
- [ ] Bisa correlation/trace id
- [ ] Bisa desain dashboard
- [ ] Bisa alert rule
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 4

```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status="5xx"}[5m]) > 0.05
for: 5m
```

</details>
