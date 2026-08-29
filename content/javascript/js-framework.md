# Frontend Framework — Vue & React (Pilih Satu)

## Learning Objective

- Memahami mengapa perlu framework frontend
- React: komponen, state, props, hooks dasar
- Vue: SFC, reactive, directives
- Memilih satu dan fokus sampai bisa buat aplikasi
- Menghubungkan ke API (fetch + render)

---

## Theory

### Kenapa framework?

- Reusable component
- Reactive state (UI auto-update)
- SPA routing
- Ekosistem tooling (build, dev server)

### React (pilih jika ekosistem kamu condong ke sana)

```jsx
// komponen
function UserCard({ name, role }) {
    return (
        <div className="card">
            <h3>{name}</h3>
            <p>{role}</p>
        </div>
    );
}

// state + effect
function Counter() {
    const [count, setCount] = useState(0);
    useEffect(() => {
        console.log('count berubah:', count);
    }, [count]);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Vue (pilih jika pekerjaanmu dekat Laravel/bootcamp Vue)

```vue
<template>
    <div class="card">
        <h3>{{ name }}</h3>
        <p>{{ role }}</p>
        <button @click="count++">+</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps(['name', 'role']);
const count = ref(0);
</script>
```

---

## Analogy

Framework frontend = "kit konstruksi bangunan": balok (component) sudah terstandar, kamu tinggal menyusun. Tanpa framework, kamu manual mortar & bata (querySelector + innerHTML di tiap tempat) — cepat berantakan saat besar.

---

## Examples — fetch + render di React

```jsx
function Users() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetch('/api/users')
            .then(r => r.json())
            .then(setUsers);
    }, []);

    return (
        <ul>
            {users.map(u => <li key={u.id}>{u.name}</li>)}
        </ul>
    );
}
```

---

## Code — Vue ekivalen

```vue
<script setup>
import { ref, onMounted } from 'vue';

const users = ref([]);
onMounted(async () => {
    users.value = await (await fetch('/api/users')).json();
});
</script>

<template>
    <ul>
        <li v-for="u in users" :key="u.id">{{ u.name }}</li>
    </ul>
</template>
```

---

## Explanation

- **Satu saja**: jangan belajar React + Vue dua-duanya. Pilih satu lalu buat aplikasi utuh.
- React: state pakai `useState`, side-effect `useEffect`, props → data turun.
- Vue: `ref` reactive, `defineProps`, `@click` = event, `v-for` = render list.
- Keduanya membaca API yang sama (`fetch`) — konsep yang sama, sintaks beda.
- Feedback dari state → UI otomatis, kamu tidak menulis DOM manual.

---

## Common Mistakes

1. Belajar dua framework sekaligus.
2. Mutate state langsung (harus via setter/setter fungsi).
3. Lupa `key` di list → bug render / warning.
4. Effect menelan `fetch` baru tiap render (dependency array).
5. Menaruh seluruh state global di komponen acak (pakai store bila perlu).

---

## Manual Exercises

### Exercise 1
Komponen `HelloWorld({ name })` di framework pilihanmu.

### Exercise 2
Counter dengan state.

### Exercise 3
Fetch list users + render.

### Exercise 4
Todo app: input + list + hapus.

### Exercise 5
Routing (React Router / Vue Router) halaman Home & About.

---

## Challenge — Minimal Exercise

Buat komponen `UserList` di framework pilihanmu yang fetch `/api/users` dan menampilkan daftar nama.

---

## Reflection

1. Kenapa pakai framework bukan vanilla terus?
2. Apa itu state & props?
3. Apa peran `key` di list render?
4. Kapan memilih Vue vs React?
5. Bagaimana framework berhubungan dengan API backend?

---

## Checklist

- [ ] Bisa komponen + props
- [ ] Bisa state + event
- [ ] Bisa fetch + render
- [ ] Fokus SATU framework
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 5 (React)

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

<Routes>
    <Route path="/" element={<Home />} />
    <Route path="/about" element={<About />} />
</Routes>
```

</details>