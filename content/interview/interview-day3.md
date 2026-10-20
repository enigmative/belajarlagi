# Interview Day 3 — React, Live Coding & Interview

Target hari ini: kamu bisa menjelaskan React dengan bahasa sederhana, mengerjakan live coding sambil berbicara, dan menjawab pertanyaan lisan tanpa panik.

## Jadwal 3 Jam

| Waktu | Materi |
|---|---|
| 60 menit | React: JSX, props, state, hooks, Context, import/export |
| 75 menit | Live coding: FizzBuzz, string, hitung item, max, counter, fetch, Spring CRUD |
| 45 menit | Interview lisan: 8 pertanyaan dan cara menjawabnya |

## Bagian 1 — React

### Apa itu React?

React adalah library JavaScript untuk membangun UI berdasarkan **component**. Setiap component adalah function yang mengembalikan **JSX** (tampilan yang mirip HTML).

```jsx
function Hello() {
  return <h1>Halo!</h1>;
}
```

Analogi: React seperti menyusun UI dari balok LEGO. Setiap balok adalah component yang bisa dipakai ulang dan digabung.

Di Laravel/Blade, kamu mungkin menulis:

```blade
<h1>Halo, {{ $name }}</h1>
```

Di React, tampilan ditulis di dalam JavaScript dan data dikirim sebagai props.

### JSX

JSX bukan HTML murni. Beberapa aturan:

- `class` menjadi `className`.
- `for` menjadi `htmlFor`.
- Ekspresi JavaScript memakai `{ }`.
- Tag harus ditutup, termasuk `<img />` dan `<input />`.
- Satu component hanya boleh mengembalikan satu elemen induk; gunakan `<div>` atau `<>...</>`.

```jsx
function UserCard({ name, age }) {
  return (
    <div className="card">
      <h2>{name}</h2>
      <p>Umur: {age}</p>
      {age >= 18 ? <span>Dewasa</span> : <span>Anak</span>}
    </div>
  );
}
```

### Props

Props adalah data dari parent ke child. Props **read-only**.

```jsx
function Hello({ name = 'Guest' }) {
  return <h1>Hello, {name}</h1>;
}

<Hello name="Ada" />
<Hello />
```

Hasilnya `Hello, Ada` dan `Hello, Guest`.

Kalau child ingin mengubah data, parent mengirim callback:

```jsx
function Child({ onSave }) {
  return <button onClick={() => onSave('data baru')}>Simpan</button>;
}
```

### State dan `useState`

State adalah data internal component yang bisa berubah dan memicu render ulang.

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      {count}
    </button>
  );
}
```

Aturan penting:

- Jangan mengubah state langsung (`count++`). Gunakan setter.
- Kalau nilai baru bergantung pada nilai lama, gunakan functional update `setCount(c => c + 1)`.
- State baru terlihat pada render berikutnya, bukan langsung setelah `setCount`.

### `useEffect`

`useEffect` menjalankan **side effect** setelah render: fetch, timer, event listener, mengubah title.

```jsx
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);
```

Dependency array:

| Dependency | Kapan effect jalan |
|---|---|
| tidak ada | setiap render |
| `[]` | sekali setelah mount |
| `[count]` | setiap `count` berubah |

Effect bisa mengembalikan **cleanup**:

```jsx
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
}, []);
```

Cleanup mencegah timer, subscription, atau fetch bocor saat component hilang.

Catatan: di React StrictMode development, effect bisa dijalankan dua kali untuk membantu menemukan cleanup yang salah. Ini bukan bug.

### Context

Context mengirim data ke banyak component tanpa props drilling.

```jsx
import { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  const theme = useContext(ThemeContext);
  return <p>{theme}</p>;
}
```

Tanpa Provider, `useContext` mengembalikan default value. Dengan Provider, ia mengembalikan `value` terdekat.

Kapan dipakai: tema, bahasa, user login, keranjang sederhana. Untuk state kompleks yang sering berubah, Context bisa menyebabkan banyak render; library seperti Redux/Zustand bisa lebih tepat.

### Import dan Export

```js
// math.js
export const add = (a, b) => a + b;
export default function multiply(a, b) { return a * b; }

