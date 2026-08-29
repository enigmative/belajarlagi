# Laravel — Routing, Controller, Blade, & Middleware

## Learning Objective

- Membuat project Laravel & memahami struktur
- Routing GET/POST/PUT/DELETE + resource
- Controller, Request, Response
- Template Blade
- Middleware

---

## Theory

### Setup

```bash
composer create-project laravel/laravel app
php artisan serve        # http://127.0.0.1:8000
php artisan make:controller UserController
php artisan make:middleware EnsureAdmin
```

### Routing

```php
<?php
// routes/web.php
Route::get('/', [HomeController::class, 'index']);
Route::get('/users', [UserController::class, 'index']);
Route::get('/users/{user}', [UserController::class, 'show']);
Route::post('/users', [UserController::class, 'store']);

// resource CRUD otomatis
Route::resource('posts', PostController::class);
// GET /posts, GET /posts/create, POST /posts,
// GET /posts/{post}, GET /posts/{post}/edit, PUT /posts/{post}, DELETE /posts/{post}
?>
```

### Controller

```php
<?php
namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index(Request $request)
    {
        $role = $request->query('role');
        $users = User::when($role, fn($q) => $q->where('role', $role))->get();
        return view('users.index', ['users' => $users]);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name'  => 'required|max:255',
            'email' => 'required|email|unique:users,email',
        ]);
        $user = User::create($validated);
        return redirect('/users')->with('success', 'User dibuat');
    }
}
?>
```

### Blade

```html
{{-- resources/views/users/index.blade.php --}}
<h1>Users</h1>
<ul>
  @foreach ($users as $user)
    <li>{{ $user->name }} ({{ $user->role }})</li>
  @endforeach
</ul>
```

---

## Analogy

Route = peta URL → controller; controller = koki: terima pesanan (Request), ambil bahan (Model), sajikan (Response/View). Middleware = penjaga pintu sebelum pesanan masuk dapur (cek login, log, throttle).

---

## Examples

```php
Route::middleware('auth')->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
    Route::resource('employees', EmployeeController::class);
});
```

Blade component:

```html
<x-layout title="Dashboard">
  <p>Selamat datang, {{ auth()->user()->name }}</p>
</x-layout>
```

---

## Code — resource penuh

```php
<?php
// routes/web.php
Route::resource('employees', EmployeeController::class);

// App/Http/Controllers/EmployeeController.php
public function index() {
    return view('employees.index', ['employees' => Employee::paginate(10)]);
}

public function edit(Employee $employee) {
    return view('employees.edit', ['employee' => $employee]);
}

public function update(Request $request, Employee $employee) {
    $validated = $request->validate([
        'name' => 'required|max:255',
    ]);
    $employee->update($validated);
    return redirect('/employees');
}
?>
```

---

## Explanation

- `artisan` = CLI: buat controller, migration, test, dsb.
- Route model binding `{user}` → otomatis fetch `User`.
- Blade `{{ }}` meng-escape otomatis (anti XSS).
- Validasi di Request/`$request->validate` → error otomatis dikembalikan ke form.
- Middleware `auth`, `admin`, `throttle` dipasang via route group.

---

## Common Mistakes

1. Menaruh semua di route closure → tanpa controller.
2. Lupa escape: pakai `{!! !!}` tanpa perlu.
3. Validasi hanya di frontend.
4. Hardcode URL `/users` daripada `route('users.index')`.
5. Middleware dipasang tapi logic ganda di controller.

---

## Manual Exercises

### Exercise 1
Buat `Route::resource('students', StudentController::class)` + controller minimal.

### Exercise 2
Blade: tampilkan list students.

### Exercise 3
Validasi `email` unique.

### Exercise 4
Middleware `admin` untuk halaman khusus.

### Exercise 5
Pagination `paginate(5)` + `{!! $users->links() !!}`.

---

## Challenge — Minimal Exercise

Buat route `GET /employees/{employee}` dengan model binding yang tampilkan detail employee via Blade.

---

## Reflection

1. Apa yang dilakukan `resource` route?
2. Bedakan route binding vs manual find.
3. Kenapa Blade aman dari XSS?
4. Untuk apa middleware?
5. Kapan pakai route group?

---

## Checklist

- [ ] Bisa buat project + artisan serve
- [ ] Bisa route + controller + blade
- [ ] Bisa validasi
- [ ] Bisa middleware
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```html
<ul>
  @foreach ($students as $s)
    <li>{{ $s->name }}</li>
  @endforeach
</ul>
```

Exercise 5

```php
public function index() {
    return view('users.index', ['users' => User::paginate(5)]);
}
```

```html
{{ $users->links() }}
```

</details>