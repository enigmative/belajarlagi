# JavaScript — Async, Fetch, Promise, JSON

## Learning Objective

- Memahami JavaScript asynchronous (event loop, promise)
- Memakai fetch + async/await
- Mengolah JSON
- Memahami alur Browser → JS → HTTP → API → Database

---

## Theory

### Promise & async/await

```javascript
async function getUsers() {
    const response = await fetch('/api/users');
    const data = await response.json();
    console.log(data);
    return data;
}

getUsers().catch(err => console.error('gagal:', err));
```

### Error handling

```javascript
async function getUsers() {
    try {
        const res = await fetch('/api/users');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error(e);
        return [];
    }
}
```

### Promise langsung

```javascript
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
await wait(1000);
```

### JSON

```javascript
const u = JSON.parse('{"name":"Amir"}');      // string → object
const s = JSON.stringify({ name: 'Amir' });   // object → string
```

---

## Alur (konsep)

```text
Browser
  ↓ (fetch)
JavaScript (async)
  ↓ (HTTP request)
Backend API
  ↓ (query)
Database
  ↓ (response JSON)
JavaScript → render DOM
```

`fetch` mengembalikan Promise; `await` menunggu tanpa memblokir UI dengan cara kerja event loop.

---

## Analogy

Async = memesan makan di restoran: kamu tidak membeku menunggu masakan jadi; koki (server) menyiapkan, saat siap pramusaji (event loop) membawakan hasilnya (resolve). `await` duduk tenang sampai pesanan datang — sementara aplikasi lain tetap jalan.

---

## Examples

```javascript
async function showDashboard() {
    const [lessons, challenges] = await Promise.all([
        fetch('/api/lessons').then(r => r.json()),
        fetch('/api/challenges').then(r => r.json()),
    ]);
    console.log('lessons:', lessons.length, 'challenges:', challenges.length);
}
```

---

## Code

```javascript
async function loadAndRender() {
    const res = await fetch('/api/progress');
    const data = await res.json();
    const el = document.querySelector('#overall');
    if (el) el.textContent = data.overall_pct + '%';
}
loadAndRender();
```

---

## Explanation

- `await` hanya valid di dalam `async` function.
- `response.ok` cek status HTTP (2xx).
- `Promise.all` menjalankan beberapa fetch paralel.
- UI tidak terblokir selama tunggu jaringan → UX mulus.
- Tanpa async (XHR lama) lebih ribet; fetch modern lebih ringkas.

---

## Common Mistakes

1. `await` di luar `async` → SyntaxError.
2. Lupa cek `response.ok` → status error dianggap sukses.
3. Menunggu berurutan padahal bisa paralel (`await Promise.all`).
4. Tidak menangani `catch` → unhandled rejection.
5. Memakai `response.json()` yang bisa throw (body bukan JSON).

---

## Manual Exercises

### Exercise 1
`fetch('/api/lessons')` lalu tampilkan jumlah di halaman.

### Exercise 2
Fungsi `postNote(title, body)` dengan POST + JSON body.

### Exercise 3
Cek `response.ok` dan tampilkan pesan error.

### Exercise 4
`Promise.all` untuk dashboard (lessons + challenges).

### Exercise 5
Simulasi delay dengan `await wait(ms)`.

---

## Challenge — Minimal Exercise

Fungsi `solveGet(url)` yang fetch, cek `ok`, dan mengembalikan `{status, data}`; kalau gagal kembalikan `{status: null, data: null}` dengan log error.

---

## Reflection

1. Apa itu Promise?
2. Kenapa `await` tidak memblokir UI?
3. Apa kegunaan `Promise.all`?
4. Kenapa cek `response.ok`?
5. Bagaimana alur Browser → API → DB?

---

## Checklist

- [ ] Bisa fetch + async/await
- [ ] Bisa JSON parse/stringify
- [ ] Bisa error handling
- [ ] Paham alur Browser ↔ API
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```javascript
async function postNote(title, body) {
    const res = await fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, body }),
    });
    return res.json();
}
```

</details>