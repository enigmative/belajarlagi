# Day 14 — OOP: Inheritance & Polymorphism

## Learning Objective

- Mewarisi class dengan `class Child(Parent)`
- Menggunakan `super()` untuk memanggil method parent
- Meng-override method
- Memahami polymorphism (banyak bentuk lewat satu interface)
- Memahami abstraction (ABC) dan `@abstractmethod`

---

## Theory

### Inheritance dasar

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):            # override
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

d = Dog("Rex")
c = Cat("Kitty")
print(d.speak())   # Woof
print(c.speak())   # Meow
```

Child mewarisi attribute & method parent, dan bisa **override** (menimpa) method.

### super()

```python
class Animal:
    def __init__(self, name, legs):
        self.name = name
        self.legs = legs

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, legs=4)   # panggil constructor parent
        self.breed = breed
```

`super()` memanggil implementasi parent — dipakai agar tidak menulis ulang logika dasar.

### Polymorphism

```python
animals = [Dog("Rex"), Cat("Kitty")]
for a in animals:
    print(a.speak())   # Woof / Meow — bentuk berbeda via interface sama
```

Banyak class berbagi method dengan nama sama → kode call-site tidak peduli tipe konkret.

### Abstraction (ABC)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2
```

`ABC` + `@abstractmethod` memaksa subclass mengimplementasikan method — tidak bisa instantiate bentuk abstrak.

---

## Analogy

Inheritance seperti **template keluarga**: anak mewarisi sifat orang tua, tapi bisa menambahkan atau mengubah perilakunya sendiri. Polymorphism = semua anak bisa "bersuara", tapi bunyinya beda-beda — pemanggil cukup tahu "kamu bisa bersuara".

---

## Examples

### Polimorfisme gamblang

```python
class Payment:
    def pay(self, amount):
        raise NotImplementedError

class CreditCard(Payment):
    def pay(self, amount):
        return f"kartu: {amount}"

class EWallet(Payment):
    def pay(self, amount):
        return f"ewallet: {amount}"

def checkout(payment, amount):
    print(payment.pay(amount))

checkout(CreditCard(), 10000)   # kartu: 10000
checkout(EWallet(), 10000)      # ewallet: 10000
```

---

## Code

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, base):
        self.name = name
        self.base = base

    @abstractmethod
    def salary(self):
        pass

class Permanent(Employee):
    def salary(self):
        return self.base + 1000000

class Contract(Employee):
    def salary(self):
        return self.base * 0.9

emps = [Permanent("John", 8000000), Contract("Budi", 8000000)]
for e in emps:
    print(e.name, "->", e.salary())
```

---

## Explanation

- Inheritance → "is-a" relationship (Dog *adalah* Animal). Komposisi (punya) lebih cocok untuk "has-a".
- Override = menimpa implementasi parent dengan versi sendiri.
- `super()` mengurangi duplikasi dengan memakai kode parent.
- Polymorphism memungkinkan menulis kode sekali yang bekerja untuk banyak tipe.
- Composition over inheritance: jangan bikin hierarki dalam; lebih suka gabungkan object.

---

## Common Mistakes

1. Memakai inheritance hanya untuk "berbagi kode" padahal tidak ada hubungan is-a.
2. Lupa memanggil `super().__init__` sehingga parent tidak terinisialisasi.
3. Hierarki terlalu dalam → kompleks, susah dipahami.
4. Method override yang tidak konsisten signature.
5. Mencoba instantiate class `ABC` yang punya `@abstractmethod`.

---

## Manual Exercises

### Exercise 1

`Vehicle` base dengan `move()`; `Car` & `Bike` override move-nya.

### Exercise 2

`Person` base; `Student` & `Teacher` mewarisi dan `super().__init__`.

### Exercise 3

`Shape(ABC)` dengan `area()`; `Triangle` & `Rectangle` implementasi.

### Exercise 4

`Animal` dengan `make_sound()`; loop daftar hewan → polymorphic call.

### Exercise 5

`Account(ABC)` dengan `deposit` nyata + `interest` abstrak; `Savings` & `Checking` implementasi.

---

## Challenge — Minimal Exercise

Buat `Shape(ABC)` dengan method `area()`, dan 2 subclass `Square` & `Circle` yang mengimplementasikannya. Test keduanya via list.

---

## Reflection

1. Apa beda inheritance dan composition?
2. Apa fungsi `super()`?
3. Apa itu polymorphism dan kenapa berguna?
4. Kapan kamu pakai `ABC`?
5. Apa risiko hierarki inheritance yang terlalu dalam?

---

## Checklist

- [ ] Bisa mewarisi class
- [ ] Bisa memakai `super()`
- [ ] Bisa override method
- [ ] Paham polymorphism & ABC
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

**Exercise 3**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): pass

class Rectangle(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h

class Triangle(Shape):
    def __init__(self, b, h): self.b, self.h = b, h
    def area(self): return 0.5 * self.b * self.h
```

**Exercise 4**

```python
class Cat:
    def make_sound(self): return "Meow"
class Dog:
    def make_sound(self): return "Woof"

for a in [Cat(), Dog()]:
    print(a.make_sound())
```

</details>
