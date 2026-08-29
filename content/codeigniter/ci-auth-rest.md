# CodeIgniter — Session, Auth, Filter, & REST API

## Learning Objective

- Memakai Session
- Implementasi Authentication & Authorization di CI4
- Membuat Filters
- Membuat REST API (JSON response)
- Error handling & logging

---

## Theory

### Session

```php
session()->set('user_id', 1);
$id = session()->get('user_id');
session()->destroy();
```

### Filter (middleware = before/after)

```php
<?php
// app/Filters/AuthFilter.php
namespace App\Filters;

use CodeIgniter\Filters\FilterInterface;
use CodeIgniter\HTTP\RequestInterface;
use CodeIgniter\HTTP\ResponseInterface;

class AuthFilter implements FilterInterface
{
    public function before(RequestInterface $request, $arguments = null)
    {
        if (!session()->get('user_id')) {
            return redirect()->to('/login');
        }
    }
    public function after(RequestInterface $request, ResponseInterface $response, $arguments = null) {}
}
?>
```

```php
// Config/Filters.php
public $filters = [
    'auth' => ['before' => ['users', 'dashboard']],
];
```

### REST API

```php
<?php
// menanggapi JSON
$this->response->setStatusCode(201)->setJSON([
    'status'  => 'success',
    'message' => 'user dibuat',
    'data'    => $user,
]);
?>
```

---

## Analogy

Session = kartu nametag agar server ingat "siapa kamu" antar request. Filter = penjaga gerbang: cek login sebelum masuk halaman/proteksi. API = membuka data via JSON agar aplikasi lain (frontend, mobile) bisa konsumsi.

---

## Examples

```php
public function login()
{
    $email = $this->request->getPost('email');
    $pass  = $this->request->getPost('password');

    $user = $this->userModel->where('email', $email)->first();
    if (!$user || !password_verify($pass, $user['password_hash'])) {
        return redirect()->back()->with('error', 'kredensial salah');
    }
    session()->set(['user_id' => $user['id'], 'role' => $user['role']]);
    return redirect()->to('/dashboard');
}

public function logout()
{
    session()->destroy();
    return redirect()->to('/login');
}
```

---

## Code — API users

```php
public function apiIndex()
{
    return $this->response->setJSON($this->userModel->findAll());
}

public function apiStore()
{
    $this->userModel->insert($this->request->getJSON(true));
    return $this->response->setStatusCode(201)->setJSON(['created' => true]);
}

public function apiDelete($id)
{
    $this->userModel->delete($id);
    return $this->response->setStatusCode(204);
}
```

---

## Explanation

- Jangan hash password simpan di app: `password_hash($pass, PASSWORD_DEFAULT)`; cek `password_verify`.
- Filter `auth` melindungi route — satu tempat, tidak per-controller.
- Aturan authorization (siapa boleh akses) → cek `role` dari session/DB permission.
- API response selalu beri status code benar (200/201/204/400/404).
- Logging: `log_message('error', 'pesan')` — wajib saat produksi.

---

## Common Mistakes

1. Simpan password plaintext / hashing tanpa salt-correct (password_hash).
2. Filter tidak diterapkan → route terbuka.
3. Session dianggap cookie-safe (session bisa di-hijack; tetap https + regenerate id).
4. API selalu 200 padahal error.
5. Logging sensitive data (jangan log password/token).

---

## Manual Exercises

### Exercise 1
Buat filter `auth` untuk route `/dashboard`.

### Exercise 2
Login menggunakan `password_hash`/`password_verify`.

### Exercise 3
Role check: hanya `admin` boleh `/users/create`.

### Exercise 4
API JSON: list + create user (201).

### Exercise 5
Logging error di catch block.

---

## Challenge — Minimal Exercise

Buat filter `isAdmin` yang redirect kalau role user bukan `admin`.

---

## Reflection

1. Apa perbedaan authentication dan authorization?
2. Bagaimana filter menyederhanakan proteksi?
3. Kenapa password harus di-hash?
4. Apa status code yang tepat untuk error API?
5. Kenapa session perlu regenerate?

---

## Checklist

- [ ] Bisa session set/get/destroy
- [ ] Bisa filter auth
- [ ] Bisa role-based authorization
- [ ] Bisa API JSON
- - [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```php
if (session()->get('role') !== 'admin') {
    return redirect()->to('/forbidden');
}
```

Exercise 5

```php
try {
    // simpan data
} catch (\Exception $e) {
    log_message('error', $e->getMessage());
    return redirect()->back()->with('error', 'gagal menyimpan');
}
```

</details>