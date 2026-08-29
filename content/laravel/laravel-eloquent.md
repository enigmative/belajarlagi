# Laravel — Eloquent ORM & Relasi

## Learning Objective

- Model, Mass Assignment, Accessor/Mutator, Cast
- Relasi hasOne, hasMany, belongsTo, belongsToMany
- Eager vs Lazy Loading + N+1 problem
- Scopes, Pagination, Transactions, Query Builder

---

## Theory

### Model & mass assignment

```php
<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Employee extends Model
{
    protected $fillable = ['name', 'department_id', 'salary'];

    public function department(): BelongsTo
    {
        return $this->belongsTo(Department::class);
    }

    public function attendances(): HasMany
    {
        return $this->hasMany(Attendance::class);
    }

    protected $casts = [
        'hired_at' => 'datetime',
    ];
}
?>
```

### Relasi

```php
Employee::find(1)->department->name;      // belongsTo
Department::find(1)->employees;           // hasMany
User::find(1)->roles;                     // belongsToMany (pivot)
User::find(1)->profile;                   // hasOne
```

### Accessor / Mutator

```php
protected function nameUpper(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => strtoupper($value),
        set: fn (string $value) => trim($value),
    );
}
```

---

## Analogy

Eloquent = "jembatan ajaib" tabel → object. `$employee->department->name` membaca kolom dari tabel lain tanpa kamu menulis JOIN — itulah relasi. Mass assignment = sekali isi object (SQL `INSERT`) dari array — tapi kamu wajib daftar `fillable` agar tak mudah disuntik (mass assignment vulnerability).

---

## Examples

```php
// N+1 problem (buruk)
$employees = Employee::all();                 // 1 query
foreach ($employees as $e) {
    echo $e->department->name;                // +1 query TANPA eager loading → N+1!
}

// Eager loading (baik)
$employees = Employee::with('department')->get();  // 2 query + JOIN/split

// Hasil: 1 query employees + 1 query departments, bukan N+1
```

```php
// scope
public function scopeHighSalary($q, $min = 10000000)
{
    return $q->where('salary', '>=', $min);
}
Employee::highSalary(5000000)->get();
```

---

## Code — transaction

```php
<?php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    $order = Order::create([...]);
    foreach ($items as $item) {
        $order->items()->create($item);
    }
});
// commit otomatis kalau sukses; rollback kalau exception
?>
```

---

## Explanation

- `$fillable` = daftar kolom yang boleh diisi mass — keamanan penting.
- Relasi: `belongsTo` (karyawan → departemen punya FK), `hasMany` (departemen memiliki karyawan).
- N+1 adalah perangkap terbesar: `with()` untuk eager loading.
- Accessor = ubah saat baca; mutator = ubah saat tulis; cast = konversi tipe (datetime, json, enum).
- Transaction = semua atomik (seperti SQL BEGIN/COMMIT/ROLLBACK).

---

## Common Mistakes

1. Lupa `with()` → N+1 query.
2. `$fillable` tidak lengkap → data tak tersimpan.
3. Over-load `$fillable` (buka kolom sensitif `password`).
4. Loop query di dalam loop relasi.
5. Memakai query builder saat hanya butuh Eloquent (atau sebaliknya).

---

## Manual Exercises

### Exercise 1
Model `Post` relasi `author` (User) dan `comments` (Comment).

### Exercise 2
Eager loading: ambil posts + author + comments dalam 3 query.

### Exercise 3
Scope `published()` pada Post.

### Exercise 4
Accessor `fullName = first + last`.

### Exercise 5
Transaction: buat order + items.

---

## Challenge — Minimal Exercise

Query: 10 `Employee` terbaru bersama `department`, tanpa N+1 (pakai `with`).

---

## Reflection

1. Kenapa `$fillable` wajib ada?
2. Apa masalah N+1 dan solusinya?
3. Bedakan `hasMany` vs `belongsTo`.
4. Apa fungsi cast?
5. Kapan transaksi diperlukan?

---

## Checklist

- [ ] Bisa model + fillable + cast
- [ ] Bisa semua relasi utama
- [ ] Bisa eager loading mencegah N+1
- [ ] Bisa scope + accessor/mutator
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```php
$posts = Post::with(['author', 'comments'])->latest()->get();
foreach ($posts as $post) {
    echo $post->author->name . ': ' . $post->comments->count();
}
```

Exercise 4

```php
public function getFullNameAttribute(): string
{
    return $this->first_name . ' ' . $this->last_name;
}
```

</details>