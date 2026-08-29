# JavaScript — DOM & Events

## Learning Objective

- Memilih & mengubah elemen DOM
- Menangani event (click, submit, input)
- Menggunakan event listener
- Membuat interaksi dasar frontend

---

## Theory

### Selector

```javascript
document.getElementById('app');
document.querySelector('button#save');
document.querySelectorAll('.item');   // NodeList
```

### Mengubah konten/atribut

```javascript
const el = document.querySelector('#message');
el.textContent = 'Halo';          // aman (tidak parse HTML)
el.innerHTML = '<b>Halo</b>';     // HATI-HATI raw HTML → XSS
el.classList.add('active');
el.setAttribute('data-id', '5');
```

### Event

```javascript
const btn = document.querySelector('#save-btn');
btn.addEventListener('click', () => {
    const input = document.querySelector('#name');
    console.log('value:', input.value);
});
```

### Form submit

```javascript
document.querySelector('#form').addEventListener('submit', (e) => {
    e.preventDefault();          // hentikan reload halaman
    const data = new FormData(e.target);
    console.log(Object.fromEntries(data));
});
```

---

## Analogy

Document = "rak buku raksasa" yang berisi elemen HTML. QuerySelector = mencari rak tertentu berdasarkan selector CSS. Event = "bel / sensor": klik, ketik, submit — lalu kamu pasang fungsi yang merespons.

---

## Examples

```javascript
const list = document.querySelector('#todo-list');
document.querySelector('#btn-add').addEventListener('click', () => {
    const txt = document.querySelector('#todo-input').value.trim();
    if (!txt) return;
    const li = document.createElement('li');
    li.textContent = txt;
    list.appendChild(li);
    document.querySelector('#todo-input').value = '';
});
```

---

## Code — counter

```javascript
let count = 0;
const display = document.querySelector('#count');
document.querySelector('#btn-plus').addEventListener('click', () => {
    count += 1;
    display.textContent = count;
});
```

---

## Explanation

- `textContent` aman; `innerHTML` bisa XSS — jangan masukkan input user tanpa escape.
- `addEventListener` lebih baik dari `onclick=` (bisa banyak handler, mudah hapus).
- `preventDefault()` menghentikan perilaku default (submit → reload).
- Delegation: pasang satu listener di parent untuk banyak child (event bubbles).

---

## Common Mistakes

1. Pakai `innerHTML` untuk input user (XSS).
2. Lupa `e.preventDefault()` di submit.
3. QuerySelector `#` vs `.` salah.
4. Listener dipasang sebelum DOM siap (letakkan di bawah / pakai `DOMContentLoaded`).
5. Inline `onclick` bercampur bikin susah maintenance.

---

## Manual Exercises

### Exercise 1
Tombol ganti `textContent` paragraf.

### Exercise 2
Form submit: tampilkan input ke list tanpa reload.

### Exercise 3
Event delegation untuk klik pada list item.

### Exercise 4
Add/remove class `active`.

### Exercise 5
`DOMContentLoaded` untuk mulai init.

---

## Challenge — Minimal Exercise

Buat tampilan TODO mini: input + tombol → tambah item ke `<ul>`, tanpa XSS, tanpa reload.

---

## Reflection

1. Bedakan textContent vs innerHTML.
2. Kenapa `e.preventDefault()` dipakai?
3. Apa itu event delegation?
4. Mengapa menyimpan event di HTML buruk?
5. Bagaimana cara aman menampilkan input user?

---

## Checklist

- [ ] Bisa memilih elemen DOM
- [ ] Bisa addEventListener
- - [ ] Bisa form submit tanpa reload
- - [ ] Paham XSS rawan innerHTML
- - [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 2

```html
<input id="nama" />
<button id="simpan">Simpan</button>
<ul id="daftar"></ul>
```

```javascript
document.querySelector('#simpan').addEventListener('click', () => {
    const v = document.querySelector('#nama').value.trim();
    if (!v) return;
    const li = document.createElement('li');
    li.textContent = v;
    document.querySelector('#daftar').appendChild(li);
});
```

</details>