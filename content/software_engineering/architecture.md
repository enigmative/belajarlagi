# Software Architecture — MVC, Layered, Clean, SOLID, DI

## Learning Objective

- Memahami MVC, Layered, Clean Architecture
- Derependency Injection
- Repository Pattern, Service Layer, DTO
- Monolith vs Microservices vs Modular Monolith
- Kapan memilih tiap pola

---

## Theory

### MVC

Model (data) – View (tampilan) – Controller (logika). Base dari CI/Laravel.

### Layered (layer)

```text
Controller
   ↓
Service (bisnis)
   ↓
Repository (data access)
   ↓
Model/Database
```

### Clean Architecture

Rules berpusat: domain inti → use cases → adapters → frameworks.

```text
Entities (bisnis)
   ↓
Use Cases (aksi)
   ↓
Controllers/Presenters (adapters)
   ↓
Frameworks & Drivers (FastAPI, DB, dll)
```

### SOLID

Satu tanggung jawab, Open/Closed, Liskov, Interface Segregation, Dependency Inversion (bergantung abstraksi).

### PATTERN

- **Repository** — abstraksi akses data, gampang ganti DB/mock.
- **Service Layer** — bisnis logic di luar controller.
- **DTO** — objek transfer data antar lapisan (tanpa entity intern).

---

## Analogy

Architecture = denah gedung. MVC = pembagian lantai sederhana. Layered = corridoor per departemen. Clean = inti bisnis di ruang aman tengah, teknology (listrik, air/DB) di tepi yang mudah diganti. Monolith = satu gedung besar; Microservices = banyak gedung kecil terhubung; Modular Monolith = satu gedung dengan sayap modular.

---

## Examples — FastAPI modular

```python
# routes/employee.py (Controller)
@router.post("/employees")
def create(payload: EmployeeDTO, svc: EmployeeService = Depends()):
    return svc.create(payload)

# services/employee.py (Service/Use case)
class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo
        self.blacklist = {"banned", "sensitive"}
    def create(self, dto: EmployeeDTO):
        return self.repo.save(dto)

# repositories/employee.py
class EmployeeRepository:
    def save(self, dto) -> Employee:
        return Employee.objects.create(**dto.model_dump())
```

---

## Code — dependency injection tanpa framework

```python
def build_employee_service() -> EmployeeService:
    repo = EmployeeRepository(db=connection())
    return EmployeeService(repo=repo)
```

---

## Explanation

- Controller tipis = jangan taruh bisnis di sana; delegate ke Service.
- Repository membuat muatan technical (SQL/Orm) terisolasi → testable dengan mock.
- DTO memutus kebocoran internal entity ke API.
- DI: consumer menerima dependency, tidak `new` sendiri → mudah diganti & diuji.
- Jangan microservice dulu — monolith modular rapi sudah jauh lebih baik untuk sebagian besar apps.

---

## Common Mistakes

1. Segala logika di controller → sulit tes & berubah.
2. Microservice premature (sudah kompleks walaupun proyek kecil).
3. Entity dipakai langsung ke API (bocorkan kolom internal).
4. DI manual di tiap tempat tanpa container yang jelas.
5. Overlayering: 5 lapisan untuk sekadar CRUD.

---

## Manual Exercises

### Exercise 1
Pisahkan CRUD FastAPI menjadi: route, service, repository.

### Exercise 2
Tambahkan DTO untuk input/output.

### Exercise 3
DI: injeksi repository ke service.

### Exercise 4
Tinjau arsitektur "Internal Company Management" CI (belajar.txt L10): Controller → Service → Repository → Model.

### Exercise 5
Tentukan layered vs clean untuk proyekmu, jelaskan.

---

## Challenge — Minimal Exercise

Refactor endpoint `/employees` menjadi route + service + repository + DTO (mengikuti struktur folder yang sudah ada: `app/api/routes`, `app/services`, `app/repositories`, `app/schemas`).

---

## Reflection

1. Apa beda MVC dan Layered?
2. Mengapa service layer penting?
3. Apa untungnya repository pattern?
4. Kapan microservice layak?
5. Mengapa controller harus tipis?

---

## Checklist

- [ ] Paham MVC/layered/clean
- [ ] Bisa service + repository
- [ ] Bisa DTO
- [ ] Bisa DI
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```python
class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

svc = EmployeeService(repo=EmployeeRepository())
```

</details>