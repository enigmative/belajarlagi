# SQL — Query Optimization

## Learning Objective

- Menggunakan Index dengan benar
- Memahami EXPLAIN / query plan
- Mengenali dan menghindari N+1 query
- Menerapkan pagination yang efisien
- Mengenali tanda-tanda query lambat

---

## Theory

### Index

Index mempercepat pencarian dengan struktur tambahan (seperti indeks buku):

```sql
CREATE INDEX idx_orders_user ON orders (user_id);
CREATE UNIQUE INDEX idx_users_email ON users (email);
```

Query yang sering `WHERE user_id = ?`/`JOIN` → ditambahkan index → jauh lebih cepat saat data besar.

### EXPLAIN

```bash
sqlite> EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 1;
```

Lihat apakah memakai `SEARCH` (pakai index) atau `SCAN` (full table scan).

### N+1 Query

Masalah klasik: loop di aplikasi memicu query per baris.

```python
# N+1: 1 query users + N query orders
for user in users:
    print(user, get_orders_for(user))  # query baru tiap baris
```

### Pagination

```sql
SELECT * FROM orders ORDER BY id LIMIT 10 OFFSET 0;   -- halaman 1
SELECT * FROM orders ORDER BY id LIMIT 10 OFFSET 10;  -- halaman 2
```

---

## Analogy

Index seperti **daftar isi buku** — untuk mencari suatu topik kamu tidak membaca semua halaman. Tanpa index, database meng-scan seluruh tabel. Tapi index memakan ruang & lambat saat INSERT/UPDATE — seperti kalau daftar isi harus di-update tiap kali buku berubah.

---

## Examples

```sql
-- buat index untuk JOIN yang sering
CREATE INDEX idx_lessons_phase ON lessons (phase_slug);

-- cek query plan
EXPLAIN QUERY PLAN
SELECT title FROM lessons WHERE phase_slug = 'python';

-- composite index untuk filter ganda
CREATE INDEX idx_orders_user_status ON orders (user_id, status);
```

---

## Code — pengukuran kasar

```python
import sqlite3, time
conn = sqlite3.connect("learning.db")

start = time.time()
# tanpa index, 100k baris
conn.execute("CREATE TABLE IF NOT EXISTS big (id INTEGER PRIMARY KEY, v INTEGER)")
conn.execute("INSERT OR IGNORE INTO big(v) SELECT abs(random() % 1000) FROM ...")  # harus konkret
conn.commit()
print("query: SELECT * FROM big WHERE v = 5")
conn.execute("EXPLAIN QUERY PLAN SELECT * FROM big WHERE v = 5").fetchall()
print(round(time.time() - start, 3), "s")
conn.close()
```

*(Praktik nyata: buat tabel 100rb baris, jalankan tanpa vs dengan index, bandingkan waktu.)*

---

## Explanation

- Optimasi dimulai dari **tahu query mana yang lambat** — profil dulu, jangan menebak.
- Index untuk kolom di `WHERE`, `JOIN`, `ORDER BY` yang sering.
- `EXPLAIN QUERY PLAN` menampilkan apakah index terpakai.
- N+1: akali dengan satu JOIN + `GROUP BY`-satu query, atau prefetch repository.
- Pagination `LIMIT/OFFSET` memburuk di offset besar → alternatif `WHERE id > ?`.

---

## Common Mistakes

1. Index di semua kolom tanpa alasan → INSERT lambat & boros disk.
2. Menebak query lambat tanpa EXPLAIN/profiling.
3. N+1 di ORM (Eloquent/CI) karena lazy loading default.
4. `OFFSET` raksasa untuk halaman belakang.
5. `SELECT *` mengambil kolom yang tak dipakai + tidak memanfaatkan index covered.

---

## Manual Exercises

### Exercise 1
Buat tabel `payments` 10 ribu baris, ukur SELECT sebelum vs sesudah index.

### Exercise 2
Cek `EXPLAIN QUERY PLAN` untuk `WHERE id = ?` vs `WHERE kolom_tanpa_index = ?`.

### Exercise 3
Tulis versi join untuk menghindari N+1 (users + orders satu query).

### Exercise 4
Bandingkan pagination `LIMIT/OFFSET` vs `WHERE id > ?`.

### Exercise 5
Identifikasi kolom yang butuh unique index pada skema Employee Management.

---

## Challenge — Minimal Exercise

Di `learning.db`, jalankan `EXPLAIN QUERY PLAN` untuk `SELECT * FROM lessons WHERE phase_slug='python'` sebelum dan setelah `CREATE INDEX idx_lessons_phase ON lessons(phase_slug)`. Catat perbedaannya di Notes.

---

## Reflection

1. Apa yang dilakukan index?
2. Kenapa index memperlambat INSERT?
3. Apa masalah N+1 dan cara mengatasinya?
4. Kapan `OFFSET` bermasalah?
5. Kenapa profil dulu sebelum optimasi?

---

## Checklist

- [ ] Bisa membuat index
- [ ] Bisa membaca EXPLAIN QUERY PLAN
- [ ] Bisa menghindari N+1
- [ ] Bisa pagination efisien
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```sql
SELECT u.id, u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id;
```

Exercise 4

`LIMIT/OFFSET` membaca + membuang baris di depan (O(offset)); `WHERE id > last_id ORDER BY id LIMIT n` langsung melompat memakai index.

</details>