# Day 13 — OOP: Class & Object

## Learning Objective

- Mendefinisikan class dengan attribute & method
- Membuat object dari class (instansiasi)
- Menggunakan constructor `__init__` dan `self`
- Memahami `property`, `classmethod`, `staticmethod`
- Memahami encapsulation (publik vs konvensi privat `_`)

---

## Theory

### Class dasar

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello {self.name}"

u = User("John", 23)
print(u.name)       # John
print(u.greet())    # Hello John
```

- `class` mendefinisikan *template*.
- `__init__` adalah constructor — dijalankan saat object dibuat.
- `self` merujuk object tersebut sendiri.
- `u = User(...)` membuat object (instansiasi).

### Attribute vs Method

- **Attribute**: data milik object (`u.name`).
- **Method**: fungsi milik object (`u.greet()`).

### property

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        return 3.14 * self._radius ** 2

c = Circle(2)
print(c.area)       # 12.56  (dipanggil tanpa tanda kurung)
```

`@property` mengubah method menjadi seperti attribute (getter).

### classmethod & staticmethod

```python
class Employee:
    bonus_rate = 0.1

    def __init__(self, salary):
        self.salary = salary

    @classmethod
    def from_contract(cls, salary):
        # classmethod memakai cls, bukan instance
        return cls(salary * 1.2)

    @staticmethod
    def is_valid_salary(salary):
        # staticmethod tidak butuh self/cls
        return salary > 0
```

---

## Analogy

Class adalah **cetakan kue**; object adalah **kue hasil cetakan**. Cetakan menentukan bentuk (attribute) dan yang bisa dilakukan (method), tapi setiap kue punya isian sendiri-sendiri (nilai attribute berbeda).

---

## Examples

### Object bertingkat

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def discounted(self, pct):
        return self.price * (1 - pct / 100)

p = Product("Laptop", 12000000)
print(p.name, p.discounted(10))   # Laptop 10800000.0
```

---

## Code

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance   # konvensi private

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return amount
        return None

    @property
    def balance(self):
        return self._balance

acc = BankAccount("John", 100000)
acc.deposit(50000)
print(acc.balance)     # 150000
```

---

## Explanation

- OOP mengelompokkan **data + perilaku** dalam satu unit (object).
- `self` harus jadi parameter pertama method instance.
- Konvensi: attribute dengan awalan `_` dianggap "internal" (encapsulation ringan).
- `@property` memberi kontrol getter tanpa mengubah pemakaian (`obj.atribut`, bukan `obj.atribut()`).
- `classmethod` untuk factory/alternatif konstruktor; `staticmethod` untuk fungsi utilitas terkait tapi tanpa instance.

---

## Common Mistakes

1. Lupa `self` sebagai parameter pertama method → `TypeError`.
2. Lupa `self.` saat mengakses attribute di dalam method → `NameError`.
3. Mengira `@property` method dipanggil dengan `()`.
4. Mengisi attribute tanpa `__init__`.
5. Memakai object mutable sebagai default attribute (shared antar instance).

---

## Manual Exercises

### Exercise 1

Class `Student` dengan `name`, `grades` (list). Method `average()`.

### Exercise 2

Class `Book` dengan `title`, `author`. Method `describe()`.

### Exercise 3

Class `Circle` dengan `@property area` dan `@property circumference`.

### Exercise 4

Class `Counter` dengan method `increment()` dan `@property count`.

### Exercise 5

Class `BankAccount` (seperti contoh) dengan deposit/withdraw yang aman.

---

## Challenge — Minimal Exercise

Class `Rectangle` dengan `width`, `height`; method `area()` dan `perimeter()`.

---

## Reflection

1. Apa beda class dan object?
2. Apa peran `__init__` dan `self`?
3. Apa beda attribute dan method?
4. Kapan memakai `@property`, `@classmethod`, `@staticmethod`?
5. Jelaskan encapsulation dengan kata-kata sendiri.

---

## Checklist

- [ ] Bisa membuat class & object
- [ ] Bisa memakai `__init__` dan `self`
- [ ] Paham property/classmethod/staticmethod
- [ ] Bisa membuat BankAccount yang aman
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 1**

```python
class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades
    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0
```

**Exercise 4**

```python
class Counter:
    def __init__(self):
        self._count = 0
    def increment(self):
        self._count += 1
    @property
    def count(self):
        return self._count
```

</details>
