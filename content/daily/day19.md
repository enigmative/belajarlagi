# Day 19 — Big-O & Complexity

## Learning Objective

- Memahami konsep Big-O untuk mengukur efisiensi
- Mengenali O(1), O(log n), O(n), O(n log n), O(n²)
- Menganalisis loop sederhana
- Memahami trade-off waktu vs memori
- Memilih algoritma yang tepat berdasarkan skala data

---

## Theory

Big-O menggambarkan laju pertumbuhan waktu relatif terhadap ukuran input `n`, untuk `n` besar.

| Notasi | Nama | Contoh |
|--------|------|--------|
| O(1) | konstan | akses list[i], dict[key] |
| O(log n) | logaritmik | binary search |
| O(n) | linear | loop satu kali |
| O(n log n) | linearithmic | merge/quick sort |
| O(n²) | kuadratik | nested loop |

### Contoh analisis

```python
def linear(nums):        # O(n)
    for n in nums:
        print(n)

def quadratic(nums):     # O(n²)
    for a in nums:
        for b in nums:
            print(a, b)

def constant(d):         # O(1)
    return d.get("x")
```

### Kenapa penting

Untuk n = 100000:
- O(n) → 100k operasi (cepat)
- O(n²) → 10 miliar operasi (lambat)

Pilih struktur/algoritma dengan Big-O paling kecil yang masuk akal untuk datamu.

---

## Analogy

Big-O seperti mengukur jalur terburuk hujan: bukan waktu tepat, tapi "kalau orangnya n kali banyak, waktu membengkak seberapa?" — linear (tiap orang tambah waktu tetap), atau kuadratik (dua kali orang = empat kali waktu).

---

## Examples

```python
def contains(nums, target):     # O(n)
    for n in nums:
        if n == target:
            return True
    return False

def contains_fast(seen, target):  # O(1) via set
    return target in seen

# dict lookup: O(1)
scores = {"Amir": 90}
print(scores["Amir"])            # 90
```

---

## Code

```python
import time

n = 100000
nums = list(range(n))

start = time.time()
total = sum(nums)            # O(n), C-optimized
print("sum:", round(time.time() - start, 4))

start = time.time()
s = 0
for x in nums:               # O(n) loop python
    s += x
print("loop:", round(time.time() - start, 4))
```

---

## Explanation

- Abaikan konstanta: 2n dan 100n sama-sama O(n).
- Loop bersarang biasa = O(n²); dua loop berurutan = O(n).
- log n muncul saat ruang pencarian dibelah dua (binary search).
- Waktu bukan segalanya — kadang O(n) lebih baik karena memori kecil.

---

## Common Mistakes

1. Mengira O(2n) beda dengan O(n) → sama, konstanta diabaikan.
2. Tidak menghitung loop bersarang.
3. Memakai O(n²) padahal bisa satu pass (pakai dict).
4. Lupa: `in` di list = O(n), di set = O(1).
5. Menganalisis Big-O pada input kecil.

---

## Manual Exercises

### Exercise 1
Tentukan Big-O dari `for i in range(n): print(i)`.

### Exercise 2
Tentukan Big-O dari nested loop dua lapis.

### Exercise 3
Tentukan Big-O dari dua loop berurutan masing-masing O(n).

### Exercise 4
compare lookup list vs set untuk data besar.

### Exercise 5
Binary search pada data terurut → Big-O berapa?

---

## Challenge — Minimal Exercise

Tulis dua versi `unique_count(nums)` (pakai list, lalu set), sebutkan Big-O masing-masing.

---

## Reflection

1. Apa yang diukur Big-O?
2. Mengapa konstanta diabaikan?
3. Kapan muncul O(log n)?
4. Apa trade-off waktu vs memori?
5. Bagaimana memilih struktur data berdasarkan Big-O?

---

## Checklist

- [ ] Bisa menentukan Big-O loop sederhana
- [ ] Paham perbedaan O(n) dan O(n²)
- [ ] Paham O(log n) melalui binary search
- [ ] Bisa memilih list vs set/dict untuk lookup
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1 → O(n)

Exercise 2 → O(n²)

Exercise 3 → O(n)

Exercise 5 → O(log n)

</details>
