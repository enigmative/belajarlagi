# PHP — Fundamentals

## Learning Objective

- Menjalankan PHP (built-in server, CLI)
- Menguasai variable, tipe, string, array
- Menggunakan kondisi & loop
- Paham perbedaan PHP vs Python (eksplisit $, array asosiatif)

---

## Theory

### Menjalankan PHP

```bash
php -v                  # versi
php -S localhost:8080   # server dev untuk web
php file.php            # jalankan script
```

### Variable & tipe

```php
<?php
$name = "John";        // string
$age = 23;             // int
$height = 170.5;       // float
$isDev = true;         // bool
$nothing = null;

echo "Halo $name";     // interpolasi
echo "Umur: " . $age;  // concatenation pakai "."
?>
```

### Array

```php
$list = [1, 2, 3];
$list[] = 4;                     // append
echo count($list);               // 4

$user = [
    "name" => "John",
    "role" => "admin"
];
echo $user["name"];
```

### Kondisi & loop

```php
<?php
$age = 20;
if ($age >= 18) {
    echo "adult";
} elseif ($age >= 13) {
    echo "teenager";
} else {
    echo "child";
}

for ($i = 1; $i <= 5; $i++) {
    echo $i;
}

foreach ($user as $key => $value) {
    echo "$key: $value";
}
?>
```

---

## Analogy

PHP seperti Python untuk web tapi dengan `$` di depan tiap variable dan array yang bisa bertindak sebagai "list + dict" sekaligus (array asosiatif ~ dictionary Python).

---

## Examples

```php
<?php
$users = [
    ["name" => "John", "role" => "admin"],
    ["name" => "Budi", "role" => "user"],
];

foreach ($users as $u) {
    if ($u["role"] === "admin") {
        echo $u["name"] . " - ADMIN\n";
    }
}
?>
```

---

## Code

```php
<?php
function greeting($name) {
    return "Halo, $name!";
}

echo greeting("Budi");
// php hello.php → Halo, Budi!
?>
```

---

## Explanation

- `<?php ... ?>` membungkus kode PHP.
- Variable diawali `$`; string concatenation pakai `.`.
- Array asosiatif berfungsi seperti dict.
- `===` memeriksa tipe + nilai; `==` longgar.
- Web: PHP paling sering memakai `$_GET`, `$_POST`, `$_SESSION`.

---

## Common Mistakes

1. Lupa `$` di depan nama variable.
2. Pakai `.` saat menggabung string (bukan `+`).
3. Array index berubah tanpa sadar (PHP array = ordered map).
4. `==` vs `===` (mis. `"1" == 1` true).
5. Mencampur echo tanpa tag `<?php`.

---

## Manual Exercises

### Exercise 1
Buat variable nama/umur, tampilkan kalimat.

### Exercise 2
Array asosiatif user, tampilkan semua key-value.

### Exercise 3
Loop 1-100, print genap/ganjil.

### Exercise 4
Fungsi `isKabisat(year)`.

### Exercise 5
Simulasi input `$data = ["scores" => [70, 80, 90]]`, hitung rata-rata.

---

## Challenge — Minimal Exercise

Buat file PHP yang menghitung `factorial(5)` dengan loop dan print hasilnya.

---

## Reflection

1. Apa kegunaan `$` dan `.` di PHP?
2. Bagaimana array asosiatif mirip dict Python?
3. Apa beda `==` dan `===`?
4. Bagaimana PHP dipakai untuk web?
5. Sebutkan perbedaan utama PHP vs Python.

---

## Checklist

- [ ] Bisa menjalankan PHP CLI
- [ ] Bisa variable, array, loop, kondisi
- [ ] Bisa function di PHP
- [ ] Paham sintaks `$`, `.`, `<?php`
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 4

```php
<?php
function isKabisat($y) {
    return $y % 4 === 0 && ($y % 100 !== 0 || $y % 400 === 0);
}
echo isKabisat(2024) ? "kabisat" : "bukan";  // kabisat
?>
```

Exercise 5

```php
<?php
$data = ["scores" => [70, 80, 90]];
$avg = array_sum($data["scores"]) / count($data["scores"]);
echo $avg;  // 80
?>
```

</details>