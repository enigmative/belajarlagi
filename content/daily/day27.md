# Day 27 — FastAPI

## Learning Objective

- Memahami konsep API dengan FastAPI
- Membuat endpoint sederhana (rute + handler)
- Menggunakan path & query parameter
- Mengembalikan response JSON
- Memahami dokumentasi otomatis /docs

---

## Theory

### Endpoint dasar

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Halo Dunia"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items")
def create_item(name: str):
    return {"created": name, "status": 201}
```

### Dekorator rute

| Dekorator | Method | Fungsi |
|-----------|--------|--------|
| `@app.get` | GET | baca |
| `@app.post` | POST | buat |
| `@app.put` | PUT | ubah |
| `@app.delete` | DELETE | hapus |

Path parameter ditulis `{name}`; tipe dianotasikan untuk validasi otomatis.

---

## Examples

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Note(BaseModel):
    title: str
    body: str

notes = []

@app.get("/notes")
def list_notes():
    return notes

@app.post("/notes")
def create_note(note: Note):
    notes.append(note)
    return note
```

Pydantic `BaseModel` memvalidasi body JSON otomatis (jika `title` kurang → 422).

Buka `http://127.0.0.1:8000/docs` → dokumentasi interaktif otomatis.

---

## Code

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    done: bool = False

tasks = []

@app.get("/tasks")
def list_tasks():
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    tasks.append(task)
    return task

@app.delete("/tasks/{index}")
def remove_task(index: int):
    if 0 <= index < len(tasks):
        return tasks.pop(index)
    return {"error": "not found"}
```

Jalankan:

```bash
uvicorn main:app --reload
```

---

## Explanation

- FastAPI dari anotasi tipe: validasi otomatis (path, query, body).
- `BaseModel` Pydantic = schema body request yang tervalidasi.
- Return dict → otomatis jadi JSON.
- `/docs` dan `/redoc` = dokumentasi interaktif gratis dari deklarasi tipe.

---

## Common Mistakes

1. Lupa anotasi tipe → kehilangan validasi otomatis.
2. Jalankan file langsung `python main.py` → pakai `uvicorn main:app`.
3. Mengembalikan object non-JSON tanpa serialisasi.
4. Tidak memanfaatkan status code spesifik (harus selalu 200).
5. Menaruh logika berat di route (pisahkan service layer).

---

## Manual Exercises

### Exercise 1
Buat `GET /ping` mengembalikan `{"status": "ok"}`.

### Exercise 2
Buat `GET /user/{name}` dengan query `age`.

### Exercise 3
Buat `POST /todos` dengan Pydantic (title, done).

### Exercise 4
Buat list in-memory + GET/POST.

### Exercise 5
Buka `/docs` dan coba endpoint dari UI.

---

## Challenge — Minimal Exercise

Endpoint `POST /calc/avg` menerima JSON `{"nums": [...]}` dan mengembalikan `{"avg": <hasil>}`; handle list kosong → 400.

---

## Reflection

1. Apa keuntungan anotasi tipe di FastAPI?
2. Apa peran Pydantic BaseModel?
3. Kenapa pakai uvicorn bukan `python main.py`?
4. Apa fungsi /docs?
5. Bagaimana FastAPI memisahkan validasi dari logika?

---

## Checklist

- [ ] Bisa membuat GET/POST endpoint
- [ ] Bisa path & query parameter
- [ ] Bisa Pydantic body
- [ ] Bisa running uvicorn + /docs
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```python
@app.get("/ping")
def ping():
    return {"status": "ok"}
```

Exercise 2

```python
@app.get("/user/{name}")
def user(name: str, age: int = 0):
    return {"name": name, "age": age}
```

</details>