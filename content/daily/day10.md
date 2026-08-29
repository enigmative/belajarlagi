# Day 10 — Exception Handling

## Learning Objective

- Menggunakan `try`, `except`, `else`, `finally`
- Menangkap tipe exception tertentu (`ZeroDivisionError`, `ValueError`, dll.)
- Melempar exception dengan `raise`
- Membuat custom exception
- Menulis kode yang tidak mudah crash di edge case

---

## Theory

### try / except

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Tidak bisa dibagi nol")
```

Kode dalam `try` dicoba; jika muncul error, blok `except` yang cocok dijalankan. Program tidak berhenti.

### Menangkap banyak tipe

```python
try:
    n = int(input("angka: "))
    print(10 / n)
except ValueError:
    print("Itu bukan angka")
except ZeroDivisionError:
    print("Tidak bisa dibagi nol")
```

### else & finally

```python
try:
    n = int("10")
except ValueError:
    print("gagal")
else:
    print("berhasil, n =", n)   # jalan hanya jika tidak ada error
finally:
    print("selalu jalan")       # jalan apa pun yang terjadi
```

- `else`: dijalankan jika `try` sukses.
- `finally`: dijalankan selalu (misal untuk menutup file / cleanup).

### raise

```python
def set_age(age):
    if age < 0:
        raise ValueError("Umur tidak boleh negatif")
    return age
```

`raise` melempar exception secara sengaja.

### Custom exception

```python
class InsufficientBalanceError(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError("Saldo tidak cukup")
    return balance - amount
```

---

## Analogy

`try/except` seperti **helm pengaman**. Kamu tetap jalan (try), tapi kalau jatuh (error), helm menahan dampaknya (except) sehingga tidak patah (program tidak crash). `finally` seperti "membersihkan meja setelah makan" — pasti dilakukan, baik berhasil atau tidak.

---

## Examples

### Example 1 — Input angka yang aman

```python
while True:
    try:
        n = int(input("Masukkan angka: "))
        break
    except ValueError:
        print("Coba lagi, harus angka.")

print("angka:", n)
```

### Example 2 — Division safe

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # None
```

---

## Code

```python
try:
    numerator = int(input("pembilang: "))
    denominator = int(input("penyebut: "))
    print(numerator / denominator)
except ValueError:
    print("Input harus bilangan bulat")
except ZeroDivisionError:
    print("Penyebut tidak boleh nol")
```

---

## Explanation

- Tangkap exception **secara spesifik** dulu, baru yang umum (`Exception`) sebagai cadangan.
- Jangan menangkap dengan `except:` kosong — menyembunyikan error.
- Exception itu class; urutan `except` diuji dari atas.
- `finally` wajib untuk cleanup sumber daya (file, koneksi).

---

## Common Mistakes

1. `except:` terlalu luas → error tersembunyi, susah debug.
2. Menangkap exception tapi tidak melakukan apa-apa (silent swallow).
3. Melempar `Exception` tanpa pesan yang berguna.
4. Lupa bahwa `else` hanya jalan saat sukses.
5. Mengandalkan exception untuk alur normal yang seharusnya dicek `if`.

---

## Manual Exercises

### Exercise 1

Loop input angka sampai user memasukkan angka valid (handle `ValueError`).

### Exercise 2

Fungsi `safe_divide(a, b)` yang mengembalikan `None` jika b=0.

### Exercise 3

Baca `int(input())`; jika user memasukkan `"abc"`, print pesan error.

### Exercise 4

Custom exception `NegativeValueError`, lempar jika nilai negatif.

### Exercise 5

`try/except/else/finally`: bagi 2 angka; `finally` print "selesai".

---

## Challenge — Minimal Exercise

Fungsi `solve(nums)` yang menghitung rata-rata; jika list kosong atau ada non-angka, kembalikan `None` (jangan crash).

---

## Reflection

1. Apa beda `else` dan `finally` di try?
2. Kenapa sebaiknya menangkap tipe exception spesifik?
3. Kapan kamu memakai `raise`?
4. Apa risiko menangkap semua exception diam-diam?
5. Jelaskan kenapa error handling melindungi user experience.

---

## Checklist

- [ ] Bisa memakai `try/except/else/finally`
- [ ] Bisa menangkap tipe exception spesifik
- [ ] Bisa `raise` & custom exception
- [ ] Bisa menulis input loop yang aman
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1**

```python
while True:
    try:
        n = int(input("angka: "))
        break
    except ValueError:
        print("harus angka")
```

**Exercise 4**

```python
class NegativeValueError(Exception):
    pass

def check(x):
    if x < 0:
        raise NegativeValueError("negatif")
    return x
```

**Exercise 5**

```python
try:
    a = int(input())
    b = int(input())
    r = a / b
except ZeroDivisionError:
    print("tidak bisa bagi nol")
else:
    print("hasil:", r)
finally:
    print("selesai")
```

</details>
