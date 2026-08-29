# Web Security — API Hardening (CORS, Rate Limiting, Validasi, Upload, Secrets)

## Learning Objective

- CORS
- Rate Limiting
- Input Validation
- File Upload Security
- Secrets Management & praktik produksi

---

## Theory

### CORS

Browser membatasi request lintas-origin. Server bilang "boleh dari mana saja" via header:

```text
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
```

Jangan `*` untuk API dengan kredensial.

### Rate Limiting

Batas request per user/IP:

```text
10 request/detik per IP (Login)
100 request/menit global per user
```

FastAPI: slowapi; Laravel: `throttle:10,1`.

### Input Validation

- Format/prototype: pydantic/validation rule (email, int, range).
- Reject alias empty/oversize.
- Jangan percaya klien: validasi tetap server-side.

### File Upload

- Batasi ukuran (`MAX_UPLOAD_SIZE`).
- Batasi tipe via MIME + ekstensi + magic bytes (bukan sekadar ekstensi).
- Simpan di luar public dir / randomize filename.
- Arahkan navigasi antivirus/scan bila perlu.

### Secrets Management

- `.env`, environment variable, secret manager (AWS SSM, Vault).
- JANGAN commit `.env`.
- Rotasi & jangan hardcode API key.

---

## Analogy

CORS = daftar tamu yang boleh masuk. Rate limit = pintu dengan kuota per orang. Validasi = stempel "data ini sudah dicek". Upload = penjaga paket: cek ukuran, isi, nama sebelum masuk gedung. Secrets = kunci yang disimpan di brankas, bukan ditempel di dinding.

---

## Examples

```python
# FastAPI + slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("10/minute")
def login(request: Request, data: Login):
    ...
```

```php
// Laravel throttle di route
Route::post('/login')->middleware('throttle:10,1');
```

```python
from fastapi import UploadFile

MAX = 5 * 1024 * 1024  # 5 MB
content = await file.read(MAX + 1)
if len(content) > MAX:
    raise HTTPException(413, "file terlalu besar")
```

---

## Code — file upload aman (FastAPI)

```python
import os, uuid

ALLOWED = {"image/png", "image/jpeg"}

async def save_upload(file: UploadFile):
    if file.content_type not in ALLOWED:
        raise HTTPException(400, "tipe tidak diizinkan")
    data = await file.read()
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(413, "terlalu besar")
    fname = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
    with open(os.path.join("uploads", fname), "wb") as f:
        f.write(data)
    return fname
```

---

## Explanation

- CORS bukan enkripsi — hanya pembatasan browser (memitigasi abuse cross-origin, bukan blocking server-to-server).
- Rate limit vital untuk login (brute force) & endpoint mahal.
- Validasi: format + range + ukuran — selalu server-side.
- Upload: tipe asli (magic bytes) bukan extension, ukuran dibatasi, nama acak, di luar web root.
- Secrets: env + gitignore; kalau bocor → rotasi segera.

---

## Common Mistakes

1. CORS `*` dengan credential.
2. Rate limit hanya di middleware, lupa endpoint login.
3. Percaya ekstensi file tanpa cek magic bytes/MIME.
4. Simpan upload di web root dengan nama asli user.
5. `.env` ikut ter-commit.

---

## Manual Exercises

### Exercise 1
Tambahkan rate limit di endpoint login FastAPI/PHP.

### Exercise 2
Atur CORS header untuk satu origin saja.

### Exercise 3
Validation: email + umur di FastAPI (pydantic).

### Exercise 4
Upload gambar dengan cek MIME + ukuran + nama acak.

### Exercise 5
Buat `.env` gitignored berisi DB password.

---

## Challenge — Minimal Exercise

Fungsi `safe_upload(file_bytes, content_type)` memvalidasi PNG/JPEG ≤ 5MB dan mengembalikan nama file acak, atau raise.

---

## Reflection

1. Apa masa iya CORS dan mengapa bukan protection penuh?
2. Kapan rate limiting kritikal?
3. Mengapa cek magic bytes lebih baik dari ekstensi?
4. Apa risiko menyimpan upload di public dir?
5. Bagaimana mengamankan secrets?

---

## Checklist

- [ ] Bisa set CORS dengan benar
- [ ] Bisa rate limiting
- [ ] Bisa validasi input server-side
- [ ] Bisa upload aman
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1 (FastAPI)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("10/minute")
def login(request: Request, creds: Login):
    ...
```

Exercise 5

```text
# .env
DATABASE_URL=postgres://user:pass@localhost/db
# pastikan .env di .gitignore
```

</details>