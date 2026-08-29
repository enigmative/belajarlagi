# System Design — Komponen & Arsitektur

## Learning Objective

- Mengenal Load Balancer, App Server, Database, Cache, Queue, Object Storage, CDN, Reverse Proxy
- Memahami scaling horizontal & vertikal
- Caching, Replication, Fault Tolerance, Rate Limiting
- Menganalisis desain skala sederhana

---

## Theory

### Komponen 1

| Komponen | Fungsi |
|----------|--------|
| Load Balancer | sebar request ke banyak server |
| Application Server | jalankan kode/bisnis |
| Database | simpan data (SQL/NoSQL) |
| Cache | RAM untuk data baca sering |
| Queue | job asinkron (email, report) |
| Object Storage | file besar (gambar, video) |
| CDN | konten statis dekat user |
| Reverse Proxy | gateway depan (nginx): TLS, caching, routing |

### Scaling

```text
Vertical:  1 server makin besar (RAM/CPU naik) — terbatas, mahal
Horizontal:  banyak server kecil + load balancer — scalable, kompleks
```

### Availability

- **Replication** — copy DB ke beberapa node (read scaling, failover).
- **Fault Tolerance** — satu node mati, sistem tetap jalan.
- **Rate Limiting** — batasi request (anti abuse).

---

## Analogy

Sistem = restoran. Load balancer = resepsionis membagi pelanggan ke meja. App server = koki. DB = gudang bahan. Cache = meja dekat koki yang cepat diambil. Queue = antrean pesanan. CDN = cabang waralaba dekat pelanggan. Reverse proxy = gerbang depan utama. Satu koki utuh (vertical) vs dapur banyak koki (horizontal).

---

## Examples — 10k user

```text
[User] → CDN (statis)
         ↓
[Reverse Proxy / Nginx]
         ↓
[Load Balancer]
         ↓
[App Server] → [Redis Cache]
         ↓        ↓
[PostgreSQL  (primary) ← replication → replica untuk baca]
         ↓
[Queue] → Worker (kirim email/laporan)
         ↓
[Object Storage] (foto, file)
```

Langkah awalan yang masuk akal untuk skala menengah: monolith app + shared DB + cache + queue + object storage. Jangan microservice dulu.

---

## Code — konsep config (docker-compose)

```yaml
services:
  web:
    image: app
    deploy:
      replicas: 3            # horizontal app
    ports: ["80:80"]

  cache:
    image: redis:7-alpine

  db:
    image: postgres:16
```

---

## Explanation

- Mulailah dari monolith + DB + cache + queue — itu menempuh banyak persen populasi produk.
- Cache mengurangi beban DB untuk data baca sering; tapi hati-hati stale data.
- Replication: baca feat pada replica; tulis tetap primary (master — read/write).
- Rate limit & timeout membuat satu masalah tidak menjatuhkan semuanya.
- Ukuran & skala harus didasari profiling (endpoint mana yang lambat), bukan tebakan.

---

## Common Mistakes

1. Langsung microservice untuk aplikasi kecil.
2. Cache tanpa identifikasi apa/berapa (stale).
3. Single point of failure (satu server DB, no replica).
4. Rate limit dipasang tanpa memahami traffic normal.
5. Menambah resource tanpa mengukur penyebab.

---

## Manual Exercises

### Exercise 1
Gambar arsitektur "Employee Management" versi skala menengah.

### Exercise 2
Jelaskan kapan memakai vertical vs horizontal scaling.

### Exercise 3
Tambahkan cache + queue ke desainmu dan jelaskan gunanya.

### Exercise 4
Identifikasi single point of failure di desainmu.

### Exercise 5
Desain rate limit untuk endpoint login & search.

---

## Challenge — Minimal Exercise

Tulis deskripsi arsitektur 3-tier (web → app → db) untuk API employee, lengkap dengan cache dan load balancer. (Catat di Notes.)

---

## Reflection

1. Apa peran load balancer?
2. Mengapa cache bisa salah/berbahaya?
3. Bagaimana replication membantu?
4. Kapan horizontal scaling dibutuhkan?
5. Apa single point of failure di sistemmu?

---

## Checklist

- [ ] Mengenal tiap komponen
- [ ] Paham scaling
- [ ] Bisa desain sederhana
- [ ] Paham replication & fault tolerance
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

Vertical = cukup & simpel bila bottleneck CPU/RAM satu server (sampai batas). Horizontal = perlu LHA (load balancing) & scalability; dipakai saat traffic tinggi/naik naik atau butuh failover.

Exercise 5

Login: limit 10/menit/IP. Search: limit 60/menit/user + hasil cache 30 detik.

</details>