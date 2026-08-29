# SQL — Transaction & ACID

## Learning Objective

- Menggunakan BEGIN, COMMIT, ROLLBACK
- Memahami ACID
- Menulis operasi multi-langkah yang aman
- Menggunakan transaksi di sqlite3

---

## Theory

### Apa itu transaction?

Sekelompok operasi yang dijalankan **sebagai satu kesatuan**: semua sukses atau semua dibatalkan.

```sql
BEGIN;
INSERT INTO accounts (id, balance) VALUES (1, 2000000);
INSERT INTO accounts (id, balance) VALUES (2, 5000000);
COMMIT;
```

### ROLLBACK

```sql
BEGIN;
UPDATE accounts SET balance = balance - 1000000 WHERE id = 1;
-- oops! salah hitung
ROLLBACK;  -- perubahan dibatalkan
```

### ACID

| Huruf | Arti |
|-------|------|
| **A**tomicity | semua atau tidak sama sekali |
| **C**onsistency | data tetap valid setelah transaksi |
| **I**solation | transaksi tidak saling mengganggu |
| **D**urability | hasil tersimpan permanen setelah commit |

---

## Utility

Transaksi penting untuk: transfer uang, pesanan (order + order_items + stok), pembayaran, pendaftaran user + profile. Satu gagal → semua harus batal.

---

## Analogy

Transfer uang = dua langkah: kurangi rekening A, tambah ke B. Kalau kita berhenti setelah langkah 1 (crash), uang hilang. Transaksi memastikan kedua langkah dianggap satu — kalau satu gagal, tidak ada yang jadi.

---

## Examples

```sql
-- terjadi error → rollback otomatis/jelas
BEGIN;
INSERT INTO orders (user_id, total) VALUES (1, 250000);
INSERT INTO order_items (order_id, product_id, qty)
    VALUES (last_insert_rowid(), 5, 2);
COMMIT;
```

---

## Code — sqlite3

```python
import sqlite3
conn = sqlite3.connect("learning.db")
try:
    conn.execute("BEGIN")
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (100000, 1))
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (100000, 2))
    conn.commit()
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()
```

---

## Explanation

- sqlite3 mode default mungkin autocommit per statement; eksplisit `BEGIN`/`COMMIT`/`ROLLBACK` memberi kontrol.
- `with conn:` di sqlite3 = commit otomatis saat sukses, rollback saat exception.
- Isolation: default SQLite memakai serializable-ish lock — transaksi menulis mengunci.
- Transaction sebaiknya pendek; jangan loop berjam-jam di dalam transaksi.

---

## Common Mistakes

1. COMMIT di dalam kondisional yang tidak pasti.
2. Menganggap realistis crash; nyatanya crash memang mungkin terjadi → jalankan transaksi.
3. Menulis half-state ke DB tanpa transaksi (order tanpa items).
4. Menahan transaksi terlalu lama → lock blocking.
5. Lupa rollback di handler exception sehingga state rusak.

---

## Manual Exercises

### Exercise 1
Buat 2 akun di tabel `accounts`, transfer 100k dalam transaksi.

### Exercise 2
Coba skenario crash mendadak antar dua UPDATE — apa yang terjadi tanpa transaksi?

### Exercise 3
Tulis INSERT order + items dalam satu transaksi.

### Exercise 4
Uji ROLLBACK: ubah lalu rollback, cek datanya tetap.

### Exercise 5
Baca dokumentasi `with conn:` pattern di sqlite3.

---

## Challenge — Minimal Exercise

Tulis fungsi Python `transfer(conn, from_id, to_id, amount)` yang menjalankan transfer dalam transaksi, dan raise/rollback jika saldo kurang.

---

## Reflection

1. Apa jaminan ACID pada transaksi?
2. Mengapa transfer butuh transaksi?
3. Apa beda commit dan rollback?
4. Kenapa transaction harus pendek?
5. Bagaimana `with conn:` membantu?

---

## Checklist

- [ ] Bisa BEGIN/COMMIT/ROLLBACK
- [ ] Paham ACID
- [ ] Bisa menulis transfer uang aman
- [ ] Paham isu lock/blocking
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```python
conn.execute("BEGIN")
try:
    cur = conn.execute("INSERT INTO orders (user_id, total) VALUES (?, ?)", (1, 75000))
    conn.execute("INSERT INTO order_items (order_id, product_id, qty) VALUES (?, ?, ?)",
                 (cur.lastrowid, 3, 1))
    conn.commit()
except Exception:
    conn.rollback()
    raise
```

</details>