# SQL — JOIN

## Learning Objective

- Memahami relasi antar tabel (1:1, 1:N, N:N)
- Menggunakan INNER JOIN, LEFT JOIN, RIGHT JOIN
- Menulis query multi-tabel yang benar
- Menghindari kesalahan umum JOIN (duplikat, N+1)

---

## Theory

### Mengapa JOIN?

Data relasional disimpan dalam banyak tabel agar tidak duplikasi. JOIN menggabungkan tabel berdasarkan kolom relasi (biasanya foreign key).

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    total REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### INNER JOIN — hanya yang cocok

```sql
SELECT users.name, orders.total
FROM users
JOIN orders ON orders.user_id = users.id;
```

### LEFT JOIN — semua kiri + kanan yang cocok

```sql
SELECT users.name, orders.total
FROM users
LEFT JOIN orders ON orders.user_id = users.id;
-- user tanpa order tetap muncul (total = NULL)
```

### RIGHT JOIN

Kebalikan LEFT. (SQLite ver 3.39+ mendukung; MySQL memang punya.)

```sql
SELECT users.name, orders.total
FROM users
RIGHT JOIN orders ON orders.user_id = users.id;
```

---

## N:N — tabel pivot

```sql
CREATE TABLE course_student (
    course_id INTEGER,
    student_id INTEGER,
    PRIMARY KEY (course_id, student_id)
);

SELECT s.name
FROM course_student cs
JOIN students s ON s.id = cs.student_id
WHERE cs.course_id = 1;
```

---

## Analogy

JOIN = menyatukan dua katalog via nomor yang sama. INNER = buku yang ada di kedua katalog. LEFT = semua buku katalog kiri, catat kalau ada di kanan, isi "—" kalau tidak.

---

## Examples

```sql
-- daftar kursus + jumlah pendaftar
SELECT c.title, COUNT(cs.student_id) AS total
FROM courses c
LEFT JOIN course_student cs ON cs.course_id = c.id
GROUP BY c.id;

-- semua order milik John dengan produknya
SELECT u.name, o.id, p.title
FROM users u
JOIN orders o ON o.user_id = u.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE u.name = 'John';
```

---

## Code — sqlite3

```python
import sqlite3
conn = sqlite3.connect("learning.db")
cur = conn.cursor()
cur.execute("""
    SELECT lessons.title, phases.title
    FROM lessons
    JOIN phases ON phases.slug = lessons.phase_slug
    ORDER BY lessons.order_index
""")
for row in cur.fetchall():
    print(row)
conn.close()
```

---

## Explanation

- Selalu tulis `ON` yang jelas; jangan pakai `WHERE` untuk join (bisa jadi cross join tak sengaja).
- `LEFT JOIN` adalah default "semua dari kiri" yang sering kamu butuhkan.
- Ambigu nama kolom → prefix tabel (`users.id`, `orders.id`).
- Dedupe hasil: `DISTINCT` jika susunan join menggandakan baris.

---

## Common Mistakes

1. Query tanpa kondisi join → cartesian product (baris meledak).
2. Lupa di mana kolom asing menunjuk (foreign key salah arah).
3. LEFT JOIN tapi menganggap kolom kanan pasti ada.
4. N+1: melakukan query per baris di kode alih-alih satu JOIN.
5. `GROUP BY` di JOIN tanpa tahu kolom agregat.

---

## Manual Exercises

### Exercise 1
Buat tabel `departments` dan `employees` (FK department_id), insert data.

### Exercise 2
INNER JOIN: semua employee + nama department.

### Exercise 3
LEFT JOIN: semua department, employee yang kosong tetap muncul.

### Exercise 4
Hitung jumlah employee per department dengan GROUP BY + JOIN.

### Exercise 5
Buat tabel pivot `project_employee` (N:N) dan JOIN-nya.

---

## Challenge — Minimal Exercise

Tulis query di `learning.db`: JOIN `lessons` dengan `phases`, tampilkan `phase` dan jumlah lesson per phase (GROUP BY).

---

## Reflection

1. Apa beda INNER vs LEFT JOIN?
2. Kapan tabel pivot dipakai?
3. Apa risiko cross join tak sengaja?
4. Apa itu masalah N+1 dan bagaimana JOIN menyelesaikannya?
5. Kapan JOIN lebih baik daripada query terpisah?

---

## Checklist

- [ ] Bisa INNER JOIN
- [ ] Bisa LEFT JOIN (dan paham RIGHT)
- [ ] Bisa join N:N via pivot
- [ ] Paham masalah N+1
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id)
);
```

Exercise 4

```sql
SELECT d.name, COUNT(e.id) AS jumlah
FROM departments d
LEFT JOIN employees e ON e.department_id = d.id
GROUP BY d.id;
```

</details>