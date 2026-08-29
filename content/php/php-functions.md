# PHP — Function, Array, & Loop Lanjutan

## Learning Objective

- Menulis function dengan parameter, default, return
- Menguasai fungsi array bawaan (array_map, array_filter, array_reduce, sort)
- Memakai array multilevel
- Loop: for, foreach, while

---

## Theory

### Function

```php
<?php
function totalHarga($harga, $qty = 1) {   // default parameter
    return $harga * $qty;
}

echo totalHarga(10000);        // 10000  (qty default 1)
echo totalHarga(10000, 3);     // 30000

// type hint + nullable
function greet(?string $name): string {
    return "Halo, " . ($name ?? "tamu");
}
?>
```

### Array functions

```php
<?php
$nums = [1, 2, 3, 4, 5];

// map
$doubled = array_map(fn($n) => $n * 2, $nums);      // [2,4,6,8,10]

// filter
$even = array_filter($nums, fn($n) => $n % 2 === 0); // [2,4]

// reduce
$sum = array_reduce($nums, fn($c, $n) => $c + $n, 0); // 15

// sort
sort($nums);

// in / search
in_array(3, $nums);   // true
?>
```

---

## Analogy

`array_map`/`array_filter`/`array_reduce` = versi PHP dari list comprehension + zip-plus-aggrate di Python: transform → saring → kumpulkan.

---

## Examples

```php
<?php
$users = [
    ["name" => "John", "role" => "admin"],
    ["name" => "Budi", "role" => "user"],
];

$admins = array_filter($users, fn($u) => $u["role"] === "admin");
$names  = array_map(fn($u) => $u["name"], $users);

print_r($names);   // ["John","Budi"]
?>
```

---

## Code

```php
<?php
$scores = [70, 85, 92, 60];

$lulus = array_filter($scores, fn($s) => $s >= 75);
echo count($lulus) . " lulus";   // 2

$rata = array_sum($scores) / count($scores);
echo "rata-rata: $rata";
?>
```

---

## Explanation

- `fn($x) => ...` = arrow function (singkat) vs `function ($x) { ... }`.
- `array_filter` menahan KEY asli asli → gunakan `array_values()` bila butuh index berurut.
- Sering dipakai di production: map data ke view-model, filter query hasil, reduce ringkasan.
- Array di PHP = ordered map; hati-hati saat indeks campur.

---

## Common Mistakes

1. `array_filter` key tidak direset → `[1=>...]` mengejutkan.
2. Pakai loop manual padahal array_function sudah ada.
3. Merge array `+` (behavior aneh) vs `array_merge`.
4. Sorting mengubah array asli (sort vs usort dengan flag).
5. Tidak menangani array kosong di `array_reduce` initial value.

---

## Manual Exercises

### Exercise 1
Fungsi `duplicate(nums)` → array dikali 2.

### Exercise 2
Fungsi `hanyaGenap(nums)`.

### Exercise 3
Hitung total belanja `[["item"=>"A","price"=>10000], ...]`.

### Exercise 4
Sort array of assoc by key `name` (usort).

### Exercise 5
Gabung daftar nama menjadi string "John, Budi".

---

## Challenge — Minimal Exercise

`solve($nums, $times)` = `array_map` yang mengembalikan tiap elemen dikali `$times`.

---

## Reflection

1. Apa fungsi arrow function?
2. Kenapa `array_values` kadang dibutuhkan?
3. Bedakan `+` vs `array_merge`.
4. Kapan pakai `usort`?
5. Bagaimana reduce berguna untuk ringkasan?

---

## Checklist

- [ ] Bisa function + default + type hint
- [ ] Bisa map/filter/reduce
- [ ] Bisa array multilevel
- [ ] Bisa sort/merge dengan benar
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```php
<?php
$cart = [
    ["item" => "A", "price" => 10000],
    ["item" => "B", "price" => 20000],
];
$total = array_reduce($cart, fn($c, $x) => $c + $x["price"], 0);
echo $total;  // 30000
?>
```

Exercise 5

```php
<?php
$names = ["John", "Budi"];
echo implode(", ", $names);  // "John, Budi"
?>
```

</details>