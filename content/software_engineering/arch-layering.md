# Architecture — MVC, Layered & SOLID

## Learning Objective

- Memahami MVC (Model-View-Controller)
- Layer/basis: Controller → Service → Repository → Model
- Prinsip SOLID
- Menjaga controller tipis
- Kapan memakai layered vs MVC

---

## Theory

### MVC

Model (data) – View (tampilan) – Controller (logika). Basis dari CI/Laravel.

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

- **Controller** — terima request/HTTP, delegasikan, kembalikan respons.
- **Service** — logika bisnis (validasi, aturan, orkestrasi).
- **Repository** — akses data/DB, isolasi SQL/ORM.
- **Model** — representasi data.

### SOLID

| Huruf | Prinsip | Makna |
|-------|---------|-------|
| S | Single Responsibility | satu kelas satu alasan berubah |
| O | Open/Closed | terbuka ekstensi, tertutup modifikasi |
| L | Liskov | subclass bisa menggantikan parent |
| I | Interface Segregation | jangan paksa implement method tak dipakai |
| D | Dependency Inversion | bergantung abstraksi, bukan konkret |

---

## Analogy

Arsitektur = denah gedung. MVC = pembagian lantai sederhana (data / tampilan / logika). Layered = koridor per departemen: front desk (controller) menerima tamu, departemen bisnis (service) memproses, gudang (repository) mengambil barang. SOLID = aturan ketat supaya tiap departemen punya satu tugas dan mudah diganti tanpa merusak lain.

---

## Examples — layered sederhana

```text
EmployeeController
   ↓ call
EmployeeService  (bisnis: validasi, aturan)
   ↓ call
EmployeeRepository (query SQL/ORM)
   ↓
Employee Model
```

```python
# route (controller tipis)
@router.post("/employees")
def create(payload: EmployeeDTO, svc: EmployeeService = Depends()):
    return svc.create(payload)
```

---

## Code — service pisah dari controller

```python
class EmployeeService:
    def __init__(self, repo):
        self.repo = repo
    def create(self, dto):
        # bisnis logic di sini
        self.repo.save(dto)
        return {"status": "ok"}
```

Controller hanya memanggil service — tidak menulis SQL atau aturan bisnis di dalamnya.

---

## Explanation

- Controller **tipis** = tidak taruh bisnis/SQL; delegate ke Service.
- Service layer memisahkan aturan bisnis dari HTTP → mudah di-uji & digunakan ulang.
- Repository mengisolasi muatan teknis (SQL/ORM) → mudah ganti DB & mock saat test.
- SOLID terutama S & D paling berdampak pada pemeliharaan harian.
- Jangan overlayering: untuk CRUD kecil, 2-3 lapisan cukup; 5 lapisan malah beban.

---

## Common Mistakes

1. Segala logika di controller → sulit tes & berubah.
2. Business logic di dalam query/repository (campur aduk).
3. Overlayering untuk sekadar CRUD.
4. Repository dipakai langsung di controller (lewati service + aturan).
5. Mengabaikan single responsibility → kelas raksasa.

---

## Manual Exercises

### Exercise 1
Pisahkan CRUD FastAPI menjadi: route (controller), service, repository.

### Exercise 2
Pindahkan validasi/aturan bisnis ke service, jangan di route.

### Exercise 3
Identifikasi satu kelas yang melanggar Single Responsibility & pecah.

### Exercise 4
Tinjau arsitektur "Internal Company Management" (CI): Controller → Service → Repository → Model.

### Exercise 5
Jelaskan kapan MVC cukup vs kapan perlu layered penuh.

---

## Challenge — Minimal Exercise

Refactor endpoint `/employees` (atau endpoint lain di repo ini) menjadi route + service + repository, mengikuti struktur folder yang ada (`app/api/routes`, `app/services`, `app/repositories`). Catat lapisan yang kamu buat & alasan S-nya.

---

## Reflection

1. Apa beda MVC dan Layered?
2. Mengapa controller harus tipis?
3. Apa peran service layer?
4. Apa peran repository pattern?
5. Prinsip SOLID mana yang paling sering terabaikan?

---

## Checklist

- [ ] Paham MVC
- [ ] Paham layered (controller→service→repository)
- [ ] Bisa buat service + repository
- [ ] Paham SOLID (terutama S & D)
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```python
# routes/employee.py
@router.post("/employees")
def create(payload: EmployeeDTO, svc: EmployeeService = Depends()):
    return svc.create(payload)

# services/employee.py
class EmployeeService:
    def create(self, dto):
        return self.repo.save(dto)

# repositories/employee.py
class EmployeeRepository:
    def save(self, dto):
        return db.insert(dto)
```

</details>
