# System Design — Scaling, Replication & Availability

## Learning Objective

- Memahami scaling vertikal vs horizontal
- Replication & failover database
- Fault tolerance & single point of failure
- Rate limiting & timeout
- Mengukur penyebab sebelum menambah resource

---

## Theory

### Scaling

```text
Vertical:   1 server makin besar (RAM/CPU naik) — terbatas, mahal
Horizontal: banyak server kecil + load balancer — scalable, kompleks
```

- Vertikal simpel sampai batas fisik & biaya.
- Horizontal butuh stateless app + load balancer + shared state.

### Replication (DB)

```text
[Primary (tulis)] ← replication → [Replica (baca)]
```

- Replica untuk menambah kapasitas baca.
- Failover: jika primary mati, replica naik jadi primary.
- Tulis tetap ke primary.

### Fault tolerance & single point of failure (SPOF)

- Satu komponen yang jika mati menjatuhkan seluruh sistem = SPOF.
- Fault tolerance = redundansi agar satu node mati tidak mematikan layanan.

### Rate limiting & timeout

- **Rate limit** — batasi request (anti abuse, lindungi resource).
- **Timeout** — batasi waktu tunggu; satu request lambat tidak menggantung selamanya.

---

## Analogy

Restoran: vertical = satu koki diperbesar (lebih cekatan/banyak tangan — sampai batas). Horizontal = banyak koki + resepsionis (load balancer) membagi pesanan. Replication = resep (data) disalin ke dapur cadangan; kalau dapur utama kebakaran, dapur cadangan lanjut melayani (failover). SPOF = satu kasir satu-satunya — kalau dia izin, semua berhenti.

---

## Examples — memilih scaling

```text
Traffic naik 2x, CPU satu server 90%:
  Vertical: naik RAM/CPU — cepat, tapi terbatas & mahal.
  Horizontal: tambah 1 server + LB — skalabel, tapi app harus stateless.
```

```text
Baca banyak, tulis sedikit:
  Replication → baca ke replica, tulis ke primary.
```

```text
Login: rate limit 10/menit/IP.
Search: rate limit 60/menit/user + cache 30 detik.
```

---

## Code — konsep (docker-compose)

```yaml
services:
  web:
    image: app
    deploy:
      replicas: 3              # horizontal app
  db:
    image: postgres:16
    # primary + replica dikonfigurasi terpisah
```

---

## Explanation

- **Ukur dulu**: endpoint/kriteria mana yang lambat; jangan tebak lalu tambah server.
- Proses naik traffic: profil → identifikasi bottleneck → cache/optimasi → baru scale.
- Horizontal butuh app **stateless** (session/state di luar app: Redis/DB) supaya request bisa lintas server.
- Rate limit & timeout mencegah satu request/user menjatuhkan semuanya.
- Replication menambah baca & failover, tapi naikkan kompleksitas sinkronisasi.

---

## Common Mistakes

1. Menambah resource tanpa mengukur penyebab.
2. App menyimpan state lokal → tidak bisa horizontal scale.
3. Single point of failure (satu DB tanpa replica/failover).
4. Rate limit dipasang tanpa memahami traffic normal (blok user sah).
5. Langsung scale vertikal mahal padahal caching/query fix cukup.

---

## Manual Exercises

### Exercise 1
Jelaskan kapan vertical vs horizontal scaling tepat.

### Exercise 2
Identifikasi single point of failure di arsitektur proyekmu.

### Exercise 3
Desain replication (primary+replica) untuk DB dan jelaskan alur baca/tulis.

### Exercise 4
Buat rate limit untuk endpoint login & search (nilai & unit).

### Exercise 5
Tulis langkah profiling sebelum menambah server saat API lambat.

---

## Challenge — Minimal Exercise

API mulai lambat saat user 10k. Tulis rencana: (a) cara mengukur penyebab, (b) optimasi yang dicoba sebelum scaling, (c) desain scaling/availability (LB, replication, failover). Simpan di Notes.

---

## Reflection

1. Apa beda vertical & horizontal scaling?
2. Bagaimana replication membantu?
3. Apa itu single point of failure?
4. Mengapa app harus stateless untuk horizontal scale?
5. Kenapa ukur dulu sebelum tambah resource?

---

## Checklist

- [ ] Paham vertical/horizontal scaling
- [ ] Paham replication & failover
- [ ] Bisa identifikasi SPOF
- [ ] Bisa rate limit & timeout
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

Vertical = cukup & simpel bila bottleneck CPU/RAM satu server (sampai batas). Horizontal = perlu load balancing & stateless; dipakai saat traffic tinggi/naik-naik atau butuh failover.

Exercise 4

Login: 10/menit/IP. Search: 60/menit/user + hasil cache 30 detik.

Exercise 5

`top`/profiler → cek endpoint lambda → lihat query (N+1?) & cache → baru tambah server.

</details>
