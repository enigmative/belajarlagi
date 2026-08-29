# CodeIgniter — Model, Database, & Validation

## Learning Objective

- Membuat Model & koneksi database
- Memakai Query Builder
- Validation server-side
- Migration + Seeder (pengenalan)

---

## Theory

### Model dasar

```php
<?php
namespace App\Models;

use CodeIgniter\Model;

class UserModel extends Model
{
    protected $table = 'users';
    protected $primaryKey = 'id';
    protected $allowedFields = ['name', 'email', 'role'];
    protected $useTimestamps = true;
}
?>
```

```php
$m = new UserModel();
$m->insert(['name' => 'Amir', 'email' => 'a@b.co', 'role' => 'admin']);
$user = $m->find(1);            // by PK
$all  = $m->findAll();          // semua
$admin = $m->where('role', 'admin')->findAll();
$m->update(1, ['role' => 'user']);
$m->delete(1);
```

### Query Builder (tanpa model)

```php
<?php
$db = db_connect();
$rows = $db->table('users')
           ->where('role', 'admin')
           ->orderBy('name', 'asc')
           ->limit(10)
           ->get()->getResult();
?>
```

### Validation

```php
$this->validate([
    'email' => 'required|valid_email',
    'age'   => 'permit_empty|is_natural_no_zero',
]);
```

---

## Analogy

Model (Eloquent/CI Model) = "asisten pribadi" tabel: tahu cara simpan, ambil, update, hapus — kamu tidak perlu menulis `SELECT` mentah tiap kali. Query Builder = cara aman menyusun SQL tanpa string rawan typo/SQL injection.

---

## Examples

```php
<?php
namespace App\Models;

use CodeIgniter\Model;

class EmployeeModel extends Model
{
    protected $table = 'employees';
    protected $allowedFields = ['name', 'department_id', 'salary'];
}

$m = new EmployeeModel();
$engineers = $m->where('department_id', 2)->orderBy('salary', 'desc')->findAll();
?>
```

---

## Code

```php
public function store()
{
    $rules = [
        'name'  => 'required|min_length[3]|max_length[50]',
        'email' => 'required|valid_email',
        'age'   => 'required|is_natural_no_zero',
    ];
    if (!$this->validate($rules)) {
        return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
    }
    $this->userModel->insert($this->request->getPost());
    return redirect()->to('/users');
}
```

---

## Explanation

- Model adalah tempat satu-satunya akses data (repository-ish).
- Query Builder otomatis meng-escape nilai → aman dari SQL injection.
- Validation: `required|valid_email|is_natural_no_zero` dsb.
- `withInput()` mengembalikan input ke form agar tidak hilang saat error.
- Migration/seeder: definisikan schema & data awal via kode (versi terdokumentasi).

---

## Common Mistakes

1. SQL mentah langsung di controller.
2. Lupa `allowedFields` → insert/update diam-diam gagal.
3. Tidak validasi → data kotor masuk DB.
4. Mengambil semua kolom `SELECT *` padahal cuma butuh 2.
5. Insert/update tanpa handle duplikat (cek unique dulu).

---

## Manual Exercises

### Exercise 1
Buat `NoteModel` (table notes, allowedFields).

### Exercise 2
CRUD lengkap: insert, find, where, update, delete.

### Exercise 3
Query Builder: join `employees` + `departments`.

### Exercise 4
Rule: `password` min 8 + konfirmasi.

### Exercise 5
Buat branch filter `?role=` dengan `where`.

---

## Challenge — Minimal Exercise

Model `EmployeeModel` dengan method `byDepartment($deptId)` yang mengembalikan employee di department tersebut (desc by salary).

---

## Reflection

1. Kenapa semua akses data lewat model?
2. Bagaimana Query Builder mencegah SQL injection?
3. Kenapa validasi penting server-side?
4. Apa beda migration vs seeder?
5. Kapan `withInput()` diperlukan?

---

## Checklist

- [ ] Bisa model CRUD
- [ ] Bisa Query Builder + where/order/limit
- [ ] Bisa validasi
- [ ] Mengenal migration & seeder
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 4

```php
'password'  => 'required|min_length[8]',
'konfirmasi' => 'required|matches[password]',
```

Exercise 5

```php
$rows = $db->table('employees')
           ->where('role', $this->request->getGet('role'))
           ->get()->getResult();
```

</details>