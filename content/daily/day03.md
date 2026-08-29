# Day 03 — Conditional

## Learning Objective

- Menggunakan `if`, `elif`, `else`
- Menyusun kondisi bertingkat dengan logika yang benar
- Menggunakan `nested if` dan kombinasi `and` / `or`
- Menulis validasi sederhana
- Memahami alur eksekusi: hanya satu cabang yang dijalankan

---

## Theory

### Sintaks dasar

```python
age = 20

if age >= 18:
    print("adult")
elif age >= 13:
    print("teenager")
else:
    print("child")
```

Aturan penting:
- Blok ditentukan oleh **indentasi** (biasanya 4 spasi).
- Python mengecek `if` dulu; jika salah, cek `elif`; jika semua salah, jalankan `else`.
- Hanya **satu** cabang yang dijalankan — begitu sebuah kondisi benar, sisanya dilewati.

### Nested if

```python
age = 25
has_card = True

if age >= 18:
    if has_card:
        print("boleh masuk")
    else:
        print("tidak punya kartu")
else:
    print("di bawah umur")
```

Bisa juga ditulis dengan `and` agar lebih datar:

```python
if age >= 18 and has_card:
    print("boleh masuk")
```

---

## Analogy

Kondisional seperti **penjaga pintu dengan daftar pertanyaan berurutan**.

Pertanyaan pertama ("umur >= 18?") dicek dulu. Jika ya, langsung masuk — pertanyaan berikutnya tidak ditanya. Hanya satu jawaban yang menentukan.

Urutan penting: kondisi yang **paling spesifik** harus diletakkan paling atas.

---

## Examples

### Example 1 — Grade

```python
nilai = 85

if nilai >= 90:
    grade = "A"
elif nilai >= 80:
    grade = "B"
elif nilai >= 70:
    grade = "C"
elif nilai >= 60:
    grade = "D"
else:
    grade = "E"

print(grade)
```

### Example 2 — Validasi umur + status

```python
age = 17

if age >= 18:
    print("dewasa")
else:
    print("belum dewasa")
```

---

## Code

```python
nilai = int(input("Masukkan nilai (0-100): "))

if nilai >= 90:
    grade = "A"
elif nilai >= 80:
    grade = "B"
elif nilai >= 70:
    grade = "C"
elif nilai >= 60:
    grade = "D"
else:
    grade = "E"

if nilai >= 0 and nilai <= 100:
    print("Grade:", grade)
else:
    print("Nilai tidak valid")
```

---

## Explanation

- `if` mengevaluasi ekspresi bool. `if 0:` dianggap `False` (nilai falsy: `0`, `""`, `[]`, `None`).
- `elif` = "else if" — memungkinkan banyak kemungkinan.
- Kunci kebenaran: karena hanya satu cabang berjalan, **urutan `elif` menentukan hasil**. Taruh kondisi khusus lebih dulu.
- Bisa memakai `and`/`or`/`not` untuk menggabungkan syarat.

---

## Common Mistakes

1. Melupakan titik dua `:` di akhir `if`/`elif`/`else`.
2. Indentasi tidak konsisten → `IndentationError`.
3. Urutan `elif` salah: mengecek `nilai >= 60` sebelum `nilai >= 90` membuat grading rusak.
4. Menggunakan `=` bukan `==`.
5. Mengira semua cabang dieksekusi — hanya satu yang jalan.

---

## Manual Exercises

### Exercise 1

Tahun kabisat: habis dibagi 4, tapi tidak habis dibagi 100, kecuali habis dibagi 400. Buat programnya.

```text
2000 -> kabisat
1900 -> bukan
2024 -> kabisat
```

### Exercise 2

Input 3 angka, tampilkan angka terbesar.

### Exercise 3

Input sebuah karakter, tentukan vokal / konsonan / bukan huruf.

### Exercise 4

Input saldo & harga. Print "cukup", "kurang", atau "sama persis".

### Exercise 5

Grade value (A/B/C/D/E) → angka rentang. Contoh input `"A"` → `"90-100"`.

---

## Challenge — Minimal Exercise

Input umur. Print `"child"` (< 13), `"teen"` (13–19), `"adult"` (>= 20).

---

## Reflection

1. Kenapa urutan `elif` penting? Beri contoh yang salah.
2. Apa bedanya `if ... if` dan `if ... elif`?
3. Apa itu nilai *falsy*? Sebutkan 3 contoh.
4. Kapan memakai nested `if` vs gabungan `and`?
5. Jelaskan logika tahun kabisat kepada orang lain.

---

## Checklist

- [ ] Bisa memakai `if/elif/else` dengan benar
- [ ] Bisa menentukan tahun kabisat
- [ ] Bisa mencari angka terbesar dari 3 input
- [ ] Memahami konsep falsy
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1 — Kabisat**

```python
t = int(input("tahun: "))
if (t % 4 == 0 and t % 100 != 0) or t % 400 == 0:
    print("kabisat")
else:
    print("bukan")
```

**Exercise 2 — Terbesar**

```python
a = int(input())
b = int(input())
c = int(input())
if a >= b and a >= c:
    print(a)
elif b >= a and b >= c:
    print(b)
else:
    print(c)
```

**Exercise 5 — Grade → rentang**

```python
grade = input().upper()
if grade == "A":
    print("90-100")
elif grade == "B":
    print("80-89")
elif grade == "C":
    print("70-79")
elif grade == "D":
    print("60-69")
elif grade == "E":
    print("0-59")
else:
    print("invalid")
```

</details>
