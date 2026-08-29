# CodeIgniter — MVC & Routing

## Learning Objective

- Memahami alur request di CodeIgniter 4
- Membuat controller & route GET/POST
- Mengirim view dengan data
- Mendapatkan input dari request

---

## Theory

### Alur request

```text
Request
  ↓
Router (Routes.php)
  ↓
Controller
  ↓
Model (opsional)
  ↓
View (response HTML)
```

### Route

```php
// app/Config/Routes.php
$routes->get('/', 'Home::index');
$routes->get('users', 'UserController::index');
$routes->get('users/(:num)', 'UserController::show/$1');
$routes->post('users', 'UserController::create');
$routes->put('users/(:num)', 'UserController::update/$1');
$routes->delete('users/(:num)', 'UserController::delete/$1');
```

### Controller

```php
<?php
namespace App\Controllers;

use CodeIgniter\Controller;

class UserController extends Controller
{
    public function index()
    {
        return view('users/index', ['users' => $this->getUsers()]);
    }

    public function show($id)
    {
        return view('users/show', ['id' => $id]);
    }

    public function create()
    {
        $name = $this->request->getPost('name');
        return "menambah $name";
    }
}
?>
```

### View

```html
<!-- app/Views/users/index.php -->
<h1>Daftar User</h1>
<ul>
  <?php foreach ($users as $user): ?>
    <li><?= esc($user['name']) ?></li>
  <?php endforeach; ?>
</ul>
```

---

## Analogy

Route = alamat peta; controller = satpam yang memutuskan apa yang dilakukan; model = gudang data; view = etalase tampilan. Pemisahan inilah inti MVC — tiap bagian ganti tanpa merusak yang lain.

---

## Examples

```php
$routes->get('posts', 'PostController::index');
$routes->get('posts/(:segment)', 'PostController::show/$1');
```

```php
class PostController extends Controller
{
    public function index()
    {
        return view('posts/index', ['title' => 'Semua Post']);
    }
}
```

---

## Code

File `app/Controllers/MahasiswaController.php`:

```php
<?php
namespace App\Controllers;

use CodeIgniter\Controller;

class MahasiswaController extends Controller
{
    public function index()
    {
        $data = [
            'nama' => 'Amir',
            'jurusan' => 'S.Kom',
        ];
        return view('mahasiswa/index', $data);
    }
}
?>
```

Route:

```php
$routes->get('mahasiswa', 'MahasiswaController::index');
```

---

## Explanation

- `/` di route → controller method `index`.
- `(:num)` = angka, `(:segment)` = teks tanpa slash, `(:any)` = apapun.
- Email/input: `$this->request->getGet()`, `getPost()`, `getVar()`.
- View escape: `esc()` mencegah XSS.
- Controller tipis: delegasikan bisnis ke Model/Service.

---

## Common Mistakes

1. Menaruh query SQL di controller (harus di model).
2. Lupa `esc()` di view → XSS.
3. Route order salah (catch-all sebelum specific).
4. View di-require manual, bukan `view()`.
5. Controller "gemuk" dengan semua logika.

---

## Manual Exercises

### Exercise 1
Buat route `GET /halo` → controller return "Halo Dunia".

### Exercise 2
Route `(/:num)` untuk `detail/$1`.

### Exercise 3
Controller baca `getPost('email')` dan tampilkan.

### Exercise 4
Tiga view: header, index, footer.

### Exercise 5
Route POST untuk simpan user.

---

## Challenge — Minimal Exercise

Buat controller `Users` dengan `index()` (list) dan `create()` (baca post `name`), plus route yang sesuai.

---

## Reflection

1. Apa alur request MVC di CI4?
2. Kenapa controller harus tipis?
3. Apa fungsi `esc()`?
4. Bedakan `(:num)` dan `(:segment)`.
5. Bagaimana view menerima data?

---

## Checklist

- [ ] Bisa buat route GET/POST/PUT/DELETE
- [ ] Bisa controller + view
- [ ] Bisa membaca request input
- [ ] Paham alur MVC
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```php
$routes->get('halo', 'Halo::index');

class Halo extends Controller {
    public function index() {
        return "Halo Dunia";
    }
}
```

Exercise 3

```php
public function create() {
    $email = $this->request->getPost('email');
    return "Email: $email";
}
```

</details>