# Laravel — Auth, Authorization, Queue, Events, dan Fitur Produksi

## Learning Objective

- Authentication (login, session, jwt/API)
- Authorization: Policy & Gate
- Events & Listeners
- Jobs, Queue, Scheduler, Mail/Notification
- Storage, Cache, Logging, API Resource

---

## Theory

### Auth

```bash
php artisan make:auth   # (Laravel 9: composer require laravel/ui/bootstrap auth) 
```

```php
Auth::attempt(['email' => $email, 'password' => $pass]);
Auth::user();
auth()->id();
Auth::logout();
```

### Authorization

```php
// Policy
php artisan make:policy PostPolicy

class PostPolicy {
    public function update(User $user, Post $post) {
        return $user->id === $post->author_id;
    }
}

// controller
$this->authorize('update', $post);
// blade
@can('update', $post) ... @endcan
```

```php
// Gate
Gate::define('manage-employees', fn (User $u) => $u->role === 'admin');
```

### Queue / Job

```php
php artisan make:job SendNotifJob;
dispatch(new SendNotifJob($user));
// .env QUEUE_CONNECTION=database | redis
php artisan queue:work
```

### Events

```php
php artisan make:event OrderCreated
php artisan make:listener SendOrderEmail
OrderCreated::dispatch($order);   // atau event(new OrderCreated($order))
```

---

## Analogy

Auth = "siapa kamu" (cerita pelanggan + tiket). Authorization = "kamu boleh ke ruang mana" (check role/pemilik). Queue = "tumpukan tugas" yang dikerjakan worker di latar (kirim email, generate laporan) agar response cepat. Event = "pengumuman pengeras suara" — banyak pendengar bereaksi tanpa si pengirim tahu.

---

## Examples

```php
public function store(Request $request, Post $post)
{
    $this->authorize('update', $post);   // authorization

    dispatch(new SendNotifJob($post->author));   // queue

    return redirect('/posts');
}
```

```php
// listener queue
class SendOrderEmail implements ShouldQueue
{
    public function handle(OrderCreated $event)
    {
        Mail::to($event->order->user)->send(new OrderReceipt($event->order));
    }
}
```

---

## Code — scheduler + cache

```php
// app/Console/Kernel.php (Laravel 11: routes/console.php)
Schedule::dailyAt('23:00')->job(GenerateReport::class);
Schedule::everyMinute()->call(fn () => Cache::forget('report'));

$users = Cache::remember('users.all', 3600, fn () => User::all());
```

---

## Explanation

- Jangan pernah meletakkan backend auth di frontend saja — API perlu `auth:sanctum`/JWT.
- Policy = authorization per resource, bukan dalam controller.
- Queue memindahkan kerja berat dari HTTP request (response cepat), worker jalan belakang.
- Cache bikin request baca jauh lebih cepat dengan memori (Redis/file).
- Notification = ease panggil email/SMS/database "di tempat".

---

## Common Mistakes

1. Auth + authorization campur; semua user bisa edit.
2. Policy tidak dipakai → cek manual berulang.
3. Queue misconfigured → job tidak jalan.
4. Cache expired/memori penuh tak ditangani.
5. Log error rahasia (token/password).

---

## Manual Exercises

### Exercise 1
Buat `PostPolicy` untuk `update` milik sendiri.

### Exercise 2
`Gate::define` admin untuk `delete-employee`.

### Exercise 3
Job `SendReceipt` dipanggil saat order dibuat (event).

### Exercise 4
Scheduler harian: backup/ringkasan.

### Exercise 5
Cache daftar user 10 menit.

---

## Challenge — Minimal Exercise

Set job `SendWelcomeMail` di-dispatch ketika user baru dibuat (event `UserCreated`), dengan implementasi listener yang `ShouldQueue`.

---

## Reflection

1. Apa beda authentication dan authorization?
2. Kapan pakai Policy vs Gate?
3. Kenapa queue perlu worker?
4. Apa gunanya event/listener?
5. Kapan memakai cache?

---

## Checklist

- [ ] Bisa auth login/logout
- [ ] Bisa policy + gate
- [ ] Bisa job + queue
- [ ] Bisa event/listener + scheduler + cache
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```php
// app/Providers/EventServiceProvider.php
protected $listen = [
    OrderCreated::class => [SendReceiptListener::class],
];
```

Exercise 5

```php
$users = Cache::remember('users.all', 600, fn () => User::all());
```

</details>