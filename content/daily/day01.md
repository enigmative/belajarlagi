# Day 01 — Variable & Data Types

## Learning Objective

Setelah menyelesaikan Day 01, kamu harus mampu:

- Menyimpan nilai ke dalam variable dengan Python.
- Memahami konsep assignment dan dynamic typing.
- Mengenali semua data type dasar Python: `int`, `float`, `str`, `bool`, `None`, `list`, `tuple`, `set`, `dict`.
- Menggunakan `print()` dan `input()` untuk I/O dasar.
- Menjelaskan perbedaan mutable vs immutable.

---

## Theory

### Apa itu variable?

Variable adalah **nama untuk sebuah nilai** di dalam memori. Kamu memberi label pada sebuah data supaya bisa dipakai ulang.

```python
name = "John"
age = 23
```

Di sini `name` menyimpan string `"John"`, `age` menyimpan integer `23`.

### Dynamic typing

Python tidak memaksa tipe saat deklarasi. Kamu bisa menaruh angka, lalu menggantinya dengan teks:

```python
x = 5
x = "hello"   # dibolehkan, tapi biasanya tidak disarankan
```

Fleksibel, tapi berarti **kamu sendiri yang harus sadar** tipe data apa yang sedang kamu pegang.

### Data types dasar

| Tipe | Contoh | Mutable? | Kapan dipakai |
|------|--------|----------|---------------|
| `int` | `42` | tidak | angka bulat |
| `float` | `3.14` | tidak | angka desimal |
| `str` | `"halo"` | tidak | teks |
| `bool` | `True` | tidak | benar/salah |
| `None` | `None` | tidak | "tidak ada nilai" |
| `list` | `[1,2,3]` | ya | urutan yang bisa diubah |
| `tuple` | `(1,2,3)` | tidak | urutan tetap |
| `set` | `{1,2,3}` | ya | kumpulan unik |
| `dict` | `{"a":1}` | ya | pasangan key-value |

---

## Analogy

Bayangkan **variable seperti kotak berlabel** di atas meja.

`age = 23` artinya menulis label `age` pada sebuah kotak berisi angka `23`.

- `list` seperti **rak** yang bisa ditambah / dikurangi isinya.
- `tuple` seperti **kotak tersegel** — isinya sudah pasti, tidak bisa diubah.
- `dict` seperti **kamus/loker**: kamu membuka kunci (key) untuk mendapatkan isinya (value).
- `set` seperti **stoples unik** — benda yang sama tidak bisa masuk dua kali.

---

## Examples

### Example 1 — Variable dasar

```python
name = "John"
age = 23
height = 170.5
is_developer = True

print(name)
print(age)
print(height)
print(is_developer)
```

### Example 2 — Dictionary

```python
user = {
    "name": "John",
    "age": 23,
    "skills": ["Python", "PHP"]
}
print(user["name"])
print(user["skills"][0])
```

### Example 3 — Set menghapus duplikat

```python
numbers = [1, 2, 2, 3, 3, 3]
unique = set(numbers)
print(unique)
```

---

## Code

Coba jalankan kode berikut di Playground, lalu ubah nilainya:

```python
name = "John"
age = 23

print("Nama:", name)
print("Umur:", age)
print("Tahun lahir:", 2026 - age)
```

---

## Explanation

- **Assignment** (`=`) menaruh nilai kanan ke nama kiri. Jangan dibaca "sama dengan", baca "disimpan ke".
- `print(x)` menampilkan nilai ke layar.
- `input()` berhenti menunggu kamu mengetik, dan **selalu mengembalikan string**.

```python
age = input("Berapa umurmu? ")   # hasilnya string, bukan int
age = int(age)                    # ubah ke int
print(age + 1)
```

- `len()` untuk panjang sebuah koleksi (`list`, `str`, `tuple`, `dict`, `set`).

---

## Common Mistakes

1. **Lupa mengubah hasil `input()`** — `input()` selalu string. `"20" + 1` error.
2. **Menggunakan list untuk lookup** padahal seharusnya dictionary.
3. **Menduga urutan `set`** — `set` tidak menjamin urutan.
4. **Memakai `=` bukan `==`** untuk perbandingan.
5. **Mencoba mengubah `tuple` atau `str`** → `TypeError: 'tuple' object does not support item assignment`.

---

## Manual Exercises

Tulis kode sendiri — jangan lihat solusi dulu. Gunakan Playground.

### Exercise 1

Buat variable `my_name`, `my_age`, `my_city`. Print ketiganya.

### Exercise 2

Tanya umur user via `input()`, ubah ke int, lalu print umur 5 tahun kemudian.

### Exercise 3

Buat list `fruits` berisi 3 buah. Tambahkan satu buah. Print jumlah elemennya.

### Exercise 4

Buat dictionary `person` berisi `name`, `job`, `salary`. Cetak `name` dan `salary`.

### Exercise 5

Dari list `[5, 5, 6, 6, 7]`, buat set, lalu print hasil dan jumlah elemen unik.

*(Jawaban ada di akhir halaman — coba sendiri dulu.)*

---

## Challenge — Minimal Exercise

> Hanya untuk melatih pemahaman dasar. Challenge sebenarnya ada di halaman `/challenges`.

Tulis program yang:

1. Menerima 3 angka dari user.
2. Menyimpannya ke variable.
3. Mencetak jumlah ketiganya.

Wajib mengonversi `input()` ke `int`.

---

## Reflection

Jawab dalam kalimatmu sendiri (simpan di halaman Notes):

1. Apa yang kamu pahami tentang variable?
2. Apa perbedaan `list` dan `tuple`?
3. Kenapa `input()` perlu dikonversi dengan `int()`?
4. Apa edge case-nya jika user memasukkan huruf, bukan angka?
5. Bagaimana cara menjelaskan `dict` kepada orang yang baru belajar coding?

---

## Checklist

- [ ] Bisa membuat variable dengan benar
- [ ] Bisa menyebutkan 5+ data type beserta contohnya
- [ ] Bisa menggunakan `input()` dan `print()`
- [ ] Bisa menjelaskan mutable vs immutable
- [ ] Selesai mengerjakan 5 Manual Exercises
- [ ] Menuliskan Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1**

```python
my_name = "John"
my_age = 23
my_city = "Jakarta"
print(my_name, my_age, my_city)
```

**Exercise 2**

```python
age = int(input("Berapa umurmu? "))
print("5 tahun lagi:", age + 5)
```

**Exercise 3**

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("mango")
print(len(fruits))
```

**Exercise 4**

```python
person = {"name": "John", "job": "Developer", "salary": 8000000}
print(person["name"], person["salary"])
```

**Exercise 5**

```python
nums = [5, 5, 6, 6, 7]
unique = set(nums)
print(unique, len(unique))
```

</details>
