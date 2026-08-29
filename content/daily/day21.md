# Day 21 — Sorting

## Learning Objective

- Menerapkan Bubble Sort, Selection Sort, Insertion Sort
- Memahami Merge Sort dan Quick Sort secara konsep
- Menganalisis kompleksitas masing-masing
- Memakai `sorted()` / `.sort()` yang benar

---

## Theory

### Bubble Sort — O(n²)

```python
def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a
```

Membandingkan berpasangan, "menggelembungkan" nilai terbesar ke akhir.

### Selection Sort — O(n²)

```python
def selection_sort(arr):
    a = arr[:]
    for i in range(len(a)):
        m = i
        for j in range(i + 1, len(a)):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a
```

Memilih elemen terkecil dan menaruh di depan.

### Insertion Sort — O(n²)

```python
def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a
```

Menaruh tiap elemen ke posisi yang tepat pada bagian kiri yang sudah terurut.

### Merge/Quick Sort — O(n log n) konsep

- Merge: bagi dua terus, lalu gabung secara terurut.
- Quick: pilih pivot, pisahkan yang lebih kecil/besar.

---

## Analogy

- Bubble = menyusun kursi: geser kursi bersebelahan sampai urut (lambat, banyak geser).
- Selection = cari kursi terkecil di sisa baris, taruh paling depan, ulangi.
- Insertion = seperti menyusun kartu remi di tangan: taruh tiap kartu baru pada tempatnya.
- Merge/Quick = bagi masalah jadi dua separuh, selesaikan separuhnya, gabung.

---

## Examples

```python
arr = [64, 34, 25, 12, 22, 11, 90]
print(bubble_sort(arr))      # [11, 12, 22, 25, 34, 64, 90]
print(selection_sort(arr))   # sama
print(insertion_sort(arr))   # sama

# bawaan (C-optimized, cepat) — untuk produksi
print(sorted(arr))           # [11, 12, 22, 25, 34, 64, 90]
```

---

## Code

```python
def bubble_sort(arr):
    a = arr[:]
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

nums = [5, 2, 9, 1, 7]
print(bubble_sort(nums))
```

---

## Explanation

- Tiga algoritma di atas O(n²) — dipelajari untuk **memahami cara kerja sorting**, bukan untuk produksi.
- Untuk produksi: pakai `sorted()` (O(n log n), C-optimized).
- Big-O hanya membandingkan laju pertumbuhan; pada data kecil perbedaan tidak terasa.
- Merge/Quick adalah fondasi "divide and conquer" yang penting untuk problem solving.

---

## Common Mistakes

1. Mengubah list asli (bubble_sort memodifikasi) → salin dulu dengan `[:]`.
2. Salah index inner loop → IndexError / terlewat.
3. Mengira O(n²) setara O(n log n) untuk data besar.
4. Memakai bubble sort untuk data raksasa.
5. Tidak menghafal kapan `sorted` vs `.sort()` (sorted → baru, sort → in-place).

---

## Manual Exercises

### Exercise 1
Implement bubble sort dan uji pada `[3,1,4,1,5,9,2]`.

### Exercise 2
Implement selection sort.

### Exercise 3
Implement insertion sort.

### Exercise 4
Urutkan list string secara descending dengan `sorted(x, reverse=True)`.

### Exercise 5
Bandingkan hasil `sorted()` dan `.sort()` (perbedaan return).

---

## Challenge — Minimal Exercise

Fungsi `solve(nums)` yang mengembalikan list terurut pakai **insertion sort** (bukan `sorted`).

---

## Reflection

1. Kenapa mempelajari sorting padahal ada `sorted()`?
2. Apa perbedaan Bubble vs Insertion?
3. Kenapa Merge Sort O(n log n)?
4. Kapan memakai `sorted` vs `.sort`?
5. Jelaskan insertion sort seperti menyusun kartu.

---

## Checklist

- [ ] Bisa implement bubble/selection/insertion sort
- [ ] Paham kompleksitas O(n²) vs O(n log n)
- [ ] Bisa memakai `sorted`/`.sort`
- [ ] Tahu kapan memakai bawaan
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 4

```python
print(sorted(["banana", "apple", "cherry"], reverse=True))
# ['cherry', 'banana', 'apple']
```

Exercise 5

`sorted(x)` mengembalikan list baru; `x.sort()` mengubah x dan mengembalikan None.

</details>
