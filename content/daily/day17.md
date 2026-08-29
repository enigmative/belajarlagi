# Day 17 — Generator & Iterator

## Learning Objective

- Membedakan `iterable`, `iterator`, dan `generator`
- Menulis generator dengan `yield`
- Menggunakan generator expression
- Memahami kenapa generator hemat memori (lazy)
- Memakai `next()` dan `iter()`

---

## Theory

### Iterable vs Iterator

- **Iterable**: bisa di-loop (list, str, dict, range).
- **Iterator**: punya `__next__()`; menghasilkan satu nilai per pemanggilan `next()`.
- `iter(obj)` mendapat iterator dari iterable; `next(it)` mengambil nilai berikutnya.

```python
nums = [1, 2, 3]          # iterable
it = iter(nums)           # iterator
print(next(it))           # 1
print(next(it))           # 2
print(next(it))           # 3
# print(next(it))         # StopIteration
```

### Generator dengan yield

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(3):
    print(x)   # 3 2 1
```

`yield` mengembalikan nilai dan **menjeda** fungsi; dilanjutkan saat `next()` berikutnya. Ini lazy — nilai dibuat saat diminta.

### Generator untuk data besar (hemat memori)

```python
# tanpa generator — membangun seluruh list di memori
def squares(n):
    return [i * i for i in range(n)]

# dengan generator — satu per satu
def gen_squares(n):
    for i in range(n):
        yield i * i
```

Untuk `n` sangat besar, versi generator tidak memboroskan memori.

### Generator expression

```python
gen = (x * x for x in range(5))   # generator (pakai (), bukan [])
print(sum(gen))                   # 30
```

---

## Analogy

Generator seperti **roti keluar dari mesin**: satu potong dihasilkan saat diminta, bukan seluruh tumpukan sekaligus. Untuk data raksasa (jutaan baris), kamu tidak perlu menyimpan semuanya di memori — cukup mengalirkan satu per satu.

---

## Examples

### Membaca file baris per baris (hemat memori)

```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()
```

### Generator tak hingga yang berhenti manual

```python
def natural():
    n = 0
    while True:
        yield n
        n += 1

for x in natural():
    if x > 5:
        break
    print(x)   # 0 1 2 3 4 5
```

---

## Code

```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

f = fib()
for _ in range(10):
    print(next(f), end=" ")
# 0 1 1 2 3 5 8 13 21 34
```

---

## Explanation

- `yield` membedakan generator dari function biasa.
- Generator **hanya bisa di-loop sekali** — setelah habis, `StopIteration`.
- `next(gen)` mengambil nilai berikutnya.
- Generator expression `(...)` vs list comprehension `[...]`.
- Lazy = nilai diproduksi saat dibutuhkan → hemat memori untuk data besar.

---

## Common Mistakes

1. Mengira generator bisa dipakai ulang (loop dua kali) → tidak, sekali pakai.
2. `next()` pada generator yang sudah habis → `StopIteration`.
3. Menulis `return` alih-alih `yield` di generator.
4. Memakai list comprehension padahal `n` raksasa.
5. Terjebak infinite generator tanpa `break`.

---

## Manual Exercises

### Exercise 1

Generator `evens(n)` yang `yield` bilangan genap sampai n.

### Exercise 2

Generator `countdown(n)`.

### Exercise 3

Generator expression untuk kuadrat 0..9, cari jumlahnya.

### Exercise 4

Generator `powers(base, n)` yang menghasilkan `base**i` untuk i=0..n.

### Exercise 5

Gunakan `next()` untuk mengambil 3 nilai pertama dari generator `natural()`.

---

## Challenge — Minimal Exercise

Generator `fib(n)` yang menghasilkan n bilangan Fibonacci pertama.

---

## Reflection

1. Apa beda iterable, iterator, dan generator?
2. Apa artinya *lazy evaluation* dan kenapa berguna?
3. Kenapa generator hanya bisa di-loop sekali?
4. Apa beda `(x for x ...)` dan `[x for x ...]`?
5. Kapan kamu memakai generator alih-alih list?

---

## Checklist

- [ ] Bisa menulis generator dengan `yield`
- [ ] Bisa generator expression
- [ ] Bisa memakai `next()`/`iter()`
- [ ] Paham kenapa generator hemat memori
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1**

```python
def evens(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i
```

**Exercise 3**

```python
print(sum(x * x for x in range(10)))   # 285
```

**Exercise 4**

```python
def powers(base, n):
    for i in range(n + 1):
        yield base ** i
```

</details>
