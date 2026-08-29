# Web Security — CSRF, XSS, SQL Injection

## Learning Objective

- Memahami 3 serangan paling umum & cara mencegahnya
- CSRF, XSS, SQL Injection
- Menjawab "bagaimana SQLi terjadi?"

---

## Theory

### SQL Injection

User menyuntikkan SQL ke dalam query.

```php
// RENTAN
$sql = "SELECT * FROM users WHERE name = '$name'";
// input: ' OR '1'='1
// → SELECT * FROM users WHERE name = '' OR '1'='1'  → semua user bocor!
```

```php
// AMAN — parameterized query
$stmt = $db->prepare("SELECT * FROM users WHERE name = ?");
$stmt->execute([$name]);
```

### XSS (Cross Site Scripting)

Memasukkan script ke halaman yang dijalankan browser korban.

```html
<!-- RENTAN -->
<input value="<?= $_POST['name'] ?>" />
<!-- input: "><script>alert(1)</script> -->
```

```html
<!-- AMAN: escape output (textContent / {{ }} / esc()) -->
<?= htmlspecialchars($name, ENT_QUOTES) ?>
```

### CSRF (Cross Site Request Forgery)

Korban sudah login; penyerang membuat request yang memanfaatkannya (form/jahat) untuk menjalankan aksi atas nama korban.

```html
<img src="http://bank.com/transfer?to=hacker&amt=1000" />
```

Pencegahan: **CSRF token** — field token unik per session yang diminta form. Framework (Laravel `@csrf`, CI4) menyediakan otomatis; FastAPI: middleware/origin check.

```html
<form method="POST">
    @csrf
    ...
</form>
```

---

## Analogy

- SQLi = menyusup kata sandi ke perintah yang dijalankan database (jangan menulis SQL dengan menggabung string input).
- XSS = menyelipkan script beda agar browser korban menjalaninya (jangan percaya input → selalu escape saat tampil).
- CSRF = memalsukan permintaan atas nama korban (minta bukti token bahwa user memang mau).

---

## Examples

```python
# FastAPI: parameterized (SQLite) — selalu pakai placeholder
cur.execute("SELECT * FROM users WHERE name=?", (name,))
```

```python
# FastAPI: pydantic validation = input validation (bukan replacement XSS/SQLi tapi filter)
class Login(BaseModel):
    email: EmailStr
```

---

## Code — XSS-safe rendering (JS)

```javascript
// AMAN
el.textContent = userInput;
// RENTAN
el.innerHTML = userInput;
```

---

## Explanation

- **Aturan emas input**: jangan pernah string-interpolasi input ke SQL. Pakai placeholder.
- **Aturan emas output**: escape saat tampil (textContent, `{{ }}`, `htmlspecialchars`, `esc()`).
- CSRF token: hanya request yang membawa token yang benar bisa mengubah state.
- Validation (format) & Sanitization berbeda dari escaping — campur tapi tiap satu tujuan.
- Framework: Laravel/CI otomatis CSRF + escaping; FastAPI: pydantic + manual.

---

## Common Mistakes

1. `f"SELECT ... WHERE name='{x}'"`.
2. `innerHTML` dengan input user.
3. Koneksi DB tanpa `prepare`.
4. Lupa CSRF token di form method POST.
5. Satu fix dianggap cukup — selalu kombinasikan: parameterized query + escape output + CSRF.

---

## Manual Exercises

### Exercise 1
Tulis contoh SQLi dan perbaikannya (placeholder).

### Exercise 2
Tulis contoh XSS dan perbaikannya (textContent/escape).

### Exercise 3
Jelaskan alur CSRF dan letak token.

### Exercise 4
Scan proyekmu: cari `SELECT` interpulasi & innerHTML.

### Exercise 5
Tambah express contoh server yang escape semua respons.

---

## Challenge — Minimal Exercise

Fungsi `safe_query(conn, name)` yang eksekusi `SELECT * FROM users WHERE name = ?` dengan placeholder.

---

## Reflection

1. Bagaimana SQL Injection terjadi?
2. Apa beda XSS stored vs reflected?
3. Apa peran CSRF token?
4. Kenapa `textContent` aman dibanding innerHTML?
5. Apa tiga lapisan pertahanan utama?

---

## Checklist

- [ ] Bisa cegah SQLi (parameterized)
- [ ] Bisa cegah XSS (escape output)
- [ ] Bisa cegah CSRF (token)
- [ ] Paham "bagaimana SQLi terjadi?"
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

Alur: 1) server kirim token CSRF saat render form; 2) klien sertakan token di request; 3) server verifikasi. Tanpa token → tolak. Karena penyerang tidak tahu token unik korban, request palsu gagal.

</details>