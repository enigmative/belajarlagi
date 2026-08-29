# Day 09 — Set & Tuple

## Learning Objective

- Membuat & memakai `set`
- Operasi set: union, intersection, difference
- Memahami `list` vs `tuple` (mutable vs immutable)
- Memilih tipe yang tepat untuk kasus tertentu

---

## Theory

### Set — kumpulan unik

```python
numbers = [1, 2, 2, 3, 3, 3]
unique = set(numbers)
print(unique)          # {1, 2, 3}

# Keanggotaan sangat cepat (O(1))
print(2 in unique)     # True
unique.add(4)
unique.discard(1)      # hapus tanpa error jika tidak ada
```

Operasi himpunan:

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)   # union      -> {1,2,3,4,5}
print(a & b)   # intersect  -> {3}
print(a - b)   # difference -> {1,2}
print(a ^ b)   # sym diff   -> {1,2,4,5}
```

Catatan: `set` **tidak menjamin urutan** dan hanya berisi elemen unik.

### Tuple — urutan immutable

```python
point = (10, 20)
x, y = point          # unpacking
print(x, y)           # 10 20

coords = (3, 4)
# coords[0] = 99      # TypeError: tuple immutable!
```

`tuple` seperti `list` tapi **tidak bisa diubah** setelah dibuat.

---

## Analogy

- `set` = **stoples unik**: tidak bisa berisi dua benda yang sama; kalau kamu masukkan duplikat, tetap hanya ada satu.
- `tuple` = **kotak tersegel**: isinya sudah tetap sejak awal, cocok untuk data yang "seharusnya tidak berubah" seperti koordinat atau field record.

---

## Examples

### Menghapus duplikat & cek keanggotaan

```python
emails = ["a@x.com", "b@x.com", "a@x.com"]
uniq = set(emails)
print(len(uniq))          # 2
print("a@x.com" in uniq)  # True
```

### return multiple values (umumnya pakai tuple)

```python
def min_max(nums):
    return min(nums), max(nums)   # ini adalah tuple

lo, hi = min_max([5, 1, 9])
print(lo, hi)   # 1 9
```

---

## Code

```python
text = "the quick brown fox the lazy dog"
words = text.split()

unique_words = set(words)
print("total kata:", len(words))
print("kata unik:", len(unique_words))

common = set("aeiou") & set(text)
print("vokal yang muncul:", common)
```

---

## Explanation

- Gunakan `set` untuk: menghapus duplikat & cek keanggotaan cepat.
- Gunakan `tuple` untuk: data tetap & return beberapa nilai.
- `list` untuk koleksi yang berubah-ubah & berurutan.
- `frozenset` adalah versi immutable dari set (jarang dipakai di tahap ini).

---

## Common Mistakes

1. Mengira `set` mempertahankan urutan → tidak.
2. Mencoba mengubah `tuple` → `TypeError`.
3. Memakai `set` untuk data yang butuh urutan & duplikat → gunakan list.
4. Membuat set kosong dengan `{}` → itu dict! Gunakan `set()`.
5. Operasi set salah simbol: union `|`, bukan `+`.

---

## Manual Exercises

### Exercise 1

Dari `[1,2,2,3,3,3,4]`, buat set dan print jumlah elemen unik.

### Exercise 2

Cek apakah `"x"` ada di set tanpa error.

### Exercise 3

Dua group siswa (set A & B). Tampilkan siswa yang ada di keduanya (intersection).

### Exercise 4

Buat fungsi `swap(a, b)` yang `return` (b, a), lalu unpack hasilnya.

### Exercise 5

Hitung berapa banyak karakter berbeda dalam sebuah string (ini fungsi set).

---

## Challenge — Minimal Exercise

Buat function `unique_count(text)` mengembalikan jumlah huruf unik (abaikan spasi & huruf besar/kecil).

---

## Reflection

1. Apa beda `list` dan `tuple`?
2. Kapan memakai `set`?
3. Bagaimana cara membuat set kosong yang benar?
4. Apa output `{1,2,3} & {3,4}`?
5. Kenapa `return a, b` di Python sebenarnya mengembalikan tuple?

---

## Checklist

- [ ] Bisa membuat & memakai set
- [ ] Bisa union/intersection/difference
- [ ] Paham perbedaan list/tuple/set
- [ ] Bisa menghapus duplikat pakai set
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1**

```python
nums = [1, 2, 2, 3, 3, 3, 4]
print(len(set(nums)))   # 4
```

**Exercise 3**

```python
a = {"Amir", "Budi", "Cika"}
b = {"Budi", "Dewi"}
print(a & b)   # {'Budi'}
```

**Exercise 4**

```python
def swap(a, b):
    return b, a

x, y = swap(1, 2)
print(x, y)   # 2 1
```

**Exercise 5**

```python
text = "Hello"
print(len(set(text.lower())))   # 4
```

</details>
