# SQL — CRUD & Query Dasar

## Learning Objective

- Memahami tabel, kolom, dan baris
- Menguasai SELECT, INSERT, UPDATE, DELETE
- Menggunakan WHERE, ORDER BY, GROUP BY, HAVING, LIMIT, OFFSET
- Menulis query di sqlite3 (Python) maupun phpMyAdmin

---

## Theory

### Struktur tabel

```text
users
┌────┬───────┬─────────┬───────┐
│ id │ name  │ email   │ role  │
├────┼───────┼─────────┼───────┤
│ 1  │ Amir  │ ...     │ admin │
│ 2  │ Budi  │ ...     │ user  │
└────┴───────┴─────────┴───────┘
```

### CREATE TABLE

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    role TEXT DEFAULT 'user'
);
```

### CRUD

```sql
-- CREATE
INSERT INTO users (name, email, role) VALUES ('Amir', 'amir@mail.com', 'admin');

-- READ
SELECT * FROM users;
SELECT name, email FROM users WHERE role = 'admin';

-- UPDATE
UPDATE users SET role = 'user' WHERE id = 1;

-- DELETE
DELETE FROM users WHERE id = 2;
```

---

## Query lanjutan

```sql
SELECT name, role
FROM users
WHERE role = 'admin'
ORDER BY name ASC
LIMIT 10 OFFSET 0;
```

- `ORDER BY` → urutkan (ASC/DESC)
- `LIMIT` dan `OFFSET` → pagination
- `GROUP BY` + `HAVING`:

```sql
SELECT role, COUNT(*) AS total
FROM users
GROUP BY role
HAVING COUNT(*) > 1;
```

---

## Analogy

Tabel = spreadsheet. `SELECT` = melihat kolom tertentu + menyaring baris. `INSERT` = menambah baris. `UPDATE` = mengubah sel. `DELETE` = menghapus baris. WHERE adalah "filter" di spreadsheet.

---

## Examples

```sql
SELECT * FROM products WHERE price > 10000 ORDER BY price DESC;
SELECT COUNT(*) AS total, category FROM products GROUP BY category;
UPDATE products SET stock = stock - 1 WHERE id = 10;
```

---

## Code — sqlite3 di Python

```python
import sqlite3

conn = sqlite3.connect("learning.db")
cur = conn.cursor()
cur.execute("SELECT id, title FROM lessons ORDER BY order_index")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()
```

---

## Explanation

- SQL itu deklaratif: kamu bilang APA yang mau, bukan BAGAIMANA caranya.
- Parameterized query: `cur.execute("... WHERE id = ?", (5,))` mencegah SQL injection.
- Selalu `conn.commit()` setelah INSERT/UPDATE/DELETE di sqlite3.
- `SELECT` tidak merusak data; `DELETE` tanpa `WHERE` menghapus SEMUA baris — hati-hati.

---

## Common Mistakes

1. `DELETE`/`UPDATE` tanpa `WHERE` → seluruh tabel berubah.
2. Lupa `commit()` di sqlite3.
3. Menyisipkan nilai lewat f-string → rawan SQL injection.
4. `GROUP BY` tanpa agregat yang benar.
5. Lupa `OFFSET` saat pagination → halaman duplikat.

---

## Manual Exercises

### Exercise 1
Buat tabel `notes(id, title, body, created_at)`.

### Exercise 2
Insert 3 baris.

### Exercise 3
SELECT yang hanya title dari 2 note terbaru.

### Exercise 4
UPDATE satu note, DELETE satu note.

### Exercise 5
Hitung jumlah note per tanggal dengan GROUP BY.

---

## Challenge — Minimal Exercise

Tulis query untuk daftar `name` user dengan `role='admin'`, urut alfabetis, 5 pertama. (Kerjakan di DB `learning.db` — tabel mana pun yang relevan.)

---

## Reflection

1. Apa beda DELETE vs DROP?
2. Kenapa WHERE penting di UPDATE/DELETE?
3. Apa fungsi ORDER BY, LIMIT, OFFSET?
4. Apa beda WHERE vs HAVING?
5. Kenapa harus pakai parameterized query?

---

## Checklist

- [ ] Bisa CREATE TABLE
- [ ] Bisa CRUD penuh
- [ ] Bisa WHERE/ORDER/LIMIT/OFFSET
- [ ] Bisa GROUP BY + HAVING
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
```

Exercise 3

```sql
SELECT title FROM notes ORDER BY created_at DESC LIMIT 2;
```

Exercise 5

```sql
SELECT created_at, COUNT(*) AS jumlah FROM notes GROUP BY created_at;
```

</details>