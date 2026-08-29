# Day 28 — Backend Project: Employee API

## Learning Objective

- Membangun API mini (CRUD karyawan) dengan FastAPI
- Menyatukan: routing, Pydantic, in-memory atau SQLite
- Menerapkan RESTful design yang benar
- Menguji endpoint dengan httpx/testclient
- Meninjau seluruh kurikulum Python

---

## Theory

Kita membangun **Employee Management API**:

```text
GET    /api/employees          → daftar
POST   /api/employees          → tambah
GET    /api/employees/{id}     → detail
PUT    /api/employees/{id}     → ubah
DELETE /api/employees/{id}     → hapus
```

Field: `id` (auto), `name`, `role`, `salary`.

### Test dengan TestClient (httpx)

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_employee():
    r = client.post("/api/employees", json={
        "name": "Amir", "role": "Backend", "salary": 8000000
    })
    assert r.status_code == 201
    assert r.json()["name"] == "Amir"
```

---

## Code

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class EmployeeIn(BaseModel):
    name: str
    role: str
    salary: float

class Employee(EmployeeIn):
    id: int

employees = []
next_id = 1

@app.get("/api/employees")
def list_employees():
    return employees

@app.post("/api/employees", status_code=201)
def create_employee(data: EmployeeIn):
    global next_id
    emp = Employee(id=next_id, **data.model_dump())
    next_id += 1
    employees.append(emp)
    return emp

@app.get("/api/employees/{emp_id}")
def get_employee(emp_id: int):
    for e in employees:
        if e.id == emp_id:
            return e
    raise HTTPException(404, "employee not found")

@app.put("/api/employees/{emp_id}")
def update_employee(emp_id: int, data: EmployeeIn):
    for i, e in enumerate(employees):
        if e.id == emp_id:
            employees[i] = Employee(id=emp_id, **data.model_dump())
            return employees[i]
    raise HTTPException(404, "employee not found")

@app.delete("/api/employees/{emp_id}")
def delete_employee(emp_id: int):
    for i, e in enumerate(employees):
        if e.id == emp_id:
            return employees.pop(i)
    raise HTTPException(404, "employee not found")
```

---

## Explanation

- CRUD lengkap dengan status yang benar (201 untuk create, 404 jika tak ada).
- `HTTPException` → response error dengan kode yang klien bisa baca.
- Test dengan TestClient memastikan API bekerja tanpa server hidup.
- Ini template dasar menuju proyek sungguhan (lampu lalu: SQLite + auth + frontend).

---

## Common Mistakes

1. Tidak menangani "id tidak ada" → 500 padahal harus 404.
2. Lupa `status_code=201` pada create.
3. Menaruh semua di satu file untuk proyek besar (pisahkan: main, models, services).
4. Tidak menulis test endpoint.
5. Id duplikat karena tidak ada counter/persistence.

---

## Manual Exercises

### Exercise 1
Tambahkan field `department` ke model.

### Exercise 2
Endpoint filter `GET /api/employees?role=Backend`.

### Exercise 3
Hitung rata-rata gaji seluruh karyawan.

### Exercise 4
Tulis test: create → get → update → delete.

### Exercise 5
Refactor: pindahkan data (employees) ke database SQLite.

---

## Challenge — Minimal Exercise

Endpoint `POST /api/employees` akan menolak (400) jika `salary <= 0`.

---

## Reflection

1. Apa saja komponen dasar REST CRUD?
2. Kenapa status code penting di API?
3. Apa peran TestClient?
4. Bagaimana cara menangani "data tidak ada"?
5. Langkah apa berikutnya setelah CRUD sederhana?

---

## Checklist

- [ ] Bisa CRUD penuh dengan REST
- [ ] Bisa HTTPException dengan kode benar
- [ ] Bisa test endpoint dengan TestClient
- [ ] Paham struktur modul yang baik
- [ ] Seluruh kurikulum Python selesai — rayakan & catat di Notes!

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```python
@app.get("/api/employees")
def list_employees(role: str | None = None):
    if role is None:
        return employees
    return [e for e in employees if e.role == role]
```

Exercise 3

```python
def avg_salary():
    if not employees:
        return 0
    return sum(e.salary for e in employees) / len(employees)
```

</details>