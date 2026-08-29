# Day 26 — HTTP & REST

## Learning Objective

- Memahami HTTP: klien, server, request, response
- Menguasai method GET, POST, PUT, DELETE
- Memahami status code umum (200, 201, 400, 404, 500)
- Menguasai RESTful API design
- Memakai `requests`/`httpx` untuk memanggil API

---

## Theory

### HTTP basics

Klien mengirim **request**, server membalas **response**:

```text
GET /api/lessons HTTP/1.1
Host: localhost:8000
```

Response:

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"data": [...]}
```

### Method utama

| Method | Fungsi | Status sukses |
|--------|--------|---------------|
| GET | membaca | 200 |
| POST | membuat | 201 |
| PUT | mengganti/update | 200 |
| DELETE | menghapus | 200/204 |

### Status code umum

| Code | Arti |
|------|------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request (request salah) |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

### RESTful design

- Gunakan **resource** kata benda, jamak: `/api/lessons`, bukan `/getLessons`.
- Bedakan verb dengan method, bukan nama URL.
- Path parameter: `/api/lessons/{slug}`.
- JSON sebagai format data utama.

---

## Examples

```python
# query di URL
GET /api/challenges?limit=5

# POST body (JSON)
POST /api/notes  {"title": "Belajar HTTP", "body": "..."}

# DELETE
DELETE /api/notes/3
```

Dari Python:

```python
import requests

r = requests.get("http://127.0.0.1:8000/api/lessons")
print(r.status_code)      # 200
print(r.json())
```

---

## Code

```python
import requests

BASE = "http://127.0.0.1:8000/api"

# buat note
resp = requests.post(f"{BASE}/notes", json={
    "title": "HTTP note",
    "body": "belajar method & status"
})
print(resp.status_code)      # 201

# baca note
notes = requests.get(f"{BASE}/notes").json()
print(len(notes), "notes")
```

---

## Explanation

- REST = kontrak yang mudah dibaca: URL = resource, method = aksi, status = hasil.
- GET untuk baca (idempotent), POST untuk buat, PUT untuk update penuh, DELETE untuk hapus.
- Selalu gunakan status code dengan benar agar klien bisa logika percabangan.
- Response JSON → Python dict langsung via `.json()`.

---

## Common Mistakes

1. Memakai GET untuk operasi yang mengubah data.
2. Status code menyesatkan (return 200 padahal error).
3. URL mendeskripsikan aksi ("/addLesson") bukan resource.
4. Tidak menangani error status (402, 404, 500).
5. Mengirim body di GET (bukan praktik standar).

---

## Manual Exercises

### Exercise 1
Sebutkan pair method + status untuk CRUD note.

### Exercise 2
Tulis URL REST untuk: daftar challenge, ambil challenge by slug, hapus note.

### Exercise 3
Apa status code untuk: data tidak ketemu, request body invalid?

### Exercise 4
Dari Python, GET `/api/lessons` dan print judul.

### Exercise 5
POST note baru, lalu cek status 201.

---

## Challenge — Minimal Exercise

Panggil `https://jsonplaceholder.typicode.com/users` (pakai requests/httpx di playground), print nama user pertama.

---

## Reflection

1. Apa peran status code?
2. Kenapa REST memakai kata benda sebagai URL?
3. Apa beda GET dan POST?
4. Kapan memakai PUT vs POST?
5. Bagaimana klien tahu request gagal?

---

## Checklist

- [ ] Paham request/response HTTP
- [ ] Bisa 4 method utama + status
- [ ] Bisa desain RESTful API
- [ ] Bisa panggil API dari Python
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

GET /api/notes (200), POST /api/notes (201), PUT /api/notes/{id} (200), DELETE /api/notes/{id} (200/204)

Exercise 2

- Daftar challenge: `GET /api/challenges`
- Ambil by slug: `GET /api/challenges/{slug}`
- Hapus note: `DELETE /api/notes/{id}`

Exercise 3

Data tidak ketemu → 404; body invalid → 400.

</details>