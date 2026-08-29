# Day 08 — Dictionary

## Learning Objective

- Membuat & mengakses dictionary
- Menggunakan `keys`, `values`, `items`, `get`, `update`, `pop`
- Menggunakan dictionary untuk lookup & menghitung frekuensi
- Menjelaskan kenapa `dict` lebih baik dari `list` untuk lookup

---

## Theory

### Dasar

```python
user = {
    "id": 1,
    "name": "John",
    "email": "amir@example.com"
}

print(user["name"])           # John
print(user.get("phone"))      # None (tidak error)
print(user.get("phone", "N/A"))  # "N/A" (default)
user["age"] = 23              # tambah / ubah
user.update({"job": "Dev"})   # tambah banyak sekaligus
del user["id"]                # hapus
email = user.pop("email")     # hapus & ambil nilainya
```

### Iterasi

```python
for key in user:              # key saja
    print(key)

for key in user.keys():       # sama
    pass
for value in user.values():   # nilai saja
    pass
for key, value in user.items():  # pasangan
    print(key, "=", value)
```

### Lookup vs list

```python
# LIST: O(n), harus cari satu per satu
names = ["John", "Budi", "Cika"]
# butuh mencari posisi "Budi"

# DICT: O(1) langsung ke key
ages = {"John": 23, "Budi": 24}
print(ages["Budi"])           # 24 langsung
```

---

## Analogy

Dictionary = **kamar loker**. Setiap loker punya nomor (key) dan isi (value). Untuk mengambil isi, kamu langsung ke nomor lokernya — tidak perlu membuka semua loker satu per satu (seperti list). Ini yang membuat lookup `dict` **jauh lebih cepat** untuk data besar.

---

## Examples

### Counting frequency

```python
def count_chars(text):
    counts = {}
    for c in text:
        counts[c] = counts.get(c, 0) + 1
    return counts

print(count_chars("aabbabc"))  # {'a':3,'b':3,'c':1}
```

### Nested dict

```python
users = {
    1: {"name": "John", "skills": ["Python", "PHP"]},
    2: {"name": "Budi", "skills": ["Java"]},
}
print(users[1]["skills"][0])   # Python
```

---

## Code

```python
data = input("teks: ")
freq = {}
for c in data:
    if c.isalpha():
        freq[c] = freq.get(c, 0) + 1

for c, n in sorted(freq.items()):
    print(c, n)
```

---

## Explanation

- Key harus **immutable** (string, int, tuple). List tidak bisa jadi key.
- `dict.get(key, default)` aman — tidak melempar `KeyError`.
- Access `dict[key]` tanpa key → `KeyError`. Selalu pakai `get` jika belum yakin.
- Dictionary adalah tulang punggung data backend: JSON, mapping, cache.

---

## Common Mistakes

1. Mengakses key yang tidak ada dengan `[]` → `KeyError`.
2. Menggunakan list untuk lookup yang seharusnya dictionary.
3. `counts[c] += 1` saat key belum ada → `KeyError` (harus `get` dulu).
4. Mengira urutan dict selalu tetap (mulai Python 3.7 urutan = urutan masukan, tapi jangan bergantung untuk logika).
5. Memakai object mutable sebagai key.

---

## Manual Exercises

### Exercise 1

Hitung frekuensi karakter dalam `"hello world"`.

### Exercise 2

Dari list nama, hitung berapa kali tiap nama muncul.

### Exercise 3

Buat dict `inventory` (produk → stok). Update stok jika ada pembelian.

### Exercise 4

Dari dict nilai siswa, tentukan siapa dengan nilai tertinggi.

### Exercise 5

Gabungkan dua dict (nilai dari dict kedua menimpa yang pertama).

---

## Challenge — Minimal Exercise

Buat function `most_frequent(text)` mengembalikan karakter yang paling sering muncul.

---

## Reflection

1. Kenapa `dict` lebih baik untuk lookup daripada `list`?
2. Bagaimana `get(key, default)` mencegah error?
3. Apa syarat untuk sebuah key?
4. Bagaimana menghitung frekuensi memakai dict?
5. Kapan kamu memakai nested dict?

---

## Checklist

- [ ] Bisa membuat & mengakses dictionary
- [ ] Bisa memakai `get`, `items`, `update`, `pop`
- [ ] Bisa menghitung frekuensi dengan dict
- [ ] Menjelaskan keunggulan dict vs list
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 2**

```python
names = ["John", "Budi", "John", "Cika", "Budi", "Budi"]
freq = {}
for n in names:
    freq[n] = freq.get(n, 0) + 1
print(freq)   # {'John':2,'Budi':3,'Cika':1}
```

**Exercise 4**

```python
grades = {"A": 80, "B": 92, "C": 75}
top = max(grades, key=grades.get)
print(top)   # "B"
```

**Exercise 5**

```python
a = {"x": 1, "y": 2}
b = {"y": 9, "z": 3}
merged = {**a, **b}
print(merged)   # {'x':1,'y':9,'z':3}
```

</details>