// app.js
import multiply, { add } from './math.js';
```

- **Named export** → memakai kurung kurawal, nama harus cocok (atau `as`).
- **Default export** → tanpa kurung kurawal, nama bebas.
- `Component` dari React adalah named export: `import { Component } from 'react';`.

### List dan Key

```jsx
function UserList({ users }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

Setiap item butuh `key` yang stabil, biasanya ID. Jangan memakai index kalau urutan bisa berubah.

### Aturan Hooks

1. Panggil hooks hanya di **top-level** component atau custom hook.
2. Jangan panggil di dalam `if`, loop, atau setelah early return.
3. Urutan hooks harus sama di setiap render.

Contoh salah:

```jsx
function UserList({ users, loading }) {
  if (loading) return <p>Loading...</p>;
  const [selected, setSelected] = useState(null); // salah
}
```

Contoh benar:

```jsx
function UserList({ users, loading }) {
  const [selected, setSelected] = useState(null);

  if (loading) return <p>Loading...</p>;
}
```

### Jembatan dari Laravel/Blade

| Laravel / Blade | React |
|---|---|
| Blade component | function component |
| `@props(['name'])` | props destructuring |
| `{{ $name }}` | `{name}` |
| `@if` | ternary / `&&` |
| `@foreach` | `.map()` + `key` |
| Alpine.js state | `useState` |
| Blade layout/slot | component composition + `children` |
| Session/global config | Context (untuk UI) |

React bukan pengganti backend. React mengurus tampilan; Laravel/Spring tetap mengurus data dan aturan bisnis.

## Bagian 2 — Live Coding

### Cara Menghadapi Live Coding

Jangan langsung menulis kode. Ikuti urutan ini:

1. **Dengarkan dan klarifikasi.** Tanyakan input, output, edge case, dan batasan.
2. **Ulangi requirement dengan bahasamu.** “Jadi saya perlu mengembalikan array, bukan print, benar?”
3. **Beri contoh kecil.** Hitung manual 1–2 kasus.
4. **Jelaskan pendekatan sebelum coding.** Sebutkan struktur data dan kompleksitas.
5. **Tulis kode sambil menjelaskan.** Jangan diam terlalu lama.
6. **Test dengan contoh.** Cek edge case: kosong, satu elemen, angka negatif.
7. **Sebutkan kompleksitas dan kemungkinan perbaikan.**

Yang dinilai bukan hanya jawaban benar, tetapi cara berpikir dan komunikasi.

### Pola Live Coding yang Perlu Dikuasai

| Soal | Pola utama | Kompleksitas |
|---|---|---|
| FizzBuzz | loop + modulus + urutan kondisi | O(n) |
| Reverse string | dua pointer atau built-in | O(n) |
| Hitung item | frequency map | O(n) |
| Max number | linear scan | O(n) |
| React counter | `useState` + event | — |
| React fetch | `useEffect` + loading/error + cleanup | — |
| Spring CRUD | controller + service + DTO | — |

### Template Komentar Saat Coding

Ucapkan hal seperti:

- “Saya mulai dari edge case array kosong.”
- “Saya pakai loop karena hanya butuh satu kali lewat.”
- “Saya simpan hasil di array baru supaya input tidak berubah.”
- “Saya cek `response.ok` karena fetch tidak otomatis error untuk 404.”
- “Saya gunakan constructor injection supaya dependency jelas.”

## Bagian 3 — Interview Lisan

### Struktur Jawaban Teknis

Gunakan pola **Definisi → Contoh → Trade-off → Pengalaman**:

1. **Definisi:** satu kalimat sederhana.
2. **Contoh:** satu kasus nyata atau potongan kode.
3. **Trade-off:** kapan cocok, kapan tidak.
4. **Pengalaman:** jujur tentang apa yang pernah kamu pakai.

Contoh untuk “Apa itu dependency injection?”:

“Dependency injection adalah pola di mana class menerima dependency dari luar, bukan membuatnya sendiri. Contohnya `OrderService` menerima `PaymentService` lewat constructor. Di Laravel container mengisi type-hint; di Spring constructor injection melakukan hal yang sama. Keuntungannya mudah diuji dan implementasi bisa diganti.”

### Tips Menjawab

- Jangan menghafal paragraf. Hafalkan **poin**.
- Kalau tidak tahu, katakan: “Saya belum memakai itu di produksi, tetapi yang saya pahami adalah...” lalu jelaskan konsepnya.
- Jangan mengklaim pengalaman yang tidak ada. Interviewer akan mengejar detail.
- Kalau pertanyaannya luas, tanyakan konteks: “Apakah yang dimaksud REST untuk CRUD atau untuk integrasi?”
- Akhiri dengan ringkasan satu kalimat.

### Delapan Pertanyaan Lisan

1. Apa itu dependency injection?
2. Apa bedanya REST dan GraphQL?
3. Apa bedanya `@Bean` dan `@Component`?
4. Apa bedanya `@Primary` dan `@Qualifier`?
5. Apa bedanya props dan state?
6. Jelaskan `useEffect` dan dependency array.
7. Apa bedanya `var`, `let`, dan `const`?
8. Apa itu NullPointerException dan cara mencegahnya?

Jawaban lengkap ada di bank soal:

- [Dependency injection](#/interview/oral-01-dependency-injection)
- [REST vs GraphQL](#/interview/oral-02-rest-vs-graphql)
- [@Bean vs @Component](#/interview/oral-03-bean-vs-component)
- [@Primary vs @Qualifier](#/interview/oral-04-primary-vs-qualifier)
- [Props vs state](#/interview/oral-05-props-vs-state)
- [useEffect](#/interview/oral-06-useeffect)
- [var/let/const](#/interview/oral-07-var-let-const)
- [NullPointerException](#/interview/oral-08-npe)

## Checklist Hari 3

- [ ] Menjelaskan JSX dan perbedaan `class` vs `className`.
- [ ] Menjelaskan props vs state.
- [ ] Menjelaskan `useState` dan functional update.
- [ ] Menjelaskan `useEffect` dan tiga bentuk dependency array.
- [ ] Menjelaskan Context dan kapan dipakai.
- [ ] Menjelaskan named vs default import.
- [ ] Menjelaskan aturan hooks dan key pada list.
- [ ] Mengerjakan FizzBuzz sambil berbicara.
- [ ] Mengerjakan reverse string, hitung item, dan max.
- [ ] Membuat counter dan fetch component.
- [ ] Menjelaskan struktur Spring CRUD.
- [ ] Menjawab 8 pertanyaan lisan dengan suara keras.
- [ ] Merekam mock interview 15 menit.

## Mock Interview 15 Menit

Minta teman atau rekam dirimu sendiri:

1. Perkenalan 1 menit.
2. Jelaskan satu project Laravel/Python yang pernah kamu buat (3 menit).
3. Soal Java trace atau output (3 menit).
4. Pertanyaan Spring: bean, DI, @Primary (3 menit).
5. Pertanyaan React: props/state/useEffect (3 menit).
6. Kamu bertanya balik ke interviewer (2 menit).

Setelah selesai, tonton rekamanmu. Perbaiki tiga hal: terlalu banyak “eee”, penjelasan terlalu bertele-tele, atau tidak menyebut trade-off.

## Setelah 3 Hari

Kamu tidak akan hafal semuanya, dan itu normal. Yang penting:

- Kamu bisa membaca kode sederhana dan menjelaskan alurnya.
- Kamu tahu istilah utama dan bisa menghubungkannya dengan pengalaman Laravel.
- Kamu punya cara berpikir untuk soal yang belum pernah dilihat.
- Kamu jujur tentang apa yang sudah dan belum kamu kuasai.

Kembali ke [halaman Interview Prep](#/interview) untuk melihat progres dan soal yang masih salah.
