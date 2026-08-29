# JavaScript — Fundamentals

## Learning Objective

- Memahami let/const, tipe data
- Array & Object + metode umum
- Function, Arrow Function, Template Literal
- Destructuring, Spread, Rest
- Kondisi & Loop

---

## Theory

### Variable & tipe

```javascript
let name = "John";        // bisa diubah
const age = 23;           // tidak boleh diubah (reassign)
let height = 170.5;
let isDev = true;
let nothing = null;

console.log(`Halo ${name}, umur ${age}`);   // template literal
```

### Array

```javascript
let nums = [1, 2, 3];
nums.push(4);                          // [1,2,3,4]
let doubled = nums.map(n => n * 2);    // [2,4,6,8]
let evens = nums.filter(n => n % 2 === 0);
let total = nums.reduce((acc, n) => acc + n, 0);
console.log(nums.includes(3));         // true
```

### Object

```javascript
const user = {
    name: "John",
    role: "admin",
    greet() {
        return `Halo ${this.name}`;
    },
};
console.log(user.name, user["role"]);
```

### Function

```javascript
function add(a, b) { return a + b; }
const addArrow = (a, b) => a + b;
const kubus = n => n ** 3;
```

### Destructuring, spread, rest

```javascript
const { name, role } = user;
const [x, y, ...rest] = [1, 2, 3, 4, 5];
const merged = { ...user, age: 23 };
function sumAll(...args) { return args.reduce((a, b) => a + b, 0); }
```

---

## Analogy

`let` vs `const` = "bisa ganti isi kotak" vs "kotak wajib tetap". Destructuring = "bongkar isi secara rapi sekaligus". Spread = "buka isi lalu salin". Rest = "kumpulkan sisanya jadi satu".

---

## Examples

```javascript
const employees = [
    { name: "John", salary: 8000000 },
    { name: "Budi", salary: 7000000 },
];

const totalGaji = employees.reduce((acc, e) => acc + e.salary, 0);
const nama = employees.map(e => e.name);
console.log(totalGaji, nama);   // 15000000 ["John","Budi"]
```

---

## Code

```javascript
function highestSalary(list) {
    return list.reduce((best, e) => (e.salary > best.salary ? e : best), list[0]);
}
console.log(highestSalary(employees).name);  // "John"
```

---

## Explanation

- JS otomatis dinamik (dynamic typing) seperti Python.
- Arrow function singkat; `const fn = () => {}`.
- Map/filter/reduce = versi JS dari transform list Python.
- Destructuring/spread/rest membuat kode rapi & immutable-friendly.

---

## Common Mistakes

1. Reassign `const`. Memakai `var` di kode baru.
2. Memakai `===` terus terang lebih aman (vs `==`).
3. Mutation tanpa salin: `const b = a` bukan copy array/object.
4. Lupa bahwa `reduce` butuh initial value.
5. Arrow function dan `this` (behavior beda).

---

## Manual Exercises

### Exercise 1
Array 1-10, buat array kuadrat via map.

### Exercise 2
Filter angka > 5.

### Exercise 3
Object `mkayak` dengan method `kali2()`.

### Exercise 4
Destructuring dari object user, tampilkan nama.

### Exercise 5
`sumAll(1,2,3,4)` hasil 10.

---

## Challenge — Minimal Exercise

Fungsi `solve(nums)` mengembalikan jumlah semua elemen dalam array memakai reduce.

---

## Reflection

1. Bedakan let/const.
2. Apa guna map/filter/reduce?
3. Kenapa spread dipakai saat menggandakan object?
4. Apa beda function biasa vs arrow?
5. Apa kegunaan rest parameter?

---

## Checklist

- [ ] Bisa let/const + tipe
- [ ] Bisa array & object
- [ ] Bisa arrow function + template literal
- [ ] Bisa destructuring/spread/rest
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```javascript
const kuadrat = [1,2,3,4,5,6,7,8,9,10].map(n => n * n);
```

Exercise 5

```javascript
const sumAll = (...args) => args.reduce((a, b) => a + b, 0);
console.log(sumAll(1,2,3,4));   // 10
```

</details>