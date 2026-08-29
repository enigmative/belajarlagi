# Day 16 — Decorator

## Learning Objective

- Memahami bagaimana decorator bekerja
- Menulis decorator sederhana dengan `@decorator`
- Membuat decorator dengan argument
- Memakai decorator umum: `@staticmethod`, `@classmethod`, `@property`
- Menambah perilaku (logging, timing, auth) tanpa mengubah fungsi asli

---

## Theory

### Decorator = fungsi yang membungkus fungsi

```python
def shout(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).upper()
    return wrapper

@shout
def greet(name):
    return f"hello {name}"

print(greet("amir"))   # HELLO AMIR
```

`@shout` sama dengan `greet = shout(greet)`. `wrapper` menambah/turunkan perilaku di sekitar fungsi asli.

### Timing decorator

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {(time.time() - start)*1000:.2f}ms")
        return result
    return wrapper

@timer
def compute():
    total = 0
    for i in range(100000):
        total += i
    return total

print(compute())
```

### Decorator dengan argument (parameterized)

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def hi():
    print("hi")

hi()   # hi hi hi
```

---

## Analogy

Decorator seperti **stempel/stiker pada kotak**. Kamu tidak mengubah isi kotak (fungsi asli), tapi menempelkan label yang menambah perilaku — misal "catat waktu", "wajib login". Kotak tetap sama, tingkah lakunya diperkaya dari luar.

---

## Examples

### Logging

```python
def log(func):
    def wrapper(*args, **kwargs):
        print("> memanggil", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@log
def add(a, b):
    return a + b

add(1, 2)   # > memanggil add
```

### Auth stub

```python
def require_login(func):
    def wrapper(*args, **kwargs):
        # contoh: objek pertama punya user
        if not getattr(args[0], "user", None):
            raise PermissionError("login dulu")
        return func(*args, **kwargs)
    return wrapper
```

---

## Code

```python
import functools

def timer(func):
    @functools.wraps(func)          # pertahankan nama & docstring asli
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        r = func(*args, **kwargs)
        print("time:", round(time.time() - start, 4))
        return r
    return wrapper

@timer
def work():
    return sum(range(100000))

print(work())
```

---

## Explanation

- Decoration dihitung **saat definisi**, bukan saat pemanggilan — fungsi dibungkus sekali.
- `functools.wraps` menjaga metadata fungsi asli (`__name__`, docstring).
- `*args, **kwargs` membuat wrapper fleksibel untuk fungsi apa pun.
- Jangan berlebihan — decorator rumit menyulitkan debugging.

---

## Common Mistakes

1. Lupa `return wrapper` → `NoneType` di-assign ke nama fungsi.
2. Tidak memakai `*args, **kwargs` → error untuk fungsi berparameter.
3. Lupa `@functools.wraps` → metadata fungsi hilang.
4. Decorator untuk argument tapi salah lapis closure.
5. Memakai decorator untuk logika yang seharusnya di dalam fungsi.

---

## Manual Exercises

### Exercise 1

Decorator `uppercase` yang membuat hasil fungsi jadi huruf besar.

### Exercise 2

Decorator `timer` yang print waktu eksekusi.

### Exercise 3

Decorator `double` yang menggandakan hasil `int`.

### Exercise 4

Decorator berargumen `repeat(n)` untuk memanggil fungsi n kali.

### Exercise 5

Gunakan `@property` dan `@staticmethod` (sisa dari Day 13).

---

## Challenge — Minimal Exercise

Buat decorator `logged` yang mencetak nama fungsi & hasilnya setiap dipanggil.

---

## Reflection

1. Apa sebenarnya `@decorator` itu (syntax sugar untuk apa)?
2. Kenapa `wrapper` memakai `*args, **kwargs`?
3. Apa fungsi `functools.wraps`?
4. Kapan kamu sebaiknya memakai decorator?
5. Jelaskan decorator berargument bekerja (lapisan closure).

---

## Checklist

- [ ] Bisa menulis decorator sederhana
- [ ] Bisa decorator berargument
- [ ] Bisa memakai `functools.wraps`
- [ ] Paham `@property`/`@staticmethod`
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 3**

```python
def double(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) * 2
    return wrapper

@double
def add(a, b): return a + b
print(add(2, 3))   # 10
```

**Exercise 4**

```python
def repeat(n):
    def deco(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return deco
```

</details>
