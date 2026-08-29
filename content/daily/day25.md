# Day 25 — Debugging

## Learning Objective

- Membaca traceback Python dengan benar
- Mengidentifikasi tipe & lokasi error
- Mereproduksi bug dan mengisolasi penyebab
- Menggunakan `print`/logging dan debugger (`pdb`)
- Memperbaiki bug + menulis regression test

---

## Theory

### Membaca traceback

```python
def divide(a, b):
    return a / b

print(divide(10, 0))
```

Output:

```text
Traceback (most recent call last):
  File "<...>", line 3, in <module>
    print(divide(10, 0))
  File "<...>", line 2, in divide
    return a / b
ZeroDivisionError: division by zero
```

Baca dari **bawah ke atas**:
1. Jenis error (`ZeroDivisionError`)
2. Pesan (`division by zero`)
3. Lokasi paling bawah = tempat error terjadi.

### Tips

```python
import pdb
pdb.set_trace()   # debugger interaktif (n=next, p=print, c=continue)
```

Atau gunakan print sementara:

```python
def process(nums):
    print("DEBUG nums:", nums)          # cek input
    total = sum(nums)
    print("DEBUG total:", total)        # cek step
    return total / len(nums)
```

---

## Contoh error umum

| Error | Arti |
|-------|------|
| `NameError` | nama tidak terdefinisi |
| `TypeError` | operasi dengan tipe salah |
| `IndexError` | index melebihi panjang |
| `KeyError` | key tidak ada di dict |
| `ValueError` | nilai tidak sesuai konteks |
| `AttributeError` | object tidak punya attribute/method |

---

## Analogy

Debugging seperti **detektif di TKP**: jangan menebak. Kumpulkan bukti (pesan error), cari petunjuk (baris kode), tanya saksi (print variabel), uji hipotesis (ubah kode), dan pastikan pelakunya tidak muncul lagi (regression test).

---

## Examples

```python
# Bug: IndexError
total = 0
nums = [10, 20]
for i in range(3):      # i=2 melebihi len
    total += nums[i]
```

Perbaikan:

```python
for i in range(len(nums)):
    total += nums[i]
```

---

## Code

```python
def avg_positive(nums):
    filtered = [n for n in nums if n > 0]
    if not filtered:
        return 0
    return sum(filtered) / len(filtered)

# test
print(avg_positive([1, 2, -3]))
print(avg_positive([]))
```

---

## Explanation

Alur debugging yang benar:

```text
read traceback → identify error type → reproduce → isolate → inspect variable → test hypothesis → fix → regression test
```

Jangan langsung menebak solusi. Reproduce dulu, kecilkan ruang masalah, baru perbaiki.

---

## Common Mistakes

1. Langsung mengganti kode tanpa membaca traceback.
2. Membaca traceback dari atas (yang benar: bawah → atas).
3. Mencetak print di banyak tempat tanpa hipotesis jelas.
4. Memperbaiki tanpa regression test → bug balik lagi.
5. Menghafal "error itu biasanya ..." tanpa memahami.

---

## Manual Exercises

### Exercise 1
Buat kode yang sengaja memicu `IndexError`; perbaiki.

### Exercise 2
Buat `KeyError` dari dict; perbaiki dengan `get`.

### Exercise 3
Fungsi dividen-by-zero; handle dengan try/except.

### Exercise 4
Debug: kenapa `sum([10,"a"])` error? Perbaiki agar hanya angka.

### Exercise 5
Tulis regression test untuk bug di Exercise 4.

---

## Challenge — Minimal Exercise

Fungsi `solve(nums, divisor)`: ambil rata-rata, lalu bagi dengan divisor; handle semua error (kosong, bukan angka, divisor=0) dan jangan crash.

---

## Reflection

1. Bagaimana urutan membaca traceback yang benar?
2. Apa beda mengidentifikasi vs memperbaiki bug?
3. Kenapa perlu mereproduksi bug?
4. Apa itu regression test dan kenapa penting?
5. Jelaskan pendekatan debugging-mu kepada orang lain.

---

## Checklist

- [ ] Bisa membaca traceback
- [ ] Bisa mengidentifikasi 6 tipe error umum
- [ ] Bisa debug dengan print/pdb
- [ ] Selalu menulis regression test
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 4

```python
def safe_sum(nums):
    return sum(n for n in nums if isinstance(n, (int, float)))
```

Exercise 5

```python
def test_safe_sum():
    assert safe_sum([10, "a", 5]) == 15
```

</details>