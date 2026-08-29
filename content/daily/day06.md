# Day 06 — String

## Learning Objective

- Menggunakan index & slice string
- Menggunakan method: `split`, `join`, `replace`, `strip`, `lower`, `upper`, `find`, `startswith`, `endswith`
- Menggunakan f-string
- Menerapkan string untuk: palindrome, reverse, count character/word

---

## Theory

### Index & slice

```python
text = "Hello World"
# index:  H=0 e=1 l=2 l=3 o=4 (spasi)=5 W=6...
print(text[0])        # H
print(text[-1])       # d  (index negatif dari belakang)
print(text[0:5])      # Hello
print(text[6:])       # World
print(text[::-1])     # dlroW olleH (balik)
```

`text[start:stop:step]` — mirror dengan `range`.

### Method umum

```python
s = "  Python Belajar  "

print(s.strip())        # "Python Belajar"  (hapus spasi pinggir)
print(s.lower())        # semua huruf kecil
print(s.upper())        # semua huruf besar
print(s.replace("a", "o"))
print(s.startswith("  "))  # True
print(s.find("hon"))    # index kata, atau -1 jika tidak ada
```

### Split & join

```python
words = "satu dua tiga".split()      # ["satu","dua","tiga"]
print(" ".join(words))               # "satu dua tiga"
```

### f-string

```python
name = "John"
age = 23
print(f"Nama: {name}, Umur: {age}")   # Nama: John, Umur: 23
```

---

## Analogy

String = **untaian manik-manik (karakter)**, dan tiap manik punya nomor posisi. Slicing seperti memotong seutas tali pada posisi tertentu. Index negatif = menghitung dari ujung belakang.

---

## Examples

### Palindrome

```python
def is_palindrome(s):
    s = s.replace(" ", "").lower()
    return s == s[::-1]

print(is_palindrome("Kodok"))       # True
print(is_palindrome("Balajar"))     # False
```

### Count word

```python
sentence = "belajar python itu menyenangkan itu benar"
print(sentence.split().count("itu"))   # 2
```

---

## Code

```python
text = input("kata/kalimat: ").strip().lower()
print("terbalik:", text[::-1])
print("jumlah karakter:", len(text))
```

---

## Explanation

- String **immutable** — method seperti `.upper()` mengembalikan string baru, tidak mengubah yang asli.
- `len(text)` = jumlah karakter.
- `find` mengembalikan `-1` jika tidak ditemukan (beda dengan error).
- `split()` tanpa argumen memisah berdasarkan whitespace.

---

## Common Mistakes

1. Mengira `text[0] = "x"` bisa mengubah string → ini error (immutable).
2. Lupa bahwa method string mengembalikan nilai baru (perlu disimpan).
3. Off-by-one saat slice: `s[:5]` tidak termasuk index 5.
4. Mengabaikan huruf besar/kecil saat membandingkan → selalu `.lower()`.
5. `find` mengembalikan `-1`, bukan `None`, jika tidak ada.

---

## Manual Exercises

### Exercise 1

Reverse string `"programming"`.

### Exercise 2

Hitung jumlah kata dalam kalimat.

### Exercise 3

Cek apakah sebuah string palindrome (tanpa peduli spasi & huruf besar).

### Exercise 4

Hapus karakter `"x"` dari `"xboxx"`.

### Exercise 5

Ambil inisial nama: `"John Doe"` → `"JD"`.

---

## Challenge — Minimal Exercise

Buat function `count_vowels(text)` yang menghitung vokal (a,i,u,e,o).

---

## Reflection

1. Apa artinya string *immutable*?
2. Apa beda `s[:5]` dan `s[::2]`?
3. Kapan memakai `split` dan `join`?
4. Apa output `"hello".find("x")`? Kenapa seperti itu?
5. Bagaimana kamu menjelaskan slicing kepada orang lain?

---

## Checklist

- [ ] Bisa memakai index & slice
- [ ] Bisa memakai method umum string
- [ ] Bisa f-string
- [ ] Membuat palindrome checker
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1**

```python
s = "programming"
print(s[::-1])
```

**Exercise 2**

```python
sentence = "satu dua tiga empat"
print(len(sentence.split()))
```

**Exercise 3**

```python
def is_palindrome(s):
    s = s.replace(" ", "").lower()
    return s == s[::-1]
```

**Exercise 4**

```python
print("xboxx".replace("x", ""))   # "bo"
```

**Exercise 5**

```python
name = "John Doe"
parts = name.split()
print(parts[0][0] + parts[1][0])   # "JD"
```

</details>
