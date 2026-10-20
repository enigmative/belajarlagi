"""Bank soal Interview Prep — Hari 3 (React, live coding, interview lisan)."""

QUESTIONS_DAY3 = [
    {
        "id": "core-02-react-import",
        "day": 3,
        "topic": "React",
        "title": "Import hanya Component dari React",
        "kind": "mcq",
        "origin": "asli",
        "points": 10,
        "concept": """### Default export vs named export

React mengekspor banyak hal sebagai **named export**: `Component`, `useState`, `useEffect`, `createContext`, dan lain-lain. Untuk mengambil salah satunya, gunakan kurung kurawal:

```js
import { Component } from 'react';
```

Kalau tanpa kurung kurawal, kamu mengambil **default export** dari module React (biasanya object React utama), bukan class `Component`.

**Analogi:** di Laravel/PHP, named export seperti memilih satu function tertentu dari file; default export seperti mengambil satu nilai utama yang diekspor file tersebut.""",
        "prompt": """Manakah sintaks yang benar untuk meng-import **hanya** `Component` dari library React?

- A. `import React.Component from 'react';`
- B. `import [ Component ] from 'react';`
- C. `import Component from 'react';`
- D. `import { Component } from 'react';`""",
        "hints": [
            "React mengekspor `Component` sebagai named export, bukan default export.",
            "Named import memakai kurung kurawal `{ ... }`.",
        ],
        "answer": """**Jawaban: D. `import { Component } from 'react';`**

**Kenapa opsi lain salah:**

| Opsi | Kenapa salah |
|---|---|
| A. `import React.Component from 'react';` | Sintaks import tidak memakai titik seperti itu. |
| B. `import [ Component ] from 'react';` | Kurung siku bukan sintaks import JavaScript. |
| C. `import Component from 'react';` | Ini mengambil default export, bukan named export `Component`. |
| D. `import { Component } from 'react';` | Benar: mengambil named export `Component`. |

**Catatan modern:** dengan JSX transform baru, kamu sering tidak perlu `import React from 'react'` hanya untuk JSX. Tetapi kalau kamu memang memakai `Component` secara eksplisit, import-nya tetap `import { Component } from 'react';`.

**Default vs named:**

```js
// named export di math.js
export const add = (a, b) => a + b;

// default export
export default function multiply(a, b) { return a * b; }

// import keduanya
import multiply, { add } from './math.js';
```

Nama default bebas diganti saat import; nama named harus sama (atau memakai `as`).""",
        "traps": """- **Mengira default export sama dengan named export.** `import Component from 'react'` tidak mengambil `Component`.
- **Mengira kurung kurawal opsional.** Untuk named export, kurung kurawal wajib.
- **Mengira React selalu harus di-import.** Dengan JSX transform modern, tidak selalu; tetapi named import tetap mengikuti aturan module.""",
        "speak": """“Component adalah named export dari React, jadi import-nya memakai kurung kurawal: import { Component } from react. Kalau tanpa kurung kurawal, itu default export, bukan Component.”""",
    },
    {
        "id": "core-03-react-hooks",
        "day": 3,
        "topic": "React",
        "title": "Apa kegunaan React hooks?",
        "kind": "mcq",
        "origin": "asli",
        "points": 10,
        "concept": """### Hooks = fitur React di function component

Sebelum hooks, state dan lifecycle hanya bisa dipakai di **class component**. Hooks memungkinkan function component memakai state (`useState`), side effect/lifecycle (`useEffect`), context (`useContext`), dan fitur lain tanpa menulis class.

Analogi: hooks seperti stopkontak di rumah. Kamu tidak perlu membangun ulang rumah (class) untuk memakai listrik (state/lifecycle); cukup pasang perangkat di stopkontak yang tersedia.""",
        "prompt": """Apa kegunaan React hooks?

- A. Optimasi aplikasi mobile
- B. Membuat efek visual otomatis
- C. Memungkinkan state dan lifecycle di function component
- D. Mengintegrasikan library UI seperti Bootstrap""",
        "hints": [
            "Pikirkan perbedaan class component dan function component sebelum hooks ada.",
            "Sebutkan dua hook dasar: `useState` dan `useEffect`.",
        ],
        "answer": """**Jawaban: C. Memungkinkan state dan lifecycle di function component.**

**Penjelasan:**

- `useState` memberi function component **state** yang bisa berubah dan memicu render ulang.
- `useEffect` menangani **side effect** dan lifecycle seperti “setelah render”, “ketika dependency berubah”, dan cleanup.
- `useContext`, `useReducer`, `useMemo`, `useCallback`, dan lain-lain memberi fitur tambahan tanpa class.

Contoh:

```jsx
import { useState, useEffect } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Kenapa opsi lain salah:** hooks bukan alat optimasi mobile, bukan efek visual otomatis, dan bukan integrasi UI library. Bootstrap bisa dipakai bersama React, tetapi itu bukan tujuan hooks.""",
        "traps": """- **Mengira hooks menggantikan JavaScript.** Hooks adalah API React, bukan bahasa baru.
- **Mengira `useEffect` sama dengan lifecycle class secara persis.** Konsepnya mirip, tetapi cara berpikirnya berbeda.
- **Mengira hooks hanya untuk state.** Ada hooks untuk context, ref, memo, dan lain-lain.""",
        "speak": """“Hooks memungkinkan function component punya state dan lifecycle. useState untuk state, useEffect untuk side effect. Sebelumnya dua hal itu hanya bisa di class component.”""",
    },
    {
        "id": "core-04-react-context",
        "day": 3,
        "topic": "React",
        "title": "Mengirim data tanpa props di setiap level",
        "kind": "mcq",
        "origin": "asli",
        "points": 10,
        "concept": """### Prop drilling dan Context

Kalau data harus dikirim dari komponen atas ke komponen bawah yang sangat dalam, biasanya props harus dilewatkan lewat banyak level. Ini disebut **prop drilling**.

**React Context** menyediakan “saluran” data yang bisa diakses langsung oleh komponen mana pun di bawah `Provider`, tanpa melewatkan props satu per satu.

Analogi: prop drilling seperti menyuruh setiap orang di rantai menyampaikan paket. Context seperti radio bersama: siapa pun yang punya receiver bisa mendengar siaran yang sama.""",
        "prompt": """Cara mengirim data melalui component tree tanpa mengoper props manual di setiap level adalah?

- A. React context
- B. Redux
- C. React Router
- D. React lifecycle methods""",
        "hints": [
            "Mekanisme bawaan React untuk menghindari prop drilling adalah Context.",
            "Redux juga bisa menyimpan state global, tetapi bukan mekanisme bawaan React yang dimaksud pada opsi ini.",
        ],
        "answer": """**Jawaban: A. React context.**

**Penjelasan:**

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
  return <ThemedButton />;
}

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Theme: {theme}</button>;
}
```

`ThemedButton` bisa membaca `theme` tanpa menerima props dari `Toolbar`.

**Kapan Context dipakai:**

- Tema (light/dark).
- Bahasa / locale.
- User yang sedang login.
- Keranjang belanja sederhana.

**Kapan tidak:** untuk state yang sering berubah dan kompleks, Context bisa menyebabkan banyak komponen re-render. Redux/Zustand bisa lebih tepat, tetapi Redux bukan mekanisme bawaan yang dimaksud soal. React Router untuk routing, lifecycle methods untuk class component.""",
        "traps": """- **Mengira Context menggantikan semua state management.** Untuk state kompleks, library khusus masih berguna.
- **Mengira Redux jawaban yang paling tepat.** Redux bisa menghindari prop drilling, tetapi soal menanyakan mekanisme React; Context adalah jawaban yang diharapkan.
- **Lupa `Provider`.** `useContext` hanya mendapat nilai dari Provider terdekat; tanpa Provider, nilainya default.""",
        "speak": """“React Context. Kita bungkus component tree dengan Provider, lalu komponen di bawahnya bisa mengambil nilai dengan useContext tanpa props drilling. Redux juga bisa, tapi Context adalah mekanisme bawaan React.”""",
    },
    {
        "id": "react-01-props",
        "day": 3,
        "topic": "React",
        "title": "Latihan: props dan default value",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### Props = input dari parent

Props adalah data yang dikirim parent ke child. Props bersifat **read-only**; child tidak boleh mengubahnya langsung.

Default value bisa diberikan saat destructuring:

```jsx
function Hello({ name = 'Guest' }) { ... }
```

**Analogi:** props seperti pesanan yang dikirim dari dapur ke meja; pelayan (child) menyajikan, tetapi tidak boleh mengubah pesanannya.
""",
        "prompt": """Apa yang dirender oleh dua pemakaian komponen berikut?

```jsx
function Hello({ name = 'Guest' }) {
  return <h1>Hello, {name}</h1>;
}

<Hello name="Ada" />
<Hello />
```

- A. `Hello, Ada` dan `Hello, Guest`
- B. `Hello, Ada` dan `Hello,`
- C. `Hello, Guest` dan `Hello, Guest`
- D. Error pada `<Hello />`""",
        "hints": [
            "Kalau props `name` diberikan, nilai itu yang dipakai.",
            "Kalau props tidak diberikan, default value `Guest` yang dipakai.",
        ],
        "answer": """**Jawaban: A. `Hello, Ada` dan `Hello, Guest`**

**Penjelasan:**

- `<Hello name="Ada" />` → props `name` berisi `"Ada"`, jadi merender `<h1>Hello, Ada</h1>`.
- `<Hello />` → props `name` tidak ada, sehingga default `"Guest"` dipakai dan merender `<h1>Hello, Guest</h1>`.

**Catatan:** props read-only. Kalau child ingin mengubah nilai, parent harus mengirim callback (misalnya `onNameChange`) dan parent yang mengubah state. Ini disebut **lifting state up**.""",
        "traps": """- **Mengira child boleh mengubah props.** Props read-only; perubahan harus lewat state parent.
- **Mengira default berlaku untuk `null`.** Default destructuring hanya berlaku untuk `undefined`, bukan `null`.
- **Lupa tanda kurung kurawal saat memakai props.** `{name}` adalah ekspresi JSX.""",
        "speak": """“Kalau name diberikan Ada, hasilnya Hello Ada. Kalau tidak diberikan, default Guest dipakai, jadi Hello Guest.”""",
    },
    {
        "id": "react-02-usestate",
        "day": 3,
        "topic": "React",
        "title": "Latihan: useState dan functional update",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### `useState` dan batching

`useState` mengembalikan dua nilai: state saat ini dan fungsi untuk mengubahnya.

```jsx
const [count, setCount] = useState(0);
```

Kalau kamu memanggil `setCount(count + 1)` dua kali dalam satu event handler, keduanya membaca `count` yang sama (stale). React juga melakukan batching. Untuk menambah berdasarkan nilai terbaru, gunakan **functional update**:

```jsx
setCount(c => c + 1);
```

**Analogi:** seperti papan skor; `setCount` adalah wasit yang memperbarui angka, dan React menampilkan papan versi terbaru.
""",
        "prompt": """Perhatikan komponen berikut:

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
    setCount(count + 1);
  }

  return <button onClick={handleClick}>{count}</button>;
}
```

Setelah tombol diklik **satu kali**, angka apa yang tampil?

- A. `0`
- B. `1`
- C. `2`
- D. `Error`""",
        "hints": [
            "Kedua `setCount` membaca nilai `count` yang sama pada render itu.",
            "React melakukan batching, jadi dua update dengan nilai lama tidak otomatis menjadi +2.",
        ],
        "answer": """**Jawaban: B. `1`**

**Kenapa bukan 2?**

Pada render tersebut, `count` bernilai 0. Kedua baris sebenarnya menjadi:

```js
setCount(0 + 1);
setCount(0 + 1);
```

React menbatch update dan hasil akhirnya `1`, bukan `2`. Ini sering disebut **stale closure**.

**Perbaikan dengan functional update:**

```jsx
function handleClick() {
  setCount(c => c + 1);
  setCount(c => c + 1);
}
```

Sekarang React menjalankan update berurutan berdasarkan nilai terbaru, sehingga hasilnya `2`.

**Aturan:** kalau nilai baru bergantung pada nilai sebelumnya, gunakan `setState(prev => next)`.""",
        "traps": """- **Mengira dua `setCount` selalu berarti +2.** Tergantung apakah memakai nilai lama atau functional update.
- **Mengira state berubah langsung setelah `setCount`.** State baru terlihat pada render berikutnya.
- **Mengubah state langsung.** Jangan `count = count + 1`; gunakan setter.""",
        "speak": """“Dua setCount itu sama-sama membaca count 0, jadi hasilnya 1. Kalau mau +2, gunakan functional update setCount(c => c + 1) dua kali.”""",
    },
    {
        "id": "react-03-useeffect",
        "day": 3,
        "topic": "React",
        "title": "Latihan: dependency array useEffect",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### Dependency array

`useEffect(() => { ... }, deps)` menjalankan effect setelah render, tergantung `deps`:

- `[]` → hanya setelah render pertama (di StrictMode development bisa dua kali).
- `[count]` → setiap `count` berubah.
- Tanpa array → setelah setiap render.

Effect bisa mengembalikan **cleanup function** untuk membatalkan subscription/timer/fetch.

**Analogi:** seperti alarm yang bisa diatur untuk bunyi sekali, setiap kali suatu nilai berubah, atau setiap saat—tergantung daftar dependency.
""",
        "prompt": """Kapan `console.log('mounted')` dijalankan?

```jsx
useEffect(() => {
  console.log('mounted');
}, []);
```

- A. Setiap kali komponen render
- B. Hanya setelah render pertama
- C. Sebelum komponen dirender
- D. Hanya saat komponen di-unmount""",
        "hints": [
            "Array kosong `[]` berarti tidak ada dependency yang berubah.",
            "Di React StrictMode mode development, effect bisa dijalankan dua kali untuk membantu menemukan bug.",
        ],
        "answer": """**Jawaban: B. Hanya setelah render pertama.**

**Penjelasan:**

- `[]` berarti effect tidak bergantung pada nilai apa pun, jadi hanya dijalankan sekali setelah mount.
- Di **StrictMode development**, React sengaja menjalankan mount → cleanup → mount lagi untuk mendeteksi effect yang tidak bersih. Jadi console bisa muncul dua kali saat development, tetapi perilaku produksinya sekali.

**Variasi:**

```jsx
useEffect(() => {
  console.log('setiap render');
});
```

Tanpa dependency array → setiap render.

```jsx
useEffect(() => {
  console.log('count berubah', count);
}, [count]);
```

Hanya saat `count` berubah.

**Cleanup:**

```jsx
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
}, []);
```

Cleanup mencegah timer bocor saat komponen di-unmount.""",
        "traps": """- **Mengira `[]` berarti effect tidak pernah jalan.** Effect tetap jalan sekali setelah mount.
- **Mengira StrictMode double-run adalah bug.** Itu sengaja untuk membantu menemukan cleanup yang salah.
- **Lupa cleanup.** Timer/subscription/fetch bisa terus berjalan setelah komponen hilang.""",
        "speak": """“Dependency array kosong berarti effect hanya jalan setelah render pertama. Di StrictMode development bisa dua kali, tapi di produksi sekali. Kalau ada dependency count, effect jalan setiap count berubah.”""",
    },
    {
        "id": "react-04-context",
        "day": 3,
        "topic": "React",
        "title": "Latihan: membaca Context",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### `createContext` + `Provider` + `useContext`

- `createContext(defaultValue)` membuat context.
- `<Context.Provider value={...}>` menyediakan nilai.
- `useContext(Context)` membaca nilai dari Provider terdekat.

Tanpa Provider, `useContext` mengembalikan default value.

**Analogi:** seperti jaringan listrik rumah; Provider adalah sumber listrik, dan komponen mana pun bisa colok ke sana tanpa menarik kabel dari atas ke bawah.
""",
        "prompt": """Apa yang dirender oleh komponen `Toolbar`?

```jsx
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

- A. `light`
- B. `dark`
- C. `undefined`
- D. Error karena Toolbar tidak menerima props""",
        "hints": [
            "`Toolbar` berada di dalam `ThemeContext.Provider`.",
            "Nilai Provider adalah `\"dark\"`, sedangkan `\"light\"` hanya default kalau tidak ada Provider.",
        ],
        "answer": """**Jawaban: B. `dark`**

**Penjelasan:**

`Toolbar` berada di dalam `ThemeContext.Provider` dengan `value="dark"`. Saat `useContext(ThemeContext)` dipanggil, React mencari Provider terdekat dan mengembalikan `"dark"`.

`"light"` adalah default value yang hanya dipakai jika tidak ada Provider di atas komponen.

**Tanpa Provider:**

```jsx
function App() {
  return <Toolbar />;
}
```

Hasilnya `light`.

**Catatan:** Context membuat komponen bisa membaca data tanpa props drilling, tetapi tetap bukan pengganti semua state management.""",
        "traps": """- **Mengira `createContext('light')` mengunci nilai.** Itu hanya default; Provider bisa menggantinya.
- **Mengira perlu props.** `useContext` membaca langsung dari Provider.
- **Menaruh Provider di tempat yang salah.** Hanya komponen di dalam Provider yang mendapat nilainya.""",
        "speak": """“Toolbar ada di dalam Provider dengan value dark, jadi useContext mengembalikan dark. Light hanya default kalau tidak ada Provider.”""",
    },
    {
        "id": "react-05-import-export",
        "day": 3,
        "topic": "React",
        "title": "Latihan: default vs named import",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### Default dan named export bisa digabung

```js
// math.js
export const add = (a, b) => a + b;
export default function multiply(a, b) { return a * b; }
```

```js
// app.js
import multiply, { add } from './math.js';
```

Default import tidak memakai kurung kurawal dan namanya bebas. Named import memakai kurung kurawal dan namanya harus cocok (atau memakai `as`).

**Analogi:** default export seperti satu pintu utama dengan nama bebas; named export seperti loker berlabel yang namanya harus cocok.
""",
        "prompt": """Apa output dari kode berikut?

```js
// math.js
export const add = (a, b) => a + b;
export default function multiply(a, b) {
  return a * b;
}

// app.js
import multiply, { add } from './math.js';
console.log(add(2, 3), multiply(2, 3));
```

- A. `5 6`
- B. `6 5`
- C. `5 5`
- D. SyntaxError""",
        "hints": [
            "`add(2, 3)` menjalankan named export `add`.",
            "`multiply(2, 3)` menjalankan default export.",
        ],
        "answer": """**Jawaban: A. `5 6`**

**Penjelasan:**

- `add(2, 3)` → `2 + 3 = 5`.
- `multiply(2, 3)` → `2 * 3 = 6`.
- Import `multiply, { add }` benar: `multiply` adalah default import, `add` adalah named import.

**Kalau salah import:**

```js
import { multiply, add } from './math.js';
```

Ini error karena `multiply` adalah default export, bukan named export.

**Ganti nama default import:**

```js
import kali, { add } from './math.js';
console.log(kali(2, 3)); // 6
```

Nama `kali` bebas karena default export tidak terikat nama.""",
        "traps": """- **Mengira default import butuh kurung kurawal.** Tidak; justru named import yang butuh.
- **Mengira nama default import harus sama dengan nama function.** Bisa diganti bebas.
- **Mengira named import bisa diganti tanpa `as`.** Harus memakai `as` jika ingin nama berbeda.""",
        "speak": """“Add adalah named export, multiply default export. Import-nya benar, jadi add 2 3 menghasilkan 5 dan multiply 2 3 menghasilkan 6. Output-nya 5 6.”""",
    },
    {
        "id": "react-06-fix-bugs",
        "day": 3,
        "topic": "React",
        "title": "Latihan: temukan dua bug React",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Aturan hooks dan key

Dua aturan penting:

1. **Hooks harus dipanggil di top-level.** Jangan panggil `useState`/`useEffect` di dalam `if`, loop, atau setelah early return.
2. **Setiap item dalam list butuh `key` yang stabil.** Key membantu React mengenali item mana yang berubah.

Melanggar aturan hooks bisa menyebabkan urutan hooks berubah antar-render dan error “Rendered more hooks than during the previous render”.

**Analogi:** hooks seperti urutan resep yang harus selalu sama; kalau satu langkah dilewati, adonan berikutnya kacau.
""",
        "prompt": """Komponen berikut punya dua masalah. Temukan dan perbaiki.

```jsx
function UserList({ users, loading }) {
  if (loading) {
    return <p>Loading...</p>;
  }

  const [selected, setSelected] = useState(null);

  return (
    <ul>
      {users.map(user => (
        <li onClick={() => setSelected(user.id)}>
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```""",
        "hints": [
            "Perhatikan posisi `useState` terhadap early return `if (loading)`.",
            "Perhatikan elemen `<li>` di dalam `map`. Apa yang kurang untuk membantu React membedakan item?",
        ],
        "answer": """**Bug 1 — hook setelah early return.**

`useState` dipanggil setelah `if (loading) return ...`. Saat `loading` berubah dari `true` ke `false`, jumlah hooks yang dipanggil berubah, sehingga urutan hooks tidak konsisten. React bisa melempar error.

**Bug 2 — `key` hilang pada list.**

Setiap `<li>` di dalam `map` harus punya `key` yang stabil, biasanya `user.id`.

**Perbaikan:**

```jsx
function UserList({ users, loading }) {
  const [selected, setSelected] = useState(null);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <ul>
      {users.map(user => (
        <li key={user.id} onClick={() => setSelected(user.id)}>
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```

**Kenapa `key` penting:** React memakai key untuk mencocokkan elemen lama dan baru. Tanpa key, React memakai index dan bisa salah mempertahankan state saat urutan berubah.

**Catatan:** `selected` belum ditampilkan, tetapi state-nya sekarang aman karena hook selalu dipanggil sebelum early return.""",
        "traps": """- **Menaruh hooks di dalam kondisi.** Selalu panggil hooks di top-level sebelum return apa pun.
- **Memakai index sebagai key untuk list yang bisa berubah urutan.** Gunakan ID stabil.
- **Mengira `key` bisa dibaca sebagai props.** `key` bukan props biasa; kalau butuh nilainya, kirim props terpisah.""",
        "speak": """“Ada dua bug. Pertama, useState dipanggil setelah early return, itu melanggar aturan hooks; kedua, item list tidak punya key. Saya pindahkan useState ke atas dan menambahkan key user.id.”""",
    },
    {
        "id": "live-01-fizzbuzz",
        "day": 3,
        "topic": "Live Coding",
        "title": "Live coding: FizzBuzz",
        "kind": "code",
        "origin": "latihan",
        "points": 10,
        "concept": """### Loop + kondisi berurutan

FizzBuzz melatih tiga hal: loop, modulus (`%`), dan urutan pengecekan kondisi.

Aturan:

- Kelipatan 3 → `Fizz`
- Kelipatan 5 → `Buzz`
- Kelipatan 15 → `FizzBuzz`
- Lainnya → angka

Cek kelipatan 15 **lebih dulu**, karena 15 juga kelipatan 3 dan 5.

**Analogi:** seperti memeriksa antrean angka dengan tiga saringan; saringan 15 harus diperiksa lebih dulu agar tidak tertangkap saringan 3 atau 5.
""",
        "prompt": """Buat fungsi JavaScript `fizzBuzz(n)` yang mengembalikan array hasil FizzBuzz dari 1 sampai `n`.

Contoh:

```js
fizzBuzz(5) // [1, 2, 'Fizz', 4, 'Buzz']
fizzBuzz(15) // [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz']
```""",
        "hints": [
            "Loop dari 1 sampai n. Siapkan array kosong untuk hasil.",
            "Cek `i % 15 === 0` sebelum `i % 3 === 0` dan `i % 5 === 0`.",
        ],
        "answer": """**Solusi:**

```js
function fizzBuzz(n) {
  const result = [];

  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) {
      result.push('FizzBuzz');
    } else if (i % 3 === 0) {
      result.push('Fizz');
    } else if (i % 5 === 0) {
      result.push('Buzz');
    } else {
      result.push(i);
    }
  }

  return result;
}
```

**Verifikasi:**

```js
console.log(fizzBuzz(5));
// [1, 2, 'Fizz', 4, 'Buzz']

console.log(fizzBuzz(15));
// [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz']
```

**Kompleksitas:** O(n) waktu, O(n) ruang karena menyimpan hasil.

**Alternatif:** kalau interviewer meminta print langsung, ganti `result.push(...)` dengan `console.log(...)` dan tidak perlu return array.""",
        "traps": """- **Cek kelipatan 3 dulu.** Angka 15 akan menjadi `Fizz`, bukan `FizzBuzz`.
- **Loop mulai dari 0.** FizzBuzz biasanya mulai dari 1.
- **Lupa `return`.** Fungsi mengembalikan `undefined`.
- **Menggunakan `=` bukan `===`.** Satu tanda sama dengan adalah assignment, bukan perbandingan. Gunakan `===` untuk membandingkan.""",
        "speak": """“Saya akan loop dari 1 sampai n. Di setiap angka, saya cek kelipatan 15 dulu supaya FizzBuzz tidak tertelan Fizz, lalu cek kelipatan 3 dan 5; kalau bukan apa-apa, masukkan angkanya. Saya simpan ke array dan return, kompleksitasnya O(n).”""",
    },
    {
        "id": "live-02-reverse-string",
        "day": 3,
        "topic": "Live Coding",
        "title": "Live coding: balik string",
        "kind": "code",
        "origin": "latihan",
        "points": 10,
        "concept": """### String adalah urutan karakter

Di JavaScript, string bisa dipecah menjadi array karakter, dibalik, lalu digabung lagi:

```js
'hello'.split('').reverse().join('') // 'olleh'
```

Untuk karakter Unicode seperti emoji, `split('')` bisa memecah code unit yang salah. `Array.from(str)` lebih aman untuk banyak kasus karena bekerja per code point.

**Analogi:** seperti membalik antrean orang; orang terakhir menjadi yang pertama, dan seterusnya.
""",
        "prompt": """Buat fungsi `reverseString(str)` yang mengembalikan string terbalik.

Contoh:

```js
reverseString('hello') // 'olleh'
reverseString('abc')   // 'cba'
reverseString('')      // ''
```""",
        "hints": [
            "Coba pendekatan built-in: `split`, `reverse`, `join`.",
            "Kalau ingin manual, loop dari karakter terakhir ke indeks 0 dan tempelkan ke string hasil.",
        ],
        "answer": """**Solusi built-in:**

```js
function reverseString(str) {
  return Array.from(str).reverse().join('');
}
```

**Solusi manual (lebih menunjukkan logika):**

```js
function reverseString(str) {
  let result = '';
  for (let i = str.length - 1; i >= 0; i--) {
    result += str[i];
  }
  return result;
}
```

**Verifikasi:**

```js
console.log(reverseString('hello')); // 'olleh'
console.log(reverseString('abc'));   // 'cba'
console.log(reverseString(''));      // ''
```

**Kompleksitas:** O(n) waktu, O(n) ruang untuk hasil.

**Catatan Unicode:** `Array.from('😀')` menghasilkan satu elemen untuk emoji sederhana. Untuk gabungan emoji seperti keluarga atau bendera, dibutuhkan `Intl.Segmenter` karena satu grapheme bisa terdiri dari beberapa code point. Untuk interview pemula, sebutkan batasan ini sebagai nilai tambah.""",
        "traps": """- **Lupa `join('')`.** Hasil `reverse()` masih array.
- **Mengira `split('')` selalu aman untuk emoji.** Bisa memecah surrogate pair.
- **Loop salah arah.** Mulai dari `str.length - 1`, bukan `str.length`.
- **Mengubah string asli.** String immutable; fungsi mengembalikan string baru.""",
        "speak": """“Saya bisa memakai Array.from untuk memecah string per karakter, reverse, lalu join. Kalau manual, saya loop dari indeks terakhir sampai nol dan menempelkan setiap karakter. Keduanya O(n).”""",
    },
    {
        "id": "live-03-count-items",
        "day": 3,
        "topic": "Live Coding",
        "title": "Live coding: hitung kemunculan item",
        "kind": "code",
        "origin": "latihan",
        "points": 10,
        "concept": """### Frequency map

Untuk menghitung berapa kali setiap item muncul, gunakan **map/dictionary**:

```js
counts[item] = (counts[item] || 0) + 1;
```

Di JavaScript, `Map` lebih aman daripada object biasa karena key seperti `__proto__` tidak bentrok dengan prototype object.

**Analogi:** seperti menghitung suara di kotak suara; setiap item yang muncul menambah satu tally pada namanya.
""",
        "prompt": """Buat fungsi `countItems(items)` yang mengembalikan object berisi jumlah kemunculan setiap item.

Contoh:

```js
countItems(['a', 'b', 'a']) // { a: 2, b: 1 }
countItems([1, 1, 1, 2])    // { 1: 3, 2: 1 }
```

Kalau yang dimaksud “hitung item” adalah jumlah total elemen, jelaskan bahwa itu cukup `items.length`.""",
        "hints": [
            "Siapkan `Map` atau object kosong untuk menyimpan hitungan.",
            "Untuk setiap item, ambil hitungan sebelumnya (default 0), tambah 1, lalu simpan kembali.",
        ],
        "answer": """**Solusi dengan `Map`:**

```js
function countItems(items) {
  const counts = new Map();

  for (const item of items) {
    counts.set(item, (counts.get(item) || 0) + 1);
  }

  return Object.fromEntries(counts);
}
```

**Verifikasi:**

```js
console.log(countItems(['a', 'b', 'a'])); // { a: 2, b: 1 }
console.log(countItems([1, 1, 1, 2]));    // { '1': 3, '2': 1 }
console.log(countItems([]));              // {}
```

**Solusi object biasa:**

```js
function countItems(items) {
  const counts = {};
  for (const item of items) {
    counts[item] = (counts[item] || 0) + 1;
  }
  return counts;
}
```

**Catatan:** object biasa mengubah key menjadi string, dan key seperti `__proto__` bisa bermasalah. `Map` lebih aman untuk data yang tidak dikenal.

**Kalau maksudnya total elemen:**

```js
function countTotal(items) {
  return items.length;
}
```

**Kompleksitas:** O(n) waktu, O(k) ruang dengan k = jumlah item unik.""",
        "traps": """- **Lupa default 0.** `undefined + 1` menghasilkan `NaN`.
- **Mengira object key selalu angka.** Key object menjadi string.
- **Menggunakan `for...in` untuk array.** Gunakan `for...of` atau `forEach`.
- **Tidak mengklarifikasi requirement.** “Hitung item” bisa berarti total atau frekuensi; tanyakan dulu.""",
        "speak": """“Saya asumsikan yang diminta adalah frekuensi tiap item. Saya siapkan Map, loop setiap item, ambil hitungan sebelumnya atau nol, lalu tambah satu; setelah selesai saya ubah ke object. Kalau yang diminta total, cukup items.length.”""",
    },
    {
        "id": "live-04-max-number",
        "day": 3,
        "topic": "Live Coding",
        "title": "Live coding: cari angka terbesar",
        "kind": "code",
        "origin": "latihan",
        "points": 10,
        "concept": """### Linear scan

Untuk mencari nilai terbesar, anggap elemen pertama sebagai kandidat, lalu bandingkan dengan elemen berikutnya. Kalau ada yang lebih besar, ganti kandidat.

Ini O(n): setiap elemen dilihat sekali. Tidak perlu sorting O(n log n) kalau hanya butuh nilai terbesar.

**Analogi:** seperti menjaga rekor lari; kamu cukup mengingat juara sementara, lalu membandingkannya dengan setiap pelari baru.
""",
        "prompt": """Buat fungsi `findMax(numbers)` yang mengembalikan angka terbesar dari array.

Contoh:

```js
findMax([3, 9, 2]) // 9
findMax([-5, -2, -10]) // -2
findMax([]) // null
```""",
        "hints": [
            "Tangani array kosong terlebih dahulu.",
            "Mulai dari `numbers[0]`, lalu loop dari indeks 1.",
        ],
        "answer": """**Solusi:**

```js
function findMax(numbers) {
  if (!Array.isArray(numbers) || numbers.length === 0) {
    return null;
  }

  let max = numbers[0];

  for (let i = 1; i < numbers.length; i++) {
    if (numbers[i] > max) {
      max = numbers[i];
    }
  }

  return max;
}
```

**Verifikasi:**

```js
console.log(findMax([3, 9, 2]));       // 9
console.log(findMax([-5, -2, -10]));   // -2
console.log(findMax([]));              // null
console.log(findMax([7]));             // 7
```

**Alternatif:**

```js
Math.max(...numbers)
```

Untuk array kosong, `Math.max(...[])` menghasilkan `-Infinity`, jadi tetap perlu guard. Untuk array sangat besar, spread bisa melebihi batas argumen fungsi; loop lebih aman.

**Kompleksitas:** O(n) waktu, O(1) ruang tambahan.""",
        "traps": """- **Mulai `max = 0`.** Untuk array berisi angka negatif, hasilnya salah.
- **Lupa array kosong.** `numbers[0]` menjadi `undefined`.
- **Memakai sorting.** `sort` O(n log n) dan mengubah array asli kalau tidak disalin.
- **Membandingkan string angka.** `'10' < '9'` bisa mengejutkan; pastikan tipe number.""",
        "speak": """“Saya cek array kosong dulu dan return null. Lalu saya anggap elemen pertama sebagai max, loop dari indeks satu, dan ganti max kalau ada yang lebih besar. Ini O(n) dan tidak perlu sorting.”""",
    },
    {
        "id": "live-05-react-counter",
        "day": 3,
        "topic": "Live Coding",
        "title": "Live coding: counter React",
        "kind": "code",
        "origin": "latihan",
        "points": 10,
        "concept": """### State + event handler

Counter adalah latihan paling dasar untuk `useState`:

- state menyimpan angka;
- tombol memanggil setter;
- React merender ulang saat state berubah.

Gunakan functional update `setCount(c => c + 1)` agar aman saat update bergantung pada nilai sebelumnya.

**Analogi:** seperti penghitung putaran di pintu masuk; setiap klik menambah satu, dan papan digital langsung menampilkan angka terbaru.
""",
        "prompt": """Buat komponen React `Counter` dengan:

- menampilkan angka saat ini;
- tombol `+1`;
- tombol `-1`;
- tombol `Reset` yang mengembalikan ke 0.""",
        "hints": [
            "Gunakan `const [count, setCount] = useState(0)`.",
            "Untuk `+1`, gunakan `setCount(c => c + 1)`. Untuk reset, `setCount(0)`.",
        ],
        "answer": """**Solusi:**

```jsx
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <button onClick={() => setCount(c => c - 1)}>-1</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

**Penjelasan:**

- `useState(0)` membuat state awal 0.
- `setCount(c => c + 1)` memakai nilai terbaru, aman untuk klik cepat atau update beruntun.
- `setCount(0)` mereset.
- Setiap perubahan state memicu render ulang, dan `{count}` menampilkan nilai baru.

**Pengembangan interview:** kalau diminta menyimpan riwayat, gunakan state array. Kalau diminta batas minimum 0, tambahkan guard `Math.max(0, c - 1)`.""",
        "traps": """- **Langsung mengubah `count++`.** State harus diubah lewat setter.
- **Memakai `setCount(count + 1)` di beberapa tempat sekaligus.** Bisa stale; gunakan functional update.
- **Lupa `import { useState } from 'react'`.**
- **Menaruh `useState` di dalam kondisi.** Hooks harus top-level.""",
        "speak": """“Saya buat state count dengan useState nol. Tombol plus memanggil setCount dengan functional update, minus sebaliknya, dan reset mengisi nol. Setiap perubahan otomatis merender ulang.”""",
    },
    {
        "id": "live-06-react-fetch",
        "day": 3,
        "topic": "Live Coding",
        "title": "Live coding: komponen React fetch data",
        "kind": "code",
        "origin": "latihan",
        "points": 15,
        "concept": """### `useEffect` untuk fetch

Pola fetch yang baik:

1. Siapkan state `data`, `loading`, `error`.
2. Jalankan fetch di `useEffect` dengan dependency `[]`.
3. Cek `response.ok` sebelum `json()`.
4. Batalkan request saat komponen unmount dengan `AbortController`.
5. Tampilkan loading/error, lalu data.

Tanpa cleanup, response dari request lama bisa menimpa state komponen yang sudah tidak ada.

**Analogi:** seperti memesan makanan lewat kurir; kamu menampilkan status “loading”, menangani gagal, dan membatalkan pesanan kalau sudah tidak dibutuhkan.
""",
        "prompt": """Buat komponen React `UserList` yang:

- fetch data dari `GET /api/users` saat pertama kali mount;
- menampilkan “Loading...” saat proses;
- menampilkan pesan error kalau gagal;
- menampilkan daftar nama user kalau berhasil;
- membersihkan request saat komponen di-unmount.""",
        "hints": [
            "Gunakan tiga state: `users`, `loading`, `error`.",
            "Di `useEffect`, buat `AbortController`, fetch dengan `signal`, dan return `() => controller.abort()`.",
        ],
        "answer": """**Solusi:**

```jsx
import { useEffect, useState } from 'react';

export default function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadUsers() {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch('/api/users', {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        setUsers(data);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    loadUsers();

    return () => controller.abort();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

**Kenapa `[]`:** fetch hanya sekali saat mount. Kalau dependency berisi state yang berubah, bisa terjadi fetch berulang tanpa henti.

**Kenapa `AbortController`:** saat komponen hilang sebelum request selesai, request dibatalkan dan tidak mencoba set state pada komponen yang sudah unmount.

**Kenapa `response.ok`:** `fetch` tidak melempar error untuk status 404/500; harus dicek manual.

**Pengembangan:** kalau butuh refetch saat tombol diklik, tambahkan state `reload` dan masukkan ke dependency array.""",
        "traps": """- **Lupa dependency `[]`.** Effect jalan setiap render dan bisa memicu loop.
- **Langsung `setUsers(data)` tanpa cek `response.ok`.** Data error ikut diproses.
- **Lupa cleanup.** Request lama bisa menimpa state baru.
- **Menaruh `useEffect` setelah early return.** Hooks harus selalu dipanggil di top-level.
- **Memakai `async` langsung sebagai callback useEffect.** Callback useEffect tidak boleh mengembalikan Promise; buat fungsi async di dalam lalu panggil.""",
        "speak": """“Saya siapkan state users, loading, dan error. Di useEffect dengan dependency kosong, saya buat AbortController, fetch, cek response.ok, lalu simpan data; kalau error dan bukan abort, saya simpan pesannya, dan cleanup membatalkan request. Setelah itu render loading, error, atau list dengan key.”""",
    },
    {
        "id": "live-07-spring-crud",
        "day": 3,
        "topic": "Live Coding",
        "title": "Live coding: endpoint Spring Boot CRUD",
        "kind": "code",
        "origin": "latihan",
        "points": 25,
        "concept": """### REST controller + service + DTO

CRUD sederhana biasanya terdiri dari:

- **DTO request** untuk data masuk dan validasi.
- **Entity/model** untuk data yang disimpan.
- **Service** untuk logika dan penyimpanan.
- **Controller** untuk endpoint HTTP.
- **Exception** untuk 404 yang jelas.

Di Spring Boot, controller tidak sebaiknya menyimpan data sendiri. Pisahkan service agar mudah diuji dan dikembangkan.

Di Laravel, ini mirip `Route::apiResource`, `Controller`, `FormRequest`, dan `Model`.

**Analogi:** seperti membuka cabang restoran dengan menu dan prosedur yang sama; controller adalah kasir, service adalah dapur, dan repository adalah gudang.
""",
        "prompt": """Buat endpoint CRUD sederhana untuk Employee:

```text
GET    /api/employees       → list
GET    /api/employees/{id}  → detail
POST   /api/employees       → create (201)
PUT    /api/employees/{id}  → update
DELETE /api/employees/{id}  → delete (204)
```

Field: `name`, `role`, `salary`. Gunakan in-memory storage agar fokus pada struktur Spring Boot.""",
        "hints": [
            "Buat `EmployeeRequest` sebagai record dengan validasi, `Employee` sebagai data yang dikembalikan.",
            "Gunakan `@RestController` dan mapping HTTP; untuk id yang tidak ada, lempar exception dengan `@ResponseStatus(HttpStatus.NOT_FOUND)`.",
        ],
        "answer": """**1. DTO dan model:**

```java
// Employee.java
public record Employee(Long id, String name, String role, double salary) {}

// EmployeeRequest.java
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.PositiveOrZero;

public record EmployeeRequest(
    @NotBlank String name,
    @NotBlank String role,
    @PositiveOrZero double salary
) {}
```

**2. Exception 404:**

```java
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class EmployeeNotFoundException extends RuntimeException {
    public EmployeeNotFoundException(Long id) {
        super("Employee " + id + " not found");
    }
}
```

**3. Service:**

```java
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class EmployeeService {
    private final Map<Long, Employee> db = new ConcurrentHashMap<>();
    private final AtomicLong sequence = new AtomicLong();

    public List<Employee> findAll() {
        return List.copyOf(db.values());
    }

    public Employee findById(Long id) {
        Employee employee = db.get(id);
        if (employee == null) {
            throw new EmployeeNotFoundException(id);
        }
        return employee;
    }

    public Employee create(EmployeeRequest request) {
        long id = sequence.incrementAndGet();
        Employee employee = new Employee(id, request.name(), request.role(), request.salary());
        db.put(id, employee);
        return employee;
    }

    public Employee update(Long id, EmployeeRequest request) {
        findById(id);
        Employee employee = new Employee(id, request.name(), request.role(), request.salary());
        db.put(id, employee);
        return employee;
    }

    public void delete(Long id) {
        findById(id);
        db.remove(id);
    }
}
```

**4. Controller:**

```java
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/employees")
public class EmployeeController {
    private final EmployeeService service;

    public EmployeeController(EmployeeService service) {
        this.service = service;
    }

    @GetMapping
    public List<Employee> findAll() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public Employee findById(@PathVariable Long id) {
        return service.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Employee create(@Valid @RequestBody EmployeeRequest request) {
        return service.create(request);
    }

    @PutMapping("/{id}")
    public Employee update(@PathVariable Long id,
                           @Valid @RequestBody EmployeeRequest request) {
        return service.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        service.delete(id);
    }
}
```

**Contoh test dengan curl:**

```bash
curl -X POST http://localhost:8080/api/employees \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada","role":"Backend","salary":8000000}'

curl http://localhost:8080/api/employees
curl http://localhost:8080/api/employees/1
```

**Yang dinilai interviewer:**

- Struktur controller/service terpisah.
- Status code benar: 201 untuk create, 204 untuk delete, 404 untuk id tidak ada.
- Validasi input.
- Constructor injection, bukan `new EmployeeService()`.
- Tidak menyimpan state di controller.""",
        "traps": """- **Lupa `@RequestBody`.** JSON tidak dipetakan ke record.
- **Lupa `@PathVariable`.** Id tidak terbaca dari URL.
- **Mengembalikan 200 untuk create.** Gunakan 201.
- **Mengembalikan 200 untuk delete.** Gunakan 204.
- **Melempar exception biasa tanpa status.** Client mendapat 500, bukan 404.
- **Menyimpan data di controller.** Sulit diuji dan tidak thread-safe.
- **Lupa `@Valid`.** Annotation validasi di record tidak dijalankan.""",
        "speak": """“Saya mulai dari kontrak endpoint dan DTO. Controller hanya menerima request dan memanggil service; service menyimpan data di map dan melempar exception 404 kalau id tidak ada. Saya pakai constructor injection, validasi dengan @Valid, dan status code yang benar: 201 untuk create, 204 untuk delete, lalu test dengan curl.”""",
    },
    {
        "id": "oral-01-dependency-injection",
        "day": 3,
        "topic": "Interview Lisan",
        "title": "Apa itu dependency injection?",
        "kind": "oral",
        "origin": "latihan",
        "points": 5,
        "concept": """### Dependency injection (DI)

Dependency adalah object lain yang dibutuhkan sebuah class. Injection berarti object itu **diberikan dari luar**, bukan dibuat sendiri di dalam class.

Tanpa DI:

```java
class OrderService {
    private final PaymentService payment = new PaymentService();
}
```

Dengan DI:

```java
class OrderService {
    private final PaymentService payment;

    OrderService(PaymentService payment) {
        this.payment = payment;
    }
}
```

Manfaat: loose coupling, mudah diganti/mock saat test, dan tanggung jawab class lebih jelas.

**Analogi:** seperti memesan alat tulis ke bagian gudang; kamu tidak membuat sendiri, cukup menerima barang yang sudah disiapkan.
""",
        "prompt": """Jelaskan apa itu dependency injection dan kenapa penting. Kaitkan dengan pengalaman Laravel/Spring Boot kamu.""",
        "hints": [
            "Mulai dari masalah: class yang membuat sendiri dependency-nya jadi sulit diuji dan sulit diganti.",
            "Sebutkan constructor injection dan peran container.",
        ],
        "answer": """**Jawaban singkat:**

“Dependency injection adalah pola di mana sebuah class menerima dependency-nya dari luar, bukan membuatnya sendiri. Misalnya `OrderService` tidak membuat `PaymentService` baru, tetapi menerimanya lewat constructor. Di Laravel, container mengisi constructor type-hint; di Spring Boot, `@Autowired` atau constructor injection melakukan hal yang sama. Keuntungannya class jadi loosely coupled, mudah diuji dengan mock, dan implementasi bisa diganti tanpa mengubah class pemakai.”

**Contoh Spring:**

```java
@Service
public class OrderService {
    private final PaymentService payment;

    public OrderService(PaymentService payment) {
        this.payment = payment;
    }
}
```

**Jembatan Laravel:**

```php
class OrderService {
    public function __construct(private PaymentService $payment) {}
}
```

Laravel service container otomatis mengirim `PaymentService`; Spring container melakukan hal serupa.

**Follow-up yang mungkin:** “Apa bedanya constructor injection dan field injection?” Jawab: constructor membuat dependency wajib dan object selalu lengkap; field injection lebih ringkas tetapi sulit diuji dan dependency tidak terlihat.""",
        "traps": """- **Mengatakan DI sama dengan service container.** Container adalah alat yang menjalankan DI; DI adalah polanya.
- **Mengatakan DI hanya untuk Spring.** Laravel, NestJS, .NET, dan banyak framework memakai konsep yang sama.
- **Tidak menyebut manfaat testability.** Ini nilai jual utama DI.""",
        "speak": """“Dependency injection itu class menerima dependency dari luar, bukan membuat sendiri. Di Laravel container mengisi constructor type-hint; di Spring constructor injection melakukan hal yang sama. Jadi class lebih mudah diuji dan implementasinya bisa diganti.”""",
    },
    {
        "id": "oral-02-rest-vs-graphql",
        "day": 3,
        "topic": "Interview Lisan",
        "title": "Apa bedanya REST dan GraphQL?",
        "kind": "oral",
        "origin": "latihan",
        "points": 5,
        "concept": """### REST vs GraphQL

- **REST:** resource + HTTP method + banyak endpoint. Mudah di-cache, sederhana, populer.
- **GraphQL:** satu endpoint, client menentukan field, schema kuat. Fleksibel untuk data kompleks, tetapi server/caching lebih rumit.

Tidak ada pemenang mutlak; pilih berdasarkan kebutuhan.

**Analogi:** REST seperti memesan paket menu tetap; GraphQL seperti memesan à la carte—kamu menentukan sendiri item yang ingin diambil.
""",
        "prompt": """Jelaskan perbedaan REST dan GraphQL, lalu kapan kamu memilih salah satunya.""",
        "hints": [
            "Bandingkan bentuk endpoint, cara client meminta data, dan trade-off caching.",
            "Sebutkan over-fetching/under-fetching sebagai masalah yang GraphQL coba selesaikan.",
        ],
        "answer": """**Jawaban singkat:**

“REST memakai resource dan HTTP method, biasanya banyak endpoint seperti `GET /users` dan `GET /users/1/posts`. GraphQL biasanya satu endpoint, dan client mengirim query untuk memilih field yang dibutuhkan. REST lebih sederhana dan mudah di-cache; GraphQL lebih fleksibel untuk data yang berelasi dan banyak client, tetapi server, caching, dan otorisasi per field lebih kompleks. Untuk CRUD sederhana saya memilih REST; untuk data graph yang kompleks saya pertimbangkan GraphQL.”

**Follow-up:** “Apa itu over-fetching?” Jawab: server mengirim data lebih banyak dari yang dibutuhkan client. “Under-fetching?” Client harus memanggil beberapa endpoint untuk melengkapi data.

**Jangan menjawab:** “GraphQL selalu lebih cepat.” Itu tidak benar; GraphQL bisa lebih berat jika query tidak dibatasi.""",
        "traps": """- **Menganggap GraphQL menggantikan database.** Ia hanya lapisan API.
- **Menganggap REST sudah usang.** REST masih sangat umum dan sering lebih tepat.
- **Tidak menyebut trade-off.** Jawaban dewasa selalu menyebut konteks.""",
        "speak": """“REST itu resource-based dengan banyak endpoint dan mudah di-cache. GraphQL satu endpoint, client memilih field, jadi cocok untuk data kompleks, tapi lebih rumit di server dan caching. Untuk CRUD sederhana saya pilih REST.”""",
    },
    {
        "id": "oral-03-bean-vs-component",
        "day": 3,
        "topic": "Interview Lisan",
        "title": "Apa bedanya `@Bean` dan `@Component`?",
        "kind": "oral",
        "origin": "latihan",
        "points": 5,
        "concept": """### `@Component` vs `@Bean`

- `@Component` dipasang di **class**. Spring menemukannya lewat component scan, lalu membuat bean.
- `@Bean` dipasang di **method** dalam class `@Configuration`. Method itu sendiri yang membuat dan mengembalikan object.
- `@Service`, `@Repository`, `@Controller` adalah spesialisasi `@Component`.

`@Bean` berguna untuk class dari library pihak ketiga yang tidak bisa kamu beri `@Component`.

**Analogi:** `@Component` seperti staf yang melamar dan ditemukan lewat scan; `@Bean` seperti staf yang kamu rekrut lewat method khusus.
""",
        "prompt": """Jelaskan perbedaan `@Bean` dan `@Component`. Kapan memakai masing-masing?""",
        "hints": [
            "Bandingkan tempat annotation dipasang: class vs method.",
            "Pikirkan kasus class dari library yang tidak bisa kamu ubah.",
        ],
        "answer": """**Jawaban singkat:**

“`@Component` dipasang di class dan ditemukan lewat component scan; Spring yang membuat object-nya. `@Bean` dipasang di method dalam class `@Configuration`; method itu yang membuat dan mengembalikan object. Hasil akhirnya sama-sama bean. Saya memakai `@Component` untuk class milik sendiri, dan `@Bean` untuk class pihak ketiga atau object yang perlu konfigurasi khusus, misalnya `DataSource` atau `ObjectMapper`.”

**Contoh `@Component`:**

```java
@Component
public class EmailSender { }
```

**Contoh `@Bean`:**

```java
@Configuration
public class AppConfig {
    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper();
    }
}
```

**Follow-up:** “Apa itu `@Service`?” Jawab: spesialisasi `@Component` untuk lapisan service; secara teknis tetap bean.""",
        "traps": """- **Mengatakan `@Bean` dan `@Component` tidak ada hubungan.** Keduanya menghasilkan bean.
- **Memasang `@Bean` di class biasa tanpa `@Configuration`.** Bisa jalan dengan mode proxy tertentu, tetapi sebaiknya pakai `@Configuration`.
- **Mengira `@Component` bisa dipakai untuk class library tanpa modifikasi.** Tidak; gunakan `@Bean`.""",
        "speak": """“Component dipasang di class dan ditemukan lewat scan. Bean dipasang di method configuration dan method itu yang membuat object; keduanya menghasilkan bean. Saya pakai Component untuk class sendiri, Bean untuk library atau konfigurasi khusus.”""",
    },
    {
        "id": "oral-04-primary-vs-qualifier",
        "day": 3,
        "topic": "Interview Lisan",
        "title": "Apa bedanya `@Primary` dan `@Qualifier`?",
        "kind": "oral",
        "origin": "latihan",
        "points": 5,
        "concept": """### Dua cara menyelesaikan bean ambiguity

- `@Primary` → satu bean menjadi **default** ketika ada beberapa kandidat.
- `@Qualifier("nama")` → memilih **bean tertentu** di titik injection.
- Kalau keduanya ada, qualifier yang lebih spesifik biasanya menang.

Analogi: `@Primary` seperti kasir default; `@Qualifier` seperti meminta kasir bernama tertentu.""",
        "prompt": """Jelaskan perbedaan `@Primary` dan `@Qualifier`, serta kapan memakai masing-masing.""",
        "hints": [
            "Bandingkan level pemasangan: bean vs injection point.",
            "Sebutkan apa yang terjadi kalau ada dua kandidat tanpa keduanya.",
        ],
        "answer": """**Jawaban singkat:**

“Kalau ada beberapa bean dengan tipe sama, Spring bingung. `@Primary` menandai satu bean sebagai pilihan default, jadi injection by type memakai bean itu. `@Qualifier` dipasang di titik injection untuk memilih bean tertentu berdasarkan nama. Saya memakai `@Primary` kalau satu implementasi memang default aplikasi, dan `@Qualifier` kalau pilihan bergantung pada class yang membutuhkan.”

**Contoh:**

```java
@Bean
@Primary
public PaymentGateway stripeGateway() { ... }

@Bean
public PaymentGateway mockGateway() { ... }
```

```java
public CheckoutService(@Qualifier("mockGateway") PaymentGateway gateway) { ... }
```

**Follow-up:** “Kalau tidak ada keduanya?” Jawab: `NoUniqueBeanDefinitionException`.""",
        "traps": """- **Mengira `@Primary` dipasang di injection point.** Dipasang di bean.
- **Mengira `@Qualifier` dipasang di bean method untuk memilih.** Bisa memberi nama bean, tetapi pemilihan dilakukan di injection point.
- **Mengira qualifier selalu kalah.** Qualifier lebih spesifik daripada primary.""",
        "speak": """“Primary menandai bean default. Qualifier memilih bean tertentu di injection point. Kalau ada dua kandidat dan tidak ada keduanya, Spring melempar NoUniqueBeanDefinitionException.”""",
    },
    {
        "id": "oral-05-props-vs-state",
        "day": 3,
        "topic": "Interview Lisan",
        "title": "Apa bedanya props dan state?",
        "kind": "oral",
        "origin": "latihan",
        "points": 5,
        "concept": """### Props vs state

- **Props** dikirim dari parent, read-only bagi child.
- **State** dimiliki komponen, bisa berubah lewat setter, dan memicu render ulang.
- Kalau dua komponen perlu berbagi state, angkat state ke parent (**lifting state up**) atau gunakan Context.

Analogi: props seperti pesanan yang dikirim pelanggan; state seperti catatan internal kasir.""",
        "prompt": """Jelaskan perbedaan props dan state di React. Kapan memakai masing-masing?""",
        "hints": [
            "Siapa yang memiliki data? Siapa yang boleh mengubah?",
            "Apa yang terjadi saat state berubah?",
        ],
        "answer": """**Jawaban singkat:**

“Props adalah data yang dikirim parent ke child dan bersifat read-only. State adalah data internal komponen yang bisa berubah lewat setter dan memicu render ulang. Saya memakai props untuk konfigurasi atau data yang dimiliki parent, dan state untuk hal yang berubah karena interaksi, misalnya input atau counter. Kalau beberapa komponen perlu berbagi state, saya angkat state ke parent atau memakai Context.”

**Contoh:**

```jsx
function Card({ title }) {       // props
  return <h2>{title}</h2>;
}

function Counter() {
  const [count, setCount] = useState(0); // state
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Follow-up:** “Bolehkah child mengubah props?” Tidak; child memanggil callback dari parent, lalu parent mengubah state.""",
        "traps": """- **Mengatakan props bisa diubah child.** Tidak; props read-only.
- **Mengatakan state harus global.** State lokal lebih sederhana sampai benar-benar perlu dibagi.
- **Tidak menyebut render ulang.** Perubahan state memicu render; perubahan props juga memicu render child.""",
        "speak": """“Props itu data dari parent dan read-only. State itu data internal yang bisa berubah lewat setter dan memicu render ulang. Kalau perlu dibagi, saya lifting state up atau pakai Context.”""",
    },
    {
        "id": "oral-06-useeffect",
        "day": 3,
        "topic": "Interview Lisan",
        "title": "Jelaskan `useEffect` dan dependency array",
        "kind": "oral",
        "origin": "latihan",
        "points": 5,
        "concept": """### `useEffect`

`useEffect` menjalankan side effect setelah render. Dependency array menentukan kapan effect dijalankan:

- tanpa array → setiap render;
- `[]` → sekali setelah mount;
- `[dep]` → saat `dep` berubah.

Cleanup function mencegah timer, subscription, atau fetch bocor.

**Analogi:** seperti timer di dapur yang bisa diatur untuk sekali, setiap kali resep berubah, atau terus-menerus.
""",
        "prompt": """Jelaskan cara kerja `useEffect` dan dependency array. Beri contoh kapan memakai cleanup.""",
        "hints": [
            "Bedakan tiga bentuk dependency array.",
            "Sebutkan contoh side effect: fetch, timer, event listener.",
        ],
        "answer": """**Jawaban singkat:**

“`useEffect` dipakai untuk side effect setelah render, misalnya fetch, timer, atau event listener. Dependency array mengatur kapan effect jalan: tanpa array setiap render, array kosong sekali setelah mount, dan array berisi nilai hanya saat nilai itu berubah. Kalau effect membuat timer atau subscription, saya mengembalikan cleanup function untuk membatalkannya saat komponen unmount atau sebelum effect berikutnya.”

**Contoh:**

```jsx
useEffect(() => {
  const id = setInterval(() => console.log('tick'), 1000);
  return () => clearInterval(id);
}, []);
```

**Contoh fetch:**

```jsx
useEffect(() => {
  const controller = new AbortController();
  fetch('/api/users', { signal: controller.signal })
    .then(r => r.json())
    .then(setUsers)
    .catch(err => { if (err.name !== 'AbortError') setError(err); });
  return () => controller.abort();
}, []);
```

**Follow-up:** “Kenapa effect jalan dua kali di development?” Jawab: StrictMode sengaja mount-cleanup-mount untuk membantu menemukan cleanup yang salah.""",
        "traps": """- **Mengatakan `[]` berarti tidak pernah jalan.** Tetap jalan sekali.
- **Lupa cleanup.** Timer/fetch bisa bocor.
- **Memakai object/array baru sebagai dependency.** Referensinya berubah setiap render dan bisa memicu loop.
- **Menaruh `async` langsung di callback.** Callback tidak boleh mengembalikan Promise; buat fungsi async di dalam.""",
        "speak": """“useEffect untuk side effect setelah render. Dependency array kosong berarti sekali setelah mount, tanpa array setiap render, dan array berisi nilai berarti saat nilai berubah. Kalau ada timer atau fetch, saya return cleanup.”""",
    },
    {
        "id": "oral-07-var-let-const",
        "day": 3,
        "topic": "Interview Lisan",
        "title": "Apa bedanya `var`, `let`, dan `const`?",
        "kind": "oral",
        "origin": "latihan",
        "points": 5,
        "concept": """### `var` vs `let` vs `const`

- `var` → function scope, di-hoist dengan nilai `undefined`, bisa dideklarasikan ulang.
- `let` → block scope, di-hoist tetapi berada di TDZ, bisa diubah.
- `const` → block scope, tidak bisa di-assign ulang, tetapi isi object/array masih bisa dimutasi.

Saran modern: default `const`, gunakan `let` kalau perlu berubah, hindari `var`.

**Analogi:** seperti tiga jenis kotak: `var` bocor ke seluruh rumah, `let` hanya untuk satu ruangan, dan `const` adalah kotak yang tidak boleh diganti, tetapi isinya masih bisa ditukar.
""",
        "prompt": """Jelaskan perbedaan `var`, `let`, dan `const`. Kapan memakai masing-masing?""",
        "hints": [
            "Bandingkan scope, hoisting, dan reassignment.",
            "Ingat bahwa `const` tidak membuat object menjadi immutable.",
        ],
        "answer": """**Jawaban singkat:**

“`var` punya function scope, di-hoist dan diberi nilai undefined, serta bisa dideklarasikan ulang. `let` dan `const` punya block scope; keduanya di-hoist tetapi berada di Temporal Dead Zone sebelum deklarasi. `let` bisa diubah, sedangkan `const` tidak bisa di-assign ulang, meskipun isi object atau array-nya masih bisa diubah. Saya default memakai `const`, memakai `let` kalau nilainya perlu berubah, dan menghindari `var`.”

**Contoh:**

```js
var a = 1;   // function scope
let b = 2;   // block scope, bisa diubah
const c = 3; // block scope, tidak bisa di-assign ulang

const user = { name: 'Ada' };
user.name = 'Grace'; // boleh, object-nya tetap
// user = {};        // error, reassignment
```

**Follow-up:** “Apa itu TDZ?” Jawab: periode antara hoisting dan baris deklarasi `let`/`const` di mana variabel belum boleh diakses.""",
        "traps": """- **Mengatakan `const` membuat object immutable.** Yang tidak boleh adalah reassignment variable.
- **Mengatakan `let` tidak di-hoist.** Ia di-hoist, tetapi berada di TDZ.
- **Memakai `var` di loop dengan callback.** Bisa menyebabkan semua callback melihat nilai akhir.""",
        "speak": """“Var function scope dan di-hoist dengan undefined. Let dan const block scope dan ada TDZ; const tidak bisa di-assign ulang, tapi isi object masih bisa diubah. Saya default const, let kalau perlu berubah.”""",
    },
    {
        "id": "oral-08-npe",
        "day": 3,
        "topic": "Interview Lisan",
        "title": "Apa itu NullPointerException dan cara mencegahnya?",
        "kind": "oral",
        "origin": "latihan",
        "points": 5,
        "concept": """### NullPointerException (NPE)

NPE terjadi saat kode mencoba mengakses method/field dari reference yang `null`.

Pencegahan:

- validasi input dan beri nilai default;
- guard clause `if (x != null)`;
- `Objects.requireNonNull` untuk kontrak yang wajib;
- hindari mengembalikan `null` dari method; pertimbangkan `Optional`;
- inisialisasi collection menjadi kosong, bukan null;
- jangan mengandalkan `@Autowired` pada static field.

Di Laravel/PHP, padanannya error “Call to a member function on null”.

**Analogi:** seperti mengetuk pintu rumah yang alamatnya kosong; tidak ada yang bisa dibuka, jadi program berhenti dengan error.
""",
        "prompt": """Jelaskan apa itu NullPointerException, kapan terjadi, dan bagaimana cara mencegahnya.""",
        "hints": [
            "Mulai dari definisi: memanggil method/field pada reference null.",
            "Sebutkan minimal tiga strategi pencegahan.",
        ],
        "answer": """**Jawaban singkat:**

“NullPointerException terjadi saat kita memanggil method atau mengakses field dari reference yang null. Misalnya `user.getName()` padahal `user` null. Cara mencegahnya: validasi input di awal, gunakan guard clause atau `Objects.requireNonNull`, inisialisasi collection menjadi kosong, dan hindari mengembalikan null dari method; kalau perlu, gunakan Optional. Di Spring, saya juga menghindari `@Autowired` pada static field karena tidak di-inject. Di Laravel, error serupa muncul saat memanggil method pada null.”

**Contoh guard:**

```java
public String getCity(User user) {
    if (user == null || user.getAddress() == null) {
        return "Unknown";
    }
    return user.getAddress().getCity();
}
```

**Follow-up:** “Apa bedanya null dan string kosong?” Jawab: null berarti tidak ada object; string kosong adalah object String dengan panjang 0.""",
        "traps": """- **Mengatakan NPE hanya terjadi di Java.** Konsep null reference ada di banyak bahasa; namanya berbeda.
- **Mengatakan `Optional` harus dipakai di mana-mana.** Optional berguna untuk return type, bukan semua field/parameter.
- **Menangkap NPE lalu mengabaikannya.** Lebih baik mencegah penyebabnya.
- **Mengira `@Autowired` mengisi static field.** Tidak; ini penyebab NPE yang sering muncul di soal Spring.""",
        "speak": """“NPE terjadi saat memanggil method atau field pada reference null. Saya mencegahnya dengan validasi input, guard clause, nilai default, dan menghindari return null. Di Spring saya juga hindari autowired static field karena tidak di-inject.”""",
    },
]
