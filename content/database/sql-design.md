# SQL — Database Design & Normalization

## Learning Objective

- Memahami Primary Key, Foreign Key, Unique, Index, Constraint
- Merancang relationship 1:1, 1:N, N:N
- Menerapkan normalisasi 1NF, 2NF, 3NF
- Mendesain skema yang bisa dipakai semua stack (Python/PHP/CI/Laravel)

---

## Theory

### Konsep kunci

- **Primary Key** — kolom unik yang mengidentifikasi tiap baris.
- **Foreign Key** — kolom yang menunjuk ke PK tabel lain.
- **Unique** — nilai tidak boleh duplikat.
- **Index** — mempercepat pencarian (menukar ruang dengan waktu).
- **Constraint** — aturan integritas (NOT NULL, CHECK, UNIQUE, FK).

### Relationship

- **1:1** — user ↔ profile (setiap user punya satu profile).
- **1:N** — user ↔ order (satu user banyak order); FK di sisi banyak.
- **N:N** — course ↔ student; butuh tabel pivot.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    bio TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount REAL CHECK (amount >= 0)
);

CREATE TABLE course_student (
    course_id INTEGER REFERENCES courses(id),
    student_id INTEGER REFERENCES users(id),
    PRIMARY KEY (course_id, student_id)
);
```

---

## Normalisasi

| NF | Aturan |
|----|--------|
| 1NF | Setiap kolom satu nilai (jangan array/CSV dalam kolom) |
| 2NF | 1NF + tidak ada dependensi parsial ke sebagian PK |
| 3NF | 2NF + tidak ada dependensi transitif |

### Contoh buruk (belum 1NF)

```sql
-- skills dalam satu kolom
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    skills TEXT  -- "Python,PHP,Laravel" ← jangan
);
```

### Normalized (1NF)

```sql
CREATE TABLE employee_skills (
    employee_id INTEGER REFERENCES employees(id),
    skill TEXT,
    PRIMARY KEY (employee_id, skill)
);
```

---

## Analogy

Data seperti menyimpan alamat orang yang pindah-pindah. Kita catat orangnya sekali (users) dan alamatnya terpisah (addresses 1:N) supaya mengubah alamat tidak mengubah banyak baris sembarangan. Normalisasi = menghilangkan redudansi yang memancing inkonsistensi.

---

## Examples

Rancang skema blog:

```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    author_id INTEGER REFERENCES users(id),
    title TEXT NOT NULL,
    body TEXT,
    published_at TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    author_id INTEGER REFERENCES users(id),
    body TEXT
);
```

Post → comments = 1:N; users → posts = 1:N; N:N tidak ada di sini.

---

## Code — definisikan skema sebelum koding

```python
import sqlite3
conn = sqlite3.connect("learning.db")
conn.executescript(open("database/schema.sql", encoding="utf-8").read())
conn.commit()
conn.close()
```

---

## Explanation

- Susunan pertanyaan "siapa pemilik ini?" menentukan FK.
- Selalu tambahkan `INDEX` pada kolom FK yang sering dipakai di WHERE/JOIN.
- `CHECK` menjaga nilai valid (misal `amount >= 0`).
- Normalisasi: aturan praktis — satu fakta, satu tempat. Duplikasi = sumber bug.

---

## Common Mistakes

1. Tidak ada PK (baris duplikat tak terkendali).
2. FK tanpa index → JOIN lambat.
3. Kolom berisi daftar dipisah koma (belum 1NF).
4. Over-normalize sampai query berantakan (praktik: normalize secukupnya, denormalize untuk data baca berat).
5. Relationship arah salah (FK di tabel "satu" alih-alih "banyak").

---

## Manual Exercises

### Exercise 1
Rancang skema `students`, `courses`, `enrollments` (N:N). Tulis CREATE TABLE-nya.

### Exercise 2
Identifikasi PK/FK/Unique/Index di skema `learning.db` (buka schema.sql).

### Exercise 3
Normalisasi: tabel `orders(id, customer_name, customer_email, items_csv)` → skema 1NF+.

### Exercise 4
Tambah CHECK constraint pada kolom `age` (>= 0).

### Exercise 5
Desain skema untuk "attendance" (employee hadir per tanggal, 1:N).

---

## Challenge — Minimal Exercise

Buat skema relasional untuk **Employee Management**: `employees`, `departments` (1:N), dan `employees_roles`/`roles` (N:N), lengkap dengan PK/FK/UNIQUE. (Bisa ditulis di Notes, atau CREATE TABLE di DB.)

---

## Reflection

1. Apa beda PK dan FK?
2. Kenapa perlu UNIQUE?
3. Kapan tabel pivot dibutuhkan?
4. Apa tujuan 3NF?
5. Kapan kamu boleh denormalize?

---

## Checklist

- [ ] Bisa merancang 1:1, 1:N, N:N
- [ ] Bisa PK/FK/Unique/Index/Constraint
- [ ] Bisa menormalkan sampai 3NF
- [ ] Bisa mendesain skema aplikasi
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);
CREATE TABLE enrollments (
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    PRIMARY KEY (student_id, course_id)
);
```

Exercise 4

```sql
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    age INTEGER CHECK (age >= 0)
);
```

</details>