# Day 07 — List

## Learning Objective

- Membuat & mengakses list
- Menggunakan method: `append`, `insert`, `remove`, `pop`, `sort`, `reverse`, `index`, `count`
- Menggunakan slicing pada list
- Memahami list comprehension
- Memahami bahwa list itu **mutable** dan *reference* (bukan copy)

---

## Theory

### Dasar

```python
numbers = [1, 2, 3, 4, 5]
print(numbers[0])    # 1
print(numbers[-1])   # 5
print(numbers[1:3])  # [2, 3]
```

### Method

```python
nums = [1, 2, 3]
nums.append(4)        # [1,2,3,4]   tambah di akhir
nums.insert(0, 0)     # [0,1,2,3,4] tambah di index
nums.remove(2)        # hapus nilai 2 pertama
nums.pop()            # hapus & return elemen terakhir
nums.sort()           # urutkan (mutable)
nums.reverse()        # balik urutan
print(nums.index(3))  # index nilai 3
print(nums.count(1))  # berapa kali 1 muncul
```

### Comprehension

```python
squares = [x * x for x in range(6)]       # [0,1,4,9,16,25]
evens = [x for x in range(10) if x % 2 == 0]  # [0,2,4,6,8]
```

Pelajari comprehension **setelah** yakin paham loop biasa.

### Mutable & reference

```python
a = [1, 2, 3]
b = a            # b menunjuk ke list yang SAMA
b.append(4)
print(a)          # [1,2,3,4]  <- a ikut berubah!

c = a.copy()      # copy baru
c.append(5)
print(a)          # [1,2,3,4]  <- tidak berubah
```

---

## Analogy

List = **rak buku** dengan posisi bernomor (mulai 0). Kamu bisa menambah/mengambil buku di posisi mana pun. `b = a` tidak menyalin rak — hanya menempel label kedua ke rak yang sama; menata rak lewat label `b` juga mengubah yang terlihat lewat `a`.

---

## Examples

### Example 1 — Total & rata-rata

```python
nums = [10, 20, 30, 40]
total = sum(nums)
avg = total / len(nums)
print(total, avg)
```

### Example 2 — Filter genap

```python
nums = [3, 8, 2, 9, 4]
even = [n for n in nums if n % 2 == 0]
print(even)   # [8, 2, 4]
```

---

## Code

```python
nums = []
while True:
    s = input("angka (kosong untuk selesai): ")
    if s == "":
        break
    nums.append(int(s))

print("jumlah:", sum(nums))
print("terbesar:", max(nums) if nums else None)
print("rata-rata:", round(sum(nums) / len(nums), 2) if nums else 0)
```

---

## Explanation

- `len(list)` = panjang.
- `max`/`min`/`sum` bekerja atas list angka.
- Operasi mutate list **di tempat** (tidak mengembalikan list baru) → `nums.sort()` mengembalikan `None`.
- Menghindari modifikasi saat iterasi: ubah salinan dulu.

---

## Common Mistakes

1. `nums.sort()` lalu memakai hasilnya sebagai list → `None`.
2. Salah mengira `b = a` adalah salinan.
3. `IndexError` saat akses index di luar panjang → cek `len` dulu.
4. Comprehension dengan logika terlalu rumit → mulai dari yang sederhana.
5. Menghapus elemen saat iterasi → elemen terlewat.

---

## Manual Exercises

### Exercise 1

Dari `[5, 1, 9, 3, 7]`, print terbesar dan terkecil.

### Exercise 2

Balik list tanpa `.reverse()` (pakai slicing atau loop).

### Exercise 3

Buat list 10 bilangan genap pertama (0,2,4,...).

### Exercise 4

Dari list, buat list baru yang berisi kuadrat tiap elemen.

### Exercise 5

Gabungkan dua list lalu urutkan hasilnya.

---

## Challenge — Minimal Exercise

Buat function `second_largest(nums)` — elemen terbesar kedua.

---

## Reflection

1. Apa itu *mutable*? Kenapa `b = a` tidak menyalin list?
2. Kapan memakai `.remove` vs `.pop`?
3. Apa keuntungan list comprehension?
4. Apa beda `nums.append(x)` dan `nums[len(nums):] = ...`?
5. Bagaimana mencegah `IndexError`?

---

## Checklist

- [ ] Bisa membuat & mengakses list
- [ ] Bisa memakai method umum list
- [ ] Memahami mutable & reference
- [ ] Bisa list comprehension dasar
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 2**

```python
nums = [1, 2, 3, 4]
print(nums[::-1])          # slicing
# atau loop:
rev = []
for n in nums:
    rev.insert(0, n)
```

**Exercise 3**

```python
evens = list(range(0, 20, 2))
```

**Exercise 4**

```python
nums = [1, 2, 3]
print([n * n for n in nums])
```

**Exercise 5**

```python
a = [3, 1]
b = [2, 4]
merged = a + b
merged.sort()
print(merged)
```

</details>
