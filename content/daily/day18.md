# Day 18 — Context Manager

## Learning Objective

- Memahami `with ... as` 
- Menggunakan context manager bawaan (open, lock)
- Menulis context manager dengan `__enter__` / `__exit__`
- Memakai `contextlib.contextmanager` untuk versi ringkas
- Memahami `try/finally` di balik `with`

---

## Theory

### with statement

```python
with open("data.txt", "r", encoding="utf-8") as f:
    data = f.read()
```

`with` mengelola **setup** dan **cleanup** otomatis — file pasti ditutup, walau ada error.

### __enter__ / __exit__

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("time:", round(time.time() - self.start, 3))
        return False   # False = biarkan error lanjut menyebar

with Timer():
    sum(range(1000000))
```

- `__enter__` dijalankan saat masuk blok `with`, mengembalikan nilai `as`.
- `__exit__` dijalankan saat keluar (sukses/error). Jika mengembalikan `True`, error ditelan.

### contextlib.contextmanager (ringkas)

```python
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    try:
        yield            # ini titik masuk blok `with`
    finally:
        print("time:", round(time.time() - start, 3))

with timer():
    sum(range(1000000))
```

---

## Analogy

`with` seperti **mengunci pintu kamar saat masuk (__enter__) dan mengunci kembali saat keluar (__exit__)** — dijamin selalu ditutup, entah ada apa pun di dalam. Kamu tidak perlu mengingat-manual untuk menutup: itulah keunggulan dibanding `try/finally` yang kamu tulis sendiri setiap kali.

---

## Examples

### Mengelola transaksi fiktif

```python
class Transaction:
    def __enter__(self):
        print("mulai transaksi")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print("rollback")
        else:
            print("commit")
        return False

with Transaction():
    print("lakukan sesuatu")
```

---

## Code

```python
from contextlib import contextmanager
import time

@contextmanager
def measure(label):
    start = time.time()
    try:
        yield
    finally:
        print(f"{label}: {round((time.time()-start)*1000,2)}ms")

with measure("loop"):
    sum(range(1000000))
```

---

## Explanation

- `with` = `try/finally` yang rapi: cleanup dijamin.
- `__exit__(exc_type, exc_val, exc_tb)` menerima info error (None jika sukses).
- `contextmanager` + `yield` menyusutkan boilerplate.
- Contoh pakai sehari-hari: buka file, lock threading, koneksi DB, transaksi.

---

## Common Mistakes

1. Tidak memakai `with` untuk file/koneksi → resource bocor.
2. `__exit__` mengembalikan `True` tanpa sengaja → menyembunyikan error.
3. Di `contextmanager`, lupa `try/finally` → cleanup tidak jalan saat error.
4. Mengembalikan `self` tapi tidak memakai `as`.
5. Melakukan banyak logika di `__enter__`.

---

## Manual Exercises

### Exercise 1

Pakai `with open(...)` untuk menulis lalu membaca file (tanpa `close` manual).

### Exercise 2

Buat `Timer` context manager yang print durasi.

### Exercise 3

Buat `Message` dengan `__enter__` print "mulai" dan `__exit__` print "selesai".

### Exercise 4

Pakai `@contextmanager` untuk `suppress_errors` yang menelan exception.

### Exercise 5

Context manager `log_exception` yang mencetak jenis error bila terjadi.

---

## Challenge — Minimal Exercise

Buat context manager `opened(path, mode)` yang membuka file dan menjamin ditutup (pakai `@contextmanager`).

---

## Reflection

1. Apa yang dijamin oleh `with`?
2. Apa parameter `__exit__` dan fungsinya?
3. Kapan `__exit__` mengembalikan `True`?
4. Apa kelebihan `contextmanager` vs menulis class?
5. Kenapa `with` lebih baik daripada `try/finally` manual?

---

## Checklist

- [ ] Bisa memakai `with` untuk file
- [ ] Bisa menulis `__enter__`/`__exit__`
- [ ] Bisa `@contextmanager`
- [ ] Paham setup/cleanup otomatis
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 4**

```python
from contextlib import contextmanager

@contextmanager
def suppress_errors():
    try:
        yield
    except Exception:
        pass

with suppress_errors():
    x = 1 / 0
print("selamat, tidak error")
```

**Exercise 5**

```python
class LogException:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print("error:", exc_type.__name__)
        return False
```

</details>
