# Web Security — Otentikasi, Authorization, Session, Cookie, Password

## Learning Objective

- Memahami Authentication vs Authorization
- Session & Cookie
- JWT
- Password Hashing yang benar
- Secrets Management

---

## Theory

### Authentication vs Authorization

- **Authentication** = "siapa kamu?" (login).
- **Authorization** = "kamu boleh apa?" (role/permission).

### Session & Cookie

- Cookie: data kecil di browser, dikirim tiap request.
- Session: data di server, direferensikan via session id (biasanya di cookie).
- Jangan simpan data rahasia di cookie terlihat/plain tanpa mekanisme aman.

### JWT

```text
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.secret-signature
```

Tiga bagian: header.payload.signature. Token stateless berisi klaim (mis. `user_id`), ditandatangani server. Client bawa token (Authorization header); server verifikasi signature tanpa menyimpan sesi.

### Password Hashing

```php
// BENAR: one-way hash + garam
$hash = password_hash($password, PASSWORD_DEFAULT);
password_verify($password, $hash);   // true/false
```

```python
# BENAR: bcrypt/argon2
from hashlib import pbkdf2_hmac  # atau pakai bcrypt/argon2 lib
```

JANGAN: MD5/SHA1 tanpa garam, karena bisa dipecah brute/rainbow table.

---

## Analogy

Authentication = "perlihatkan KTP di pintu". Authorization = "kartu akses Lantai 3". Session = "stempel masuk di tangan" selama kamu di dalam gedung. JWT = "tiket tanda tangan yang bisa dibawa ke mana-mana". Hashing = "penggiling daging": hamburger tidak bisa kembali jadi daging utuh.

---

## Examples

```python
# FastAPI + password
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"])
hash_ = pwd.hash("rahasia123")
pwd.verify("rahasia123", hash_)   # True
```

```php
// CI/Laravel
$hash = bcrypt('rahasia123');        // Laravel
Auth::attempt(['email' => $e, 'password' => $p]);
```

---

## Code — JWT flow (konsep)

```text
POST /login  {email, password}
  → verifikasi password
  → buat JWT {user_id, exp}
  → kirim ke client

GET /profile  Authorization: Bearer <jwt>
  → verifikasi signature + exp
  → baca user_id
  → kembalikan data
```

---

## Explanation

- Jangan pernah menyimpan password plaintext atau hash tanpa garam.
- Gunakan lib standar: `password_verify`/bcrypt/argon2 — bukan MD5/SHA sendiri.
- Session: server-side, mudah di-revoke; JWT: stateless, perlu exp & revoke strategy.
- Secrets (API key, DB password): simpan di env/`.env`, JANGAN di git.
- Selalu HTTPS di produksi (terutama cookie auth/JWT over HTTP).

---

## Common Mistakes

1. Password MD5/SHA1 (cepat dipecah).
2. Meletakkan secret di source code / commit ke git.
3. Autentikasi tanpa menangani brute force (rate limit/lockout).
4. JWT tanpa `exp` → token valid selamanya.
5. Authorization gap: perubahan via API tidak dicek role (IDOR).

---

## Manual Exercises

### Exercise 1
Buat `register` + verify password dengan bcrypt di FastAPI/PHP.

### Exercise 2
Jelaskan alur login dan verifikasi JWT.

### Exercise 3
Buat `.env` untuk DB password & pastikan ter-gitignore.

### Exercise 4
Endpoints: `/login` & `/profile` dengan token.

### Exercise 5
Simulasikan brute force: tambahkan rate limit di login.

---

## Challenge — Minimal Exercise

Fungsi `verify_password(plain, hashed)` di Python yang memakai bcrypt dan mengembalikan `True`/`False`.

---

## Reflection

1. Apa beda authentication vs authorization?
2. Mengapa password tidak boleh plaintext?
3. Apa kelebihan/kelemahan JWT vs session?
4. Kenapa secret harus di env?
5. Apa itu brute force dan pencegahannya?

---

## Checklist

- [ ] Bisa `password_hash`/verify
- [ ] Bisa konsep session/cookie/JWT
- - [ ] Bisa bedakan auth vs authorization
- - [ ] Bisa `.env` untuk secrets
- - [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```python
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"])
h = pwd.hash("sangat rahasia")
assert pwd.verify("sangat rahasia", h)
```

Exercise 3

```text
# .env  (jangan di-commit!)
DB_PASSWORD=supersecret
```

</details>