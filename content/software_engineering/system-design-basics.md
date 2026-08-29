# System Design — Komponen & Arsitektur 3-Tier

## Learning Objective

- Mengenal komponen: Load Balancer, App Server, DB, Cache, Queue, Object Storage, CDN, Reverse Proxy
- Memahami arsitektur 3-tier (web → app → db)
- Mendesain arsitektur menengah (monolith + db + cache + queue)
- Melihat peran tiap komponen & alur request

---

## Theory

### Komponen

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

### Arsitektur 3-tier

```text
Presentation layer (web/API)
   ↓
Application layer (business logic)
   ↓
Data layer (database/storage)
```

- **Presentation** — UI/API entry.
- **Application** — bisnis & orkestrasi.
- **Data** — persistence.

---

## Analogy

Sistem = restoran. Load balancer = resepsionis membagi pelanggan ke meja. App server = koki. DB = gudang bahan. Cache = meja dekat koki yang cepat diambil. Queue = antrean pesanan. CDN = cabang waralaba dekat pelanggan. Reverse proxy = gerbang depan utama. 3-tier = tiga area dapur: tempat terima pesanan (web), tempat memasak (app), gudang (db).

---

## Examples — alur request

```text
[User] → [Reverse Proxy / Nginx] → [App Server] → [PostgreSQL]
                          ↓
                   [Redis Cache]
```

- Request masuk via nginx (TLS, static, routing).
- App server proses bisnis; DB simpan.
- Cache dipakai bila data sering dibaca.

### Skala menengah

```text
[User] → CDN (statis)
         ↓
[Reverse Proxy / Nginx]
         ↓
[Load Balancer]
         ↓
[App Server] → [Redis Cache]
         ↓        ↓
[PostgreSQL  (primary ← replication → replica untuk baca)]
         ↓
[Queue] → Worker (kirim email/laporan)
         ↓
[Object Storage] (foto, file)
```

Langkah awal yang masuk akal: monolith app + shared DB + cache + queue + object storage. Jangan microservice dulu.

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

- Mulai dari **monolith + DB + cache + queue** — itu memenuhi kebutuhan mayoritas produk.
- Tiap komponen punya peran; jangan menambah komponen tanpa kebutuhan nyata.
- Cache mempercepat baca sering; queue menangani kerja lambat.
- Reverse proxy = pintu percaya diri (TLS, routing, static) di depan app.
- Ukuran desain ditentukan kebutuhan/product, bukan tren.

---

## Common Mistakes

1. Langsung microservice untuk aplikasi kecil.
2. Menambah komponen tanpa alur request yang jelas.
3. Cache tanpa TTL/identifikasi → stale.
4. Tidak ada reverse proxy di depan app (TLS/routing berantakan).
5. Desain tanpa diagram alur (sulit dijelaskan & di-review).

---

## Manual Exercises

### Exercise 1
Gambar arsitektur 3-tier untuk "Employee Management".

### Exercise 2
Jelaskan peran tiap komponen dalam arsitektur proyekmu.

### Exercise 3
Tambahkan cache ke desain; jelaskan apa & kapan yang di-cache.

### Exercise 4
Tambahkan queue; jelaskan kerja apa yang bisa asinkron.

### Exercise 5
Identifikasi alur request utuh saat user membuka halaman profil.

---

## Challenge — Minimal Exercise

Tulis deskripsi arsitektur 3-tier (web → app → db) untuk API employee, lengkap dengan reverse proxy, cache, dan queue. Gambarkan diagram & alur request di Notes.

---

## Reflection

1. Apa peran load balancer / reverse proxy?
2. Apa beda cache dan queue?
3. Mengapa 3-tier jadi fondasi umum?
4. Kapan perlu object storage / CDN?
5. Mengapa mulai dari monolith, bukan microservice?

---

## Checklist

- [ ] Mengenal tiap komponen
- [ ] Paham 3-tier
- [ ] Bisa desain menengah
- [ ] Bisa jelaskan alur request
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3 (cache)

```text
Profil user sering dibaca, jarang berubah → cache Redis TTL 600s.
```

Exercise 4 (queue)

```text
Kirim email notifikasi & generate laporan → pindah ke queue/worker.
```

</details>
