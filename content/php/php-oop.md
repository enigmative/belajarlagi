# PHP — OOP

## Learning Objective

- Membuat class, object, constructor, property, method
- Menggunakan inheritance, interface, abstract class, trait
- Memahami encapsulation & polymorphism
- Menerapkan namespace + use

---

## Theory

### Class dasar

```php
<?php
class User {
    public string $name;              // property dengan tipe
    private string $password;         // encapsulation

    public function __construct(string $name, string $password) {
        $this->name = $name;
        $this->password = $password;
    }

    public function greet(): string {
        return "Hello, {$this->name}";
    }
}

$u = new User("John", "rahasia");
echo $u->greet();
?>
```

### Inheritance

```php
<?php
class Admin extends User {
    public function greet(): string {   // override / polymorphism
        return "Admin " . parent::greet();
    }
}
?>
```

### Interface

```php
<?php
interface Payable {
    public function amount(): float;
}

class Invoice implements Payable {
    public function amount(): float {
        return 100000.0;
    }
}
?>
```

### Abstract class

```php
<?php
abstract class Payment {
    abstract public function process(): void;
}
class CashPayment extends Payment {
    public function process(): void {
        echo "cash processed";
    }
}
?>
```

### Trait

```php
<?php
trait HasCreatedAt {
    public function createdAt(): string {
        return date('Y-m-d H:i:s');
    }
}
class Note { use HasCreatedAt; }
?>
```

---

## Analogy

Class = cetakan; object = hasil cetakan. Interface = kontrak "harus punya method X". Abstract class = cetakan setengah jadi (wajib dilengkapi method abstract). Trait = potongan kode yang bisa "ditempel" ke beberapa class.

---

## Examples

```php
<?php
namespace App\Models;

class Employee {
    private int $id;
    public string $name;
    public function __construct(int $id, string $name) {
        $this->id = $id;
        $this->name = $name;
    }
    public function id(): int { return $this->id; }
}
?>
```

```php
<?php
use App\Models\Employee;
$emp = new Employee(1, "John");
echo $emp->name;
?>
```

---

## Code

```php
<?php
interface Storage {
    public function save(string $key, string $value): void;
}

class FileStorage implements Storage {
    public function save(string $key, string $value): void {
        file_put_contents("storage/$key.txt", $value);
    }
}

$storage = new FileStorage();
$storage->save("user", "John");
?>
```

---

## Explanation

- `private`/`protected`/`public` = encapsulation.
- Interface: definisi kontrak (implementor wajib memenuhi).
- Abstract class: bisa punya implementasi + method abstract.
- Polymorphism: subclass mengganti perilaku method base.
- Trait: komposisi (PHP tidak punya multiple inheritance).
- `namespace` + `use` = organisasi modul.

---

## Common Mistakes

1. Membiarkan property `public` padahal seharusnya `private` + getter.
2. Interface vs abstract class salah konteks.
3. Lupa `parent::` saat override.
4. Trait untuk tanggung jawab yang seharusnya dungsi terpisah.
5. Constructor tanpa `$this->`.

---

## Manual Exercises

### Exercise 1
Class `Product(name, price)` + method `total(qty)`.

### Exercise 2
Interface `Logger` + class `FileLogger` implementasi.

### Exercise 3
Abstract `Shape` + `Circle`/`Square` dengan `area()`.

### Exercise 4
Trait `Timestamps` dipakai 2 class.

### Exercise 5
Namespace + `use` untuk class `Order`.

---

## Challenge — Minimal Exercise

Class `solve` yang menerima `Employee` dengan method `getSalary()`, dan subclass `Manager` yang menggandakan salary dengan override.

---

## Reflection

1. Apa beda public/private/protected?
2. Kapan interface vs abstract class?
3. Apa itu polymorphism?
4. Kenapa trait ada di PHP?
5. Bagaimana namespace membantu proyek besar?

---

## Checklist

- [ ] Bisa class + constructor + method
- [ ] Bisa inheritance & override
- [ ] Bisa interface & abstract class
- [ ] Bisa trait
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```php
<?php
abstract class Shape {
    abstract public function area(): float;
}
class Circle extends Shape {
    public function __construct(private float $r) {}
    public function area(): float { return pi() * $this->r ** 2; }
}
echo (new Circle(2))->area();  // ~12.57
?>
```

</details>