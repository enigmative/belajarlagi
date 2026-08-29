# Day 04 — Loop

## Learning Objective

- Menggunakan `for` dan `while`
- Menggunakan `range()`
- Menggunakan `break` dan `continue`
- Membedakan kapan memakai `for` vs `while`
- Menerapkan loop untuk: jumlah, factorial, Fibonacci, pattern

---

## Theory

### for + range

```python
for number in range(1, 11):
    print(number)
```

`range(start, stop, step)` — `stop` **tidak termasuk**.

```python
range(5)          # 0 1 2 3 4
range(1, 6)       # 1 2 3 4 5
range(0, 10, 2)   # 0 2 4 6 8
range(5, 0, -1)   # 5 4 3 2 1
```

### for atas koleksi

```python
fruits = ["apel", "pisang", "ceri"]
for fruit in fruits:
    print(fruit)
```

### while

```python
n = 1
while n <= 5:
    print(n)
    n += 1
```

`while` berjalan selama kondisi `True`. **Hati-hati infinite loop** — pastikan ada update variabel.

### break / continue

```python
for i in range(10):
    if i == 3:
        continue      # lewati 3, lanjut
    if i == 7:
        break         # berhenti total di 7
    print(i)
```

---

## Analogy

- `for` seperti **pemeriksa daftar** di kasir: "proses setiap item di antrean ini".
- `while` seperti **menunggu lampu biru**: "ulangi selama kondisinya masih benar".
- `break` = keluar dari barisan lebih awal.
- `continue` = skip orang ini, lanjut ke yang berikutnya.

Gunakan `for` kalau kamu tahu berapa kali / tahu koleksinya. Gunakan `while` kalau berhentinya tergantung kondisi.

---

## Examples

### Example 1 — Jumlah 1..100

```python
total = 0
for i in range(1, 101):
    total += i
print(total)   # 5050
```

### Example 2 — Factorial

```python
n = 5
f = 1
for i in range(1, n + 1):
    f *= i
print(f)   # 120
```

### Example 3 — Fibonacci

```python
a, b = 0, 1
for _ in range(10):
    print(a, end=" ")
    a, b = b, a + b
# 0 1 1 2 3 5 8 13 21 34
```

### Example 4 — Pattern

```python
for i in range(1, 6):
    print("*" * i)
```

---

## Code

```python
n = int(input("masukkan angka: "))

total = 0
i = 1
while i <= n:
    total += i
    i += 1
print("jumlah 1..n:", total)

f = 1
for j in range(1, n + 1):
    f *= j
print("factorial:", f)
```

---

## Explanation

- `range` hemat memori; evaluasi perlahan saat iterasi.
- `range(1, 6)` tidak memasukkan 6 — pola umum `range(start, stop)`.
- Variabel loop (`i`, `_`) hanya hidup dalam loop.
- `_` dipakai kalau variabel tidak dipakai.
- Untuk `while`, jangan lupa memperbarui kondisi, atau jadi infinite loop (tenang, playground punya timeout 5 detik).

---

## Common Mistakes

1. `range(1, n)` lupa bahwa `n` tidak termasuk → hasil kurang satu.
2. Infinite loop pada `while` karena lupa `i += 1`.
3. Mengubah list sambil iterasi `for` → skip item. (Pelajari nanti; untuk sekarang salin list dulu.)
4. `break`/`continue` salah tempat.
5. Mengira `for` selalu butuh `range` — bisa langsung atas list/string.

---

## Manual Exercises

### Exercise 1

Print angka 1–100, tapi untuk kelipatan 3 cetak `"Fizz"`, kelipatan 5 `"Buzz"`, kelipatan 15 `"FizzBuzz"`.

### Exercise 2

Jumlahkan angka dari list `[5, 10, 15, 20, 25]` pakai loop (jangan `sum`).

### Exercise 3

Hitung berapa kali huruf `a` muncul dalam string `"banana"`.

### Exercise 4

Print 10 bilangan Fibonacci pertama.

### Exercise 5

Dari list angka, print hanya yang genap.

---

## Challenge — Minimal Exercise

Print faktorial dari `n` (input).

---

## Reflection

1. Kapan pakai `for` dan kapan `while`?
2. Kenapa `range(5)` mulai dari 0?
3. Apa beda `break` dan `continue`?
4. Apa risiko utama `while` dan bagaimana mencegahnya?
5. Jelaskan cara kerja `range(start, stop, step)`.

---

## Checklist

- [ ] Bisa memakai `for` + `range` 
- [ ] Bisa memakai `while`
- [ ] Bisa memakai `break` & `continue`
- [ ] Bisa menghitung faktorial & Fibonacci
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1 — FizzBuzz**

```python
for n in range(1, 101):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
```

**Exercise 2**

```python
nums = [5, 10, 15, 20, 25]
total = 0
for n in nums:
    total += n
print(total)   # 75
```

**Exercise 3**

```python
text = "banana"
count = 0
for c in text:
    if c == "a":
        count += 1
print(count)   # 3
```

**Exercise 5**

```python
nums = [3, 8, 2, 9, 4, 10]
for n in nums:
    if n % 2 == 0:
        print(n)
```

</details>
