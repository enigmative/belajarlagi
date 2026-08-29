# Day 12 — Module & Package

## Learning Objective

- Menggunakan `import` untuk memakai kode dari module lain
- Membuat module sendiri dan mengimpornya
- Memahami perbedaan module vs package dan peran `__init__.py`
- Menggunakan `from x import y` dan alias `import x as y`
- Menulis kode yang bisa dijalankan langsung *atau* diimport (`if __name__ == "__main__"`)

---

## Theory

### Module bawaan

```python
import math
print(math.sqrt(16))        # 4.0
print(math.pi)              # 3.14159...

import random
print(random.randint(1, 6))

from datetime import date
print(date.today())
```

### Membuat module sendiri

Buat file `utils.py`:

```python
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

Lalu di file lain:

```python
import utils
print(utils.add(2, 3))        # 5

from utils import multiply
print(multiply(2, 3))         # 6

import utils as u
print(u.add(1, 1))            # 2
```

Module = file `.py`. Package = folder berisi module + `__init__.py`.

### if __name__ == "__main__"

Di `utils.py`:

```python
def add(a, b):
    return a + b

if __name__ == "__main__":
    # kode ini hanya jalan saat file dijalankan langsung,
    # TIDAK jalan saat diimport
    print(add(2, 3))
```

---

## Analogy

Module seperti **kotak alat**. Kamu tidak membawa semua alat sekaligus; kamu membuka kotak `math` saat butuh matematika, `random` saat butuh acak. Membuat module sendiri = merapikan alatmu (kode) ke kotak berlabel agar bisa dipakai di banyak tempat.

---

## Examples

### Program terbagi dua file

`utils.py` (pustaka) dan `main.py` (menjalankan):

```python
# utils.py
def hitung_total(harga, qty, diskon=0):
    total = harga * qty
    return total * (1 - diskon / 100)
```

```python
# main.py
from utils import hitung_total
print(hitung_total(15000, 3, 10))   # 40500.0
```

---

## Code

```python
import random

def tebak():
    target = random.randint(1, 10)
    while True:
        guess = int(input("tebak (1-10): "))
        if guess == target:
            print("benar!")
            break
        print("salah, coba lagi")

if __name__ == "__main__":
    tebak()
```

---

## Explanation

- `import module` → akses via `module.fungsi`.
- `from module import nama` → akses langsung.
- `import module as alias` → nama pendek.
- Package = folder + `__init__.py` (boleh kosong, menandai folder sebagai package).
- `if __name__ == "__main__"` memungkinkan file berperan ganda: pustaka *(saat diimport)* dan program *(saat dijalankan)*.

---

## Common Mistakes

1. Lupa menulis `from` saat `import nama_fungsi` → `NameError`.
2. Nama file sama dengan module bawaan (misal `random.py`) → menimpa.
3. Kode di modul dijalankan saat diimport (tidak dibungkus `__main__`).
4. `ModuleNotFoundError` karena file tidak di folder yang benar / tidak ada `sys.path`.
5. Salah menaruh fungsi di modul yang seharusnya di main.

---

## Manual Exercises

### Exercise 1

Buat module `geometry.py` dengan `luas_persegi` & `keliling_persegi`. Impor di file lain lalu panggil.

### Exercise 2

Gunakan `random` untuk melempar dadu 6 sisi 10 kali.

### Exercise 3

Gunakan `from math import sqrt, pi` dan print hasil.

### Exercise 4

Buat `utils.py` dengan `if __name__ == "__main__"` yang hanya mencetak saat dijalankan langsung.

### Exercise 5

Menggunakan `datetime`, print tanggal hari ini dan tahunnya.

---

## Challenge — Minimal Exercise

Buat module berisi fungsi matematika dasar, lalu tulis `main` yang memakainya dan jalankan-via-import dua arah.

*(Catatan: playground berjalan mode isolasi sehingga import file user tidak berjalan — uji di kode lokalmu sendiri.)*

---

## Reflection

1. Apa beda module dan package?
2. Apa fungsi `__init__.py`?
3. Kapan pakai `import x` vs `from x import y`?
4. Kenapa `if __name__ == "__main__"` penting?
5. Bagaimana kamu memisahkan kode ke module yang rapi?

---

## Checklist

- [ ] Bisa `import` module bawaan
- [ ] Bisa membuat & memakai module sendiri
- [ ] Memahami `__init__.py`
- [ ] Memakai `if __name__ == "__main__"`
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1**

```python
# geometry.py
def luas_persegi(s): return s * s
def keliling_persegi(s): return 4 * s

# main
from geometry import luas_persegi
print(luas_persegi(5))   # 25
```

**Exercise 2**

```python
import random
for _ in range(10):
    print(random.randint(1, 6))
```

**Exercise 3**

```python
from math import sqrt, pi
print(sqrt(81), pi)
```

</details>
