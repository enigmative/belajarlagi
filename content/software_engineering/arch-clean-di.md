# Architecture — Clean Architecture & Dependency Injection

## Learning Objective

- Memahami Clean Architecture: domain → use case → adapter → framework
- Dependency Injection (DI) & manfaatnya
- Repository Pattern & DTO (transfer object)
- Memutus kebocoran entity internal ke API
- Monolith vs Modular Monolith vs Microservices

---

## Theory

### Clean Architecture

Rules berpusat: inti bisnis di tengah, teknologi di tepi.

```text
Entities (bisnis inti)
   ↓
Use Cases (aksi aplikasi)
   ↓
Controllers/Presenters (adapters)
   ↓
Frameworks & Drivers (FastAPI, DB, dll)
```

- Dependensi mengarah **ke dalam** ke inti bisnis.
- Framework (FastAPI, DB) adalah detail yang mudah diganti.
- Business logic tidak bergantung pada framework.

### Dependency Injection (DI)

Consumer **menerima** dependency dari luar, bukan `new` sendiri:

```python
# tanpa DI (kaku, susah ditest)
class EmployeeService:
    def __init__(self):
        self.repo = EmployeeRepository()   # terkunci ke implementasi

# dengan DI (fleksibel, mudah mock)
class EmployeeService:
    def __init__(self, repo):
        self.repo = repo
```

### Repository & DTO

- **Repository** — abstraksi akses data; gampang ganti DB/mock.
- **DTO** — objek transfer antar lapisan tanpa entity internal.

---

## Analogy

Clean Architecture = gedung dengan inti bisnis di ruang aman pusat; teknologi (listrik, air/DB/FastAPI) ada di dinding luar yang mudah diganti tanpa menyentuh pusat. DI = "serah terima bahan" — departemen menerima alat dari luar, bukan membuat sendiri, jadi mudah ditukar. Monolith = satu gedung besar; Microservices = banyak gedung kecil terhubung; Modular Monolith = satu gedung dengan sayap/modul rapi.

---

## Examples — FastAPI modular (repo ini)

```python
# repositories/employee.py
class EmployeeRepository:
    def save(self, dto) -> Employee:
        return db.insert(dto)

# services/employee.py
class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo
    def create(self, dto):
        return self.repo.save(dto)

# routes/employee.py (controller)
@router.post("/employees")
def create(payload: EmployeeDTO, svc: EmployeeService = Depends()):
    return svc.create(payload)
```

---

## Code — wiring DI tanpa framework

```python
def build_employee_service() -> EmployeeService:
    repo = EmployeeRepository(db=connection())   # cabut dependency
    return EmployeeService(repo=repo)

svc = build_employee_service()
```

FastAPI: `Depends()` melakukan wiring otomatis; container DI lain juga bisa.

---

## Explanation

- **Controller tipis** & delegate ke Service/use case — jangan taruh bisnis di route.
- **Repository** membuat muatan teknis (SQL/ORM) terisolasi → testable dengan mock.
- **DTO** memutus kebocoran internal entity ke API (tidak expose kolom rahasia).
- **DI**: consumer menerima dependency, tidak `new` sendiri → mudah diganti & diuji.
- Jangan microservice dulu — **modular monolith** rapi jauh lebih baik untuk sebagian besar apps; microservice menambah kompleksitas (network, deploy, tracing).

---

## Common Mistakes

1. Entity dipakai langsung ke API → bocorkan kolom internal.
2. DI manual di tiap tempat tanpa container yang jelas (wiring tersebar).
3. Business logic bergantung framework (sulit diganti/diuji).
4. Microservice premature untuk proyek kecil.
5. Repository return entity internal tanpa DTO.

---

## Manual Exercises

### Exercise 1
Buat DTO untuk input/output endpoint employee.

### Exercise 2
DI: injeksi repository ke service (constructor), bukan `new` di dalam.

### Exercise 3
Pisahkan domain/use case dari layer framework (FastAPI) di satu fitur.

### Exercise 4
Tinjau repo ini: sebutkan yang sudah Clean/DI dan yang belum.

### Exercise 5
Tentukan monolith modular vs microservice untuk proyekmu, jelaskan alasannya.

---

## Challenge — Minimal Exercise

Refactor endpoint `/employees` → route + service + repository + **DTO**, dengan dependency injection via `Depends()`. Pastikan API memakai DTO (bukan entity internal). Catat diagram dependensinya di Notes.

---

## Reflection

1. Apa inti Clean Architecture?
2. Mengapa DI memudahkan testing?
3. Apa keuntungan Repository Pattern?
4. Mengapa DTO penting untuk keamanan API?
5. Kapan microservice benar-benar layak?

---

## Checklist

- [ ] Paham Clean Architecture
- [ ] Bisa DI
- [ ] Bisa repository + DTO
- [ ] Paham monolith vs microservices
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```python
class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

svc = EmployeeService(repo=EmployeeRepository())
```

Exercise 3

```python
class EmployeeDTO(BaseModel):
    name: str
    email: EmailStr
```

</details>
