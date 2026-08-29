# Day 05 — Function

## Learning Objective

- Mendefinisikan function dengan `def`
- Menggunakan parameter, argument, `return`
- Memahami default parameter & keyword argument
- Memahami scope (local vs global)
- Mengetahui kapan kode sebaiknya dijadikan function

---

## Theory

### Function dasar

```python
def calculate_total(price, quantity):
    return price * quantity

total = calculate_total(15000, 3)
print(total)   # 45000
```

- `def` membuat function.
- `price, quantity` adalah **parameter** (nama di definisi).
- `15000, 3` adalah **argument** (nilai yang dimasukkan saat dipanggil).
- `return` mengirim hasil balik ke pemanggil. Tanpa `return`, function mengembalikan `None`.

### Default parameter

```python
def greet(name, greeting="Halo"):
    return f"{greeting}, {name}"

print(greet("Amir"))              # Halo, Amir
print(greet("Amir", "Selamat pagi"))  # Selamat pagi, Amir
```

### Keyword argument

```python
def describe(name, age, job):
    print(name, age, job)

describe(age=23, job="Dev", name="Amir")
```

Urutan tidak penting jika memakai nama parameter.

### Scope

```python
x = 10          # global

def f():
    y = 5       # local, hanya ada di dalam f
    return x + y

print(f())      # 15
# print(y)      # NameError: y tidak ada di luar
```

---

## Analogy

Function seperti **resep atau mesin**: beri bahan (argument), mesin memproses, dan mengeluarkan hasil (return). Kamu tidak perlu tahu isi mesin tiap kali — cukup tahu input & output.

**Kapan dijadikan function?** Saat kamu:
1. mengulang kode yang sama lebih dari sekali,
2. ingin memberi nama pada satu unit logika,
3. ingin menguji satu bagian terpisah.

---

## Examples

### Example 1 — Validasi

```python
def is_adult(age):
    return age >= 18

print(is_adult(20))  # True
print(is_adult(15))  # False
```

### Example 2 — Menghitung banyak hal

```python
def stats(numbers):
    total = sum(numbers)
    n = len(numbers)
    avg = total / n if n else 0
    return total, avg, n

total, avg, n = stats([10, 20, 30])
print(total, avg, n)   # 60 20.0 3
```

---

## Code

```python
def maksimum(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    return c

print(maksimum(3, 9, 5))   # 9
```

---

## Explanation

- `return` menghentikan function; kode sesudahnya tidak dijalankan.
- Parameter dengan default harus **setelah** parameter tanpa default.
- Function memisahkan tanggung jawab → lebih mudah dibaca, diuji, dipakai ulang. (Ini inti dari DRY.)
- Jika function lebih dari ~15 baris, pertimbangkan pecah.

---

## Common Mistakes

1. Lupa `return` → function mengembalikan `None`.
2. Default parameter yang memakai object mutable (`def f(x=[])`) → dipakai ulang antar panggilan (trap klasik!). Gunakan `None` lalu inisialisasi di dalam.
3. Mengubah global dari dalam function tanpa `global` → membuat local baru.
4. Parameter wajib tidak diisi → `TypeError`.
5. Menaruh default parameter sebelum parameter non-default → `SyntaxError`.

---

## Manual Exercises

### Exercise 1

Buat `add(a, b)` dan `multiply(a, b)`. Test dengan beberapa nilai.

### Exercise 2

Buat `is_even(n)` mengembalikan `True/False`.

### Exercise 3

Buat `factorial(n)` memakai loop, `return` nilainya.

### Exercise 4

Buat `price_after_discount(price, discount_percent=10)`.

### Exercise 5

Buat `describe_number(n)` mengembalikan string seperti `"5 adalah ganjil"`.

---

## Challenge — Minimal Exercise

Buat function `reverse(text)` yang mengembalikan string terbalik.

---

## Reflection

1. Apa beda parameter dan argument?
2. Kenapa `return` penting?
3. Apa itu scope, dan kenapa kita butuh itu?
4. Kapan kamu memutuskan sebuah kode sebaiknya jadi function?
5. Apa masalah default parameter `[]`?

---

## Checklist

- [ ] Bisa membuat function + `return`
- [ ] Bisa memakai default & keyword argument
- [ ] Memahami scope local/global
- [ ] Bisa membuat `factorial` sebagai function
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 2**

```python
def is_even(n):
    return n % 2 == 0
```

**Exercise 3**

```python
def factorial(n):
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f
```

**Exercise 4**

```python
def price_after_discount(price, discount_percent=10):
    return price * (1 - discount_percent / 100)
```

**Exercise 5**

```python
def describe_number(n):
    kind = "genap" if n % 2 == 0 else "ganjil"
    return f"{n} adalah {kind}"
```

</details>
