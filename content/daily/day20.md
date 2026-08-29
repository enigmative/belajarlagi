# Day 20 — Searching

## Learning Objective

- Menerapkan Linear Search
- Menerapkan Binary Search (data terurut)
- Memahami kompleksitas keduanya
- Menangani kasus "tidak ditemukan"
- Membedakan kapan memakai masing-masing

---

## Theory

### Linear Search — O(n)

```python
def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1

print(linear_search([5, 1, 9, 3], 9))   # 2
print(linear_search([5, 1, 9, 3], 7))   # -1
```

Mengecek satu per satu dari awal. Cocok untuk list kecil / tidak terurut.

### Binary Search — O(log n)

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9, 11], 7))   # 3
print(binary_search([1, 3, 5, 7, 9, 11], 8))   # -1
```

Membutuhkan data **terurut**. Setiap langkah membuang separuh data.

---

## Analogy

Linear = mencari di tumpukan kertas tak berurutan — cek lembar demi lembar dari atas. Binary = mencari di kamus — buka tengah, kalau kata lebih besar buang separuh kiri, terus sampai ketemu.

---

## Examples

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Edge case: list kosong, target terkecil, target terbesar, target di tengah.

---

## Code

```python
arr = [1, 3, 5, 7, 9, 11, 13]
target = int(input("cari: "))
idx = binary_search(arr, target)
print("ditemukan di index", idx if idx != -1 else "- (tidak ada)")
```

---

## Explanation

- Binary search butuh array terurut.
- `mid = (lo + hi) // 2`.
- Kondisi `lo <= hi` penting; `lo < hi` bisa melewatkan elemen.
- Pahami logikanya dulu; nanti boleh pakai `bisect` bawaan.

---

## Common Mistakes

1. Binary search pada data tidak terurut.
2. Lupa `<=` di kondisi loop.
3. Off-by-one saat update `lo`/`hi` (harus `mid+1` / `mid-1`).
4. Infinite loop karena `mid` tidak maju.
5. Mengembalikan nilai alih-alih index.

---

## Manual Exercises

### Exercise 1
Implement linear search, kembalikan index atau -1.

### Exercise 2
Implement binary search untuk array terurut.

### Exercise 3
Fungsi `count_of(arr, target)` untuk array terurut.

### Exercise 4
Search di array tidak terurut: urutkan dulu lalu binary, atau linear? Jelaskan.

### Exercise 5
Cari nilai terbesar/terkecil dengan loop (O(n)).

---

## Challenge — Minimal Exercise

Fungsi `solve(nums, target)` yang mengembalikan index target pada array **terurut** memakai binary search, atau -1.

---

## Reflection

1. Kapan linear search lebih cocok?
2. Kenapa binary search butuh data terurut?
3. Apa kompleksitas masing-masing?
4. Edge case binary search yang paling sering salah?
5. Jelaskan cara kerja binary search.

---

## Checklist

- [ ] Bisa implement linear search
- [ ] Bisa implement binary search
- [ ] Paham kompleksitas keduanya
- [ ] Bisa menangani "tidak ditemukan"
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 4

Linear (O(n)) lebih sederhana untuk sekali query; jika banyak query pada data yang sama, urutkan sekali lalu binary berulang lebih murah.

Exercise 5

```python
def find_min(arr):
    m = arr[0]
    for x in arr:
        if x < m: m = x
    return m
```

</details>
