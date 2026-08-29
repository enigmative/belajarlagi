# Day 02 — Operators

## Learning Objective

- Menggunakan operator aritmatika: `+ - * / // % **`
- Menggunakan operator perbandingan: `== != > < >= <=`
- Menggunakan operator logika: `and or not`
- Menjelaskan perbedaan `/` dan `//`, dan kegunaan `%`
- Mengevaluasi ekspresi majemuk dengan benar (urutan operasi)

---

## Theory

### Aritmatika

```python
a = 10
b = 3

print(a + b)    # 13
print(a - b)    # 7
print(a * b)    # 30
print(a / b)    # 3.3333... (float selalu)
print(a // b)   # 3  (hasil bagi bulat, pembulatan ke bawah)
print(a % b)    # 1  (sisa bagi)
print(a ** b)   # 1000 (pangkat)
```

Perhatikan:
- `/` selalu menghasilkan `float`.
- `//` menghasilkan integer hasil bagi bulat.
- `%` menghasilkan sisa bagi — sangat berguna untuk menentukan genap/ganjil, atau "kabisat".

### Perbandingan

```python
print(5 == 5)   # True
print(5 != 3)   # True
print(5 > 3)    # True
print(5 < 3)    # False
print(5 >= 5)   # True
print(5 <= 4)   # False
```

Setiap operasi perbandingan selalu mengembalikan `bool`.

### Logika

```python
print(True and True)    # True
print(True and False)   # False
print(True or False)    # True
print(not True)         # False
```

`and` = kedua-duanya benar. `or` = salah satunya benar. `not` = kebalikan.

### Urutan operasi (precedence)

Urutan dari tinggi ke rendah (disarankan pakai tanda kurung agar jelas):

```text
()  **  * / // %  + -  == != < > <= >=  not  and  or
```

---

## Analogy

Anggap operasi sebagai **mesin kecil satu baris**.

- `//` = "berapa kali penuh?" — 10 dibagi 3, satu kotak penuh isi 3, jadi 3 penuh.
- `%` = "sisa yang tidak muat?" — 10 % 3 = 1 (yang tersisa setelah 3 kotak penuh).
- `and` = dua syarat: "buka jika **sudah 18+ AND** sudah bayar".
- `or` = salah satu: "masuk jika **punya KTP OR** ada yang kenal".

---

## Examples

### Example 1 — Genap / Ganjil

```python
n = 10
print(n % 2 == 0)   # True -> genap
```

### Example 2 — Diskusi harga

```python
price = 15000
qty = 4
total = price * qty
print(total)          # 60000
print(total // 10000) # 6  -> berapa puluhan ribu
print(total % 10000)  # 0  -> sisa
```

### Example 3 — Syarat gabungan

```python
age = 20
has_license = True
can_drive = age >= 17 and has_license
print(can_drive)      # True
```

---

## Code

```python
a = int(input("angka pertama: "))
b = int(input("angka kedua: "))

print("jumlah:", a + b)
print("selisih:", a - b)
print("kali:", a * b)
print("bagi:", a / b)
print("bagi bulat:", a // b)
print("sisa:", a % b)
```

---

## Explanation

- `input()` selalu string → wajib `int(...)` sebelum berhitung.
- `==` membandingkan nilai, `=` menugaskan. Jangan tertukar.
- `%` dipakai untuk: genap/ganjil, tahun kabisat, mengambil digit, membagi rata.
- `not` membalik `bool`; pakai kurung untuk ekspresi campuran agar tidak ambigu.

---

## Common Mistakes

1. Menggunakan `=` untuk perbandingan → `SyntaxError` atau bug logika.
2. Lupa bahwa `/` selalu float: `10 / 2` = `5.0`, bukan `5`.
3. `//` dengan bilangan negatif membulat ke bawah: `-10 // 3` = `-4`.
4. Mencampur `and or` tanpa kurung → hasil tak terduga.
5. `3 ** 2 ** 3` dievaluasi kanan-ke-kiri (= `3 ** 8`).

---

## Manual Exercises

### Exercise 1

Input 2 angka, print hasil `+ - * / // %` semuanya.

### Exercise 2

Input detik, konversi menjadi jam, menit, detik. Contoh `3661` → `1 jam 1 menit 1 detik`.

### Exercise 3

Input harga & qty, hitung total, lalu print total keseluruhan jika diskon 10%.

### Exercise 4

Input 3 angka, print apakah ketiganya sama besar (pakai `and`).

### Exercise 5

Tanpa `input()`, print hasil dari `7**2`, `2**10`, `17 % 5`, `-7 // 2`.

---

## Challenge — Minimal Exercise

Input sebuah angka. Print `"even"` jika genap, `"odd"` jika ganjil.

*(Terapkan di Playground. Challenge sebenarnya di `/challenges`.)*

---

## Reflection

1. Apa perbedaan `/` dan `//`?
2. Kenapa `%` berguna pada pemrograman?
3. Apa hasil `not (a > b)` jika `a=5, b=3`? Jelaskan cara berpikirmu.
4. Kapan kita perlu tanda kurung pada ekspresi logika?
5. Jelaskan `and` dan `or` dengan bahasa sehari-hari.

---

## Checklist

- [ ] Bisa memakai 7 operator aritmatika
- [ ] Bisa memakai operator perbandingan & logika
- [ ] Bisa menentukan genap/ganjil dengan `%`
- [ ] Bisa mengonversi detik ke jam-menit-detik
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 2**

```python
total = int(input("detik: "))
jam = total // 3600
sisa = total % 3600
menit = sisa // 60
detik = sisa % 60
print(jam, "jam", menit, "menit", detik, "detik")
```

**Exercise 5**

```python
print(7**2)   # 49
print(2**10)  # 1024
print(17 % 5) # 2
print(-7 // 2)# -4
```

</details>
