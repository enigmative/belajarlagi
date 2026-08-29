# PHP — Composer, Autoloading, PSR, & SOLID

## Learning Objective

- Menggunakan Composer untuk dependency
- Memahami autoloading & PSR-4
- Menerapkan SOLID
- Dependency Injection sederhana

---

## Theory

### Composer

```bash
composer init
composer require monolog/monolog
composer install
```

`composer.json` menyimpan dependency; `vendor/` hasil install; `composer.lock` mengunci versi.

### Autoloading (PSR-4)

Namafile harus match namespace.

```json
{
    "autoload": {
        "psr-4": { "App\\": "src/" }
    }
}
```

```php
<?php
require __DIR__ . '/vendor/autoload.php';

use App\Models\User;   // → src/Models/User.php
$u = new User("Amir");
?>
```

Nama file `User.php` persis seperti class `User`, folder Java-like.

### SOLID

| Huruf | Prinsip | Ide |
|-------|---------|-----|
| S | Single Responsibility | satu class satu alasan berubah |
| O | Open/Closed | terbuka extension, tertutup modifikasi |
| L | Liskov | subclass bisa menggantikan parent |
| I | Interface Segregation | jangan paksa implement method tak dipakai |
| D | Dependency Inversion | tergantung abstraksi, bukan konkret |

---

## Analogy

Composer = pip (Python) / npm (JS): sumber library + dependency management. Autoloading = `import` otomatis. SOLID = aturan rumah tangga kode agar class tidak jadi "laci barang campur aduk".

---

## Examples

**Sebelum (melanggar DI / D):**

```php
<?php
class OrderMailer {
    public function send(Order $o): void {
        $mail = new Mailgun();   // hard dependency
        $mail->send($o);
    }
}
?>
```

**Sesudah (dependency injection):**

```php
<?php
interface Mailer { public function send(Order $o): void; }

class OrderMailer {
    public function __construct(private Mailer $mailer) {}
    public function send(Order $o): void { $this->mailer->send($o); }
}

$mailer = new OrderMailer(new MailgunAdapter());
?>
```

---

## Code

```php
<?php
// src/Helpers/Str.php
namespace App\Helpers;

class Str {
    public static function slug(string $s): string {
        return strtolower(trim(preg_replace('/[^A-Za-z0-9]+/', '-', $s), '-'));
    }
}
?>
```

```php
<?php
// index.php
require __DIR__ . '/vendor/autoload.php';
use App\Helpers\Str;
echo Str::slug("Belajar PHP OOP");   // belajar-php-oop
?>
```

---

## Explanation

- Autoloading membuat lazy require — hanya kelas yang dipakai yang dimuat.
- PSR-4: namespace ↔ folder. `App\Models\User` → `src/Models/User.php`.
- SOLID mengarahkan pemisahan tanggung jawab supaya mudah diuji & diganti.
- DI (D konstruk) memudahkan test/mocking: ganti implementasi tanpa ubah consumer.

---

## Common Mistakes

1. Lupa `composer dump-autoload` setelah ubah composer.json.
2. Case-sensitif filename vs class name (PSR-4).
3. `new` dependency di dalam method → susah dites (tantang DI).
4. Interface kekar (banci satu method) — violation I.
5. Class "god object" melakukan semuanya — violation S.

---

## Manual Exercises

### Exercise 1
`composer init` di folder kosong + buat autoload psr-4.

### Exercise 2
Struktur `src/Models/User.php` + autoload working.

### Exercise 3
Refactor: pindahkan `new DB()` keluar konstruktor (DI).

### Exercise 4
Buat `interface Notifier` dengan 2 implementasi dan consumer — vertifikasi L/D.

### Exercise 5
Identifikasi 3 class dari proyek (belajar/kerja) yang melanggar SOLID, tuliskan perbaikannya.

---

## Challenge — Minimal Exercise

Buat `App\Services\Logger` (interface), `FileLogger`, lalu consumer yang menerima logger via constructor (DI) — tanpa `new` di dalam.

---

## Reflection

1. Apa peran Composer?
2. Bagaimana PSR-4 bekerja?
3. Sebutkan satu prinsip SOLID dengan contoh.
4. Kenapa DI memudahkan testing?
5. Apa tanda class melanggar S?

---

## Checklist

- [ ] Bisa composer init/require/install
- [ ] Bisa autoload psr-4
- [ ] Bisa SOLID sederhana
- [ ] Bisa dependency injection
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 5 (contoh)

`OrderService` yang juga mengirim email + menulis log → pecah jadi `OrderService` + `Mailer` + `Logger`.

</details>