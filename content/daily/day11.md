# Day 11 — File Handling

## Learning Objective

- Membaca & menulis file dengan `open` dan `with`
- Mode: `r`, `w`, `a`, `r+`
- Membaca teks, CSV, dan JSON
- Menulis JSON dengan `json.dump` / menulis list of dict ke file
- Menutup file dengan benar (context manager)

---

## Theory

### Buka & baca

```python
# Membuka, membaca, wajib ditutup
file = open("data.txt", "r", encoding="utf-8")
data = file.read()
file.close()
```

Tapi cara yang disarankan (otomatis ditutup):

```python
with open("data.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

### Mode

```python
"r"   # baca (default), error jika file tak ada
"w"   # tulis, MENIMPA isi lama
"a"   # append, tambah di akhir
"r+"  # baca + tulis
"x"   # tulis, error jika file sudah ada
```

### Membaca per baris

```python
with open("data.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

### Menulis

```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("baris 1\n")
    f.write("baris 2\n")
```

### JSON

```python
import json

data = {"name": "Amir", "age": 23}

# tulis
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# baca
with open("user.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["name"])
```

---

## Analogy

File seperti **catatan fisik di laci**.

- `"r"` = membaca catatan (harus sudah ada).
- `"w"` = menulis ulang catatan baru di atas halaman lama (menghapus yang lama).
- `"a"` = menambahkan di lembar paling bawah tanpa menyentuh isi lama.
- `with ... as` = memastikan laci selalu ditutup, walaupun ada hal tak terduga di tengah membaca.

---

## Examples

### Menulis & membaca list of dict

```python
import json

employees = [
    {"name": "Amir", "salary": 8000000},
    {"name": "Budi", "salary": 7000000},
]

with open("employees.json", "w", encoding="utf-8") as f:
    json.dump(employees, f, indent=2)

with open("employees.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data[0]["name"])
```

---

## Code

```python
import json

name = input("nama: ")
salary = int(input("gaji: "))

try:
    with open("data.json", "r", encoding="utf-8") as f:
        rows = json.load(f)
except FileNotFoundError:
    rows = []

rows.append({"name": name, "salary": salary})

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

print("data tersimpan, total:", len(rows))
```

---

## Explanation

- Selalu pakai `with open(...) as f:` agar file pasti ditutup (aman jika ada error).
- Tentukan `encoding="utf-8"` untuk teks ber-aksara (nama Indonesia biasa).
- `json.load`/`json.dump` bekerja pada file; `json.loads`/`json.dumps` pada string.
- Error umum: file tidak ada saat `"r"` → `FileNotFoundError`. Tangani dengan try/except atau cek `os.path.exists`.

---

## Common Mistakes

1. Lupa menutup file (`file.close()`) jika tidak pakai `with`.
2. Mode `"w"` menimpa data tanpa peringatan.
3. Lupa `encoding="utf-8"` → error karakter.
4. `json.load` pada file yang berisi banyak objek bertumpuk (butuh `loads` per baris).
5. Membaca file yang belum ada tanpa menangani error.

---

## Manual Exercises

### Exercise 1

Tulis 3 baris ke `notes.txt` pakai `with`, lalu baca dan print semua.

### Exercise 2

Append satu baris ke file tanpa menghapus isi lama.

### Exercise 3

Buat file JSON berisi list 2 produk (nama + harga), lalu baca kembali.

### Exercise 4

Program yang menambah record ke `data.json` (seperti Contoh Code).

### Exercise 5

Baca file, hitung dan print jumlah barisnya.

---

## Challenge — Minimal Exercise

Program yang menyimpan list kata yang dimasukkan user ke file, lalu print kembali.

---

## Reflection

1. Kenapa `with open(...)` lebih baik daripada `open`+`close` manual?
2. Apa beda mode `"w"` dan `"a"`?
3. Apa itu *serialization* dan kenapa penting untuk JSON?
4. Apa beda `json.dump` dan `json.dumps`?
5. Bagaimana menangani file yang belum ada saat dibaca?

---

## Checklist

- [ ] Bisa membaca & menulis file teks
- [ ] Bisa memakai mode `r/w/a`
- [ ] Bisa read/write JSON
- [ ] Selalu memakai `with` 
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1**

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("baris 1\nbaris 2\nbaris 3\n")

with open("notes.txt", encoding="utf-8") as f:
    print(f.read())
```

**Exercise 2**

```python
with open("notes.txt", "a", encoding="utf-8") as f:
    f.write("baris baru\n")
```

**Exercise 5**

```python
with open("notes.txt", encoding="utf-8") as f:
    lines = f.readlines()
print(len(lines))
```

</details>
