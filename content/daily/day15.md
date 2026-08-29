# Day 15 — Typing & Dataclass

## Learning Objective

- Menambahkan type annotations pada fungsi & variabel
- Memakai `Optional`, `Union`, `List`, `Dict`, `Tuple`
- Memahami `TypeAlias` dan `Generic`
- Menggunakan `@dataclass` untuk membuat data class ringkas
- Memahami beda annotation (hint) vs runtime checking (pydantic)

---

## Theory

### Type annotation

```python
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity
```

Annotasi **tidak** memaksa tipe saat runtime — ia hint untuk pembaca & tooling (linter/IDE).

### Tipe dari `typing`

```python
from typing import Optional, Union, List, Dict, Tuple

def find(names: List[str], target: str) -> Optional[int]:
    # mengembalikan index, atau None jika tidak ada
    for i, n in enumerate(names):
        if n == target:
            return i
    return None

def parse(value: Union[int, str]) -> int:
    return int(value)

def stats() -> Tuple[int, float]:
    return 10, 5.5

def config() -> Dict[str, int]:
    return {"max": 10}
```

### Optional = Union[X, None]

```python
from typing import Optional
def greet(name: Optional[str] = None) -> str:
    return f"Hello {name or 'anonymous'}"
```

### TypeAlias

```python
from typing import TypeAlias

UserId: TypeAlias = int
def get_user(uid: UserId):
    ...
```

### Generic (sederhana)

```python
from typing import TypeVar, List

T = TypeVar("T")
def first(items: List[T]) -> T:
    return items[0]
```

---

## Dataclass

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int
    email: str = ""
    skills: List[str] = field(default_factory=list)

u = User("Amir", 23)
print(u.name, u.age)      # Amir 23
print(u)                  # repr otomatis rapi
```

`@dataclass` otomatis membuat `__init__`, `__repr__`, `__eq__` dari annotation — mengurangi boilerplate. `field(default_factory=list)` menghindari shared mutable default.

---

## Analogy

Type annotation seperti **label pada wadah**: "isi ini nama (str)", "ini umur (int)". Python sendiri tidak memeriksa label saat mengisi, tapi label membuat wadah lebih jelas untuk manusia & alat bantu.

Dataclass seperti **mengisi formulir**: kamu cukup daftar field-nya, Python menyiapkan constructor, tampilan rapi, dan perbandingan otomatis.

---

## Examples

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)

products = [Product("Laptop", 12000000, tags=["elektronik"]),
            Product("Meja", 500000)]
def total_price(items: List[Product]) -> float:
    return sum(p.price for p in items)

print(total_price(products))   # 12500000.0
```

---

## Code

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    title: str
    done: bool = False
    tags: List[str] = field(default_factory=list)

t1 = Task("belajar typing")
t2 = Task("bikin api", done=True, tags=["FastAPI"])
print(t1)
print(t2)
print(t1 == Task("belajar typing"))   # True (eq otomatis)
```

---

## Explanation

- Annotations murni hint; untuk validasi runtime di API, gunakan **Pydantic** (dipakai FastAPI) — lihat Day 27.
- `default_factory` penting agar list/dict default tidak terbagi antar instance.
- Dataclass menyusutkan boilerplate → lebih fokus ke logika.
- `Optional[X]` sama dengan `Union[X, None]`.

---

## Common Mistakes

1. Mengira annotation memaksa tipe → tidak, perlu runtime validation terpisah.
2. `def f(x=[])` error pattern → pakai `field(default_factory=list)`.
3. Lupa `from typing import ...` → `NameError`.
4. Salah syntax `Optional` harus `Union[X,None]` atau `X | None` (py3.10+).
5. Membuat dataclass dengan field mutable non-factory.

---

## Manual Exercises

### Exercise 1

Annotasi fungsi `add(a,b) -> int`.

### Exercise 2

Fungsi `first_name(full: str) -> str`.

### Exercise 3

Fungsi `find_index(items: List[str], target: str) -> Optional[int]`.

### Exercise 4

Dataclass `Book(title, author, pages)`. Buat 2 object & bandingkan.

### Exercise 5

Dataclass `Student` dengan `grades: List[int]` pakai `default_factory`; method `average()`.

---

## Challenge — Minimal Exercise

Buat dataclass `Rectangle(width: float, height: float)` dengan method `area() -> float`.

---

## Reflection

1. Kenapa annotation tidak memaksa tipe?
2. Apa beda hint (annotation) dan validasi runtime?
3. Kenapa `default_factory` diperlukan?
4. Apa kelebihan `@dataclass`?
5. Kapan kamu memakai `Optional`?

---

## Checklist

- [ ] Bisa annotasi fungsi
- [ ] Bisa memakai `Optional/Union/List/Dict`
- [ ] Bisa `@dataclass`
- [ ] Mengerti hint vs runtime checking
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 3**

```python
from typing import Optional

def find_index(items: list[str], target: str) -> Optional[int]:
    for i, n in enumerate(items):
        if n == target:
            return i
    return None
```

**Exercise 5**

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    grades: list[int] = field(default_factory=list)
    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0
```

</details>
