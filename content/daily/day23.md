# Day 23 — Testing dengan pytest

## Learning Objective

- Menulis & menjalankan test dengan pytest
- Menulis assertion dan menguasai fungsi test
- Menggunakan fixture untuk setup data
- Memahami mocking konsep dasar
- Membiasakan test sesegera mungkin (TDD sederhana)

---

## Theory

### Test sederhana

Buat file `test_math.py`:

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_string():
    assert add("a", "b") == "ab"
```

Jalankan:

```bash
pytest
```

pytest menemukan file `test_*.py` dan fungsi `test_*`, lalu mengeksekusinya.

### Assertion

```python
def test_example():
    assert 1 == 1
    assert "py" in "python"
    assert [1, 2] == [1, 2]
```

### Fixture

```python
import pytest

@pytest.fixture
def user():
    return {"name": "Amir", "age": 23}

def test_user_age(user):
    assert user["age"] == 23
```

Fixture menyediakan setup yang dipakai ulang.

### Mocking (konsep)

```python
def send_message(msg):
    # bayangkan mengirim ke server
    import requests
    requests.post("https://x.com", data=msg)

def test_send_message(mocker):
    mocker.patch("requests.post")
    send_message("halo")
    # tanpa menyentuh jaringan nyata
```

Mock mengganti dependency eksternal agar test tidak butuh jaringan/DB sungguhan.

---

## Analogy

Test seperti **checklist sebelum menerbangkan pesawat**: memastikan bagian dasar (engine, roda, navigasi) masih bekerja sebelum lepas landas. Semakin penting bagiannya, semakin wajib di-check.

---

## Examples

```python
def factorial(n):
    if n < 0:
        raise ValueError("negatif")
    r = 1
    for i in range(1, n + 1):
        r *= i
    return r

def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1

def test_factorial_negative():
    import pytest
    with pytest.raises(ValueError):
        factorial(-1)
```

---

## Code

```python
# test_shop.py
def price_after(price, discount=0):
    if discount < 0 or discount > 100:
        raise ValueError("invalid discount")
    return price * (1 - discount / 100)

def test_price_normal():
    assert price_after(10000, 10) == 9000.0

def test_price_no_discount():
    assert price_after(5000) == 5000.0

def test_price_invalid():
    import pytest
    with pytest.raises(ValueError):
        price_after(1000, 200)
```

---

## Explanation

- Nama file & fungsi harus diawali `test_`.
- `assert` adalah kunci: salah → test gagal.
- `pytest.raises` menangkap exception yang diharapkan.
- Fixture = setup yang reusable; mock = pengganti dependency.
- Test bukan tambahan — ia **spesifikasi perilaku** yang bisa dijalankan.

---

## Common Mistakes

1. Tidak menamai fungsi `test_*` → tidak dieksekusi.
2. Assertion terlalu lemah (hanya `assert x` tanpa nilai).
3. Test bergantung pada state global / urutan → tidak deterministik.
4. Mock berlebihan sehingga test tidak menguji apa pun nyata.
5. Menulis test setelah bug parah bukan sebelum/perbaikan.

---

## Manual Exercises

### Exercise 1
Tulis `test_add.py` dengan 3 test untuk fungsi jumlah.

### Exercise 2
Tulis test untuk `is_even(n)`.

### Exercise 3
Gunakan fixture untuk menyediakan list data.

### Exercise 4
Tulis test dengan `pytest.raises` untuk fungsi yang melempar error.

### Exercise 5
Jalankan `pytest` dan pastikan semua hijau.

---

## Challenge — Minimal Exercise

Tulis test untuk fungsi `solve(nums)` (rata-rata) — pastikan kasus list kosong tertangani dan diuji.

---

## Reflection

1. Kenapa test penting sebelum fitur dipakai?
2. Apa beda assertion dan print debug?
3. Kapan memakai fixture?
4. Apa risiko mock yang berlebihan?
5. Bagaimana test membantu refactor tanpa takut rusak?

---

## Checklist

- [ ] Bisa menulis & menjalankan pytest
- [ ] Bisa fixture
- [ ] Bisa `pytest.raises`
- [ ] Paham konsep mock
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```python
def is_even(n):
    return n % 2 == 0

def test_even():
    assert is_even(4) is True
    assert is_even(7) is False
```

Exercise 4

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b

def test_divide_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

</details>