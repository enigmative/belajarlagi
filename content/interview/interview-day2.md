# Interview Day 2 — Spring Boot & JavaScript

Target hari ini: kamu bisa menjelaskan **dependency injection**, membaca konfigurasi Spring Boot sederhana, dan menjawab soal JavaScript modern. Hari ini adalah hari dengan materi terbanyak, jadi pakai timer.

## Jadwal 3 Jam

| Waktu | Materi |
|---|---|
| 60 menit | Spring Boot: bean, DI, @Primary, @Qualifier, static injection |
| 60 menit | JavaScript: scope, hoisting, destructuring, map/filter, undefined/null |
| 30 menit | GraphQL dan Quarkus: pengenalan logo, kegunaan, trade-off |
| 30 menit | Kerjakan soal inti dan latihan, lalu ucapkan jawaban |

## Bagian 1 — Spring Boot

### Apa itu Spring Boot?

Spring adalah framework Java untuk membangun aplikasi. Spring Boot adalah versi Spring yang lebih praktis: konfigurasi otomatis, server embed, dan dependency management.

Analogi: Spring adalah dapur lengkap dengan banyak alat. Spring Boot adalah dapur yang sudah ditata dan dinyalakan, jadi kamu bisa langsung memasak.

Hal yang paling sering ditanya di interview:

- **Bean** — object yang dibuat dan dikelola Spring.
- **Dependency injection** — Spring memberikan object yang dibutuhkan, bukan kamu membuatnya sendiri.
- **ApplicationContext** — container tempat semua bean hidup.
- **Annotation** — penanda agar Spring tahu apa yang harus dilakukan.

### Bean dan ApplicationContext

```java
@Component
public class EmailSender {
    public void send(String to) {
        System.out.println("Mengirim email ke " + to);
    }
}
```

`@Component` memberi tahu Spring: “buat object dari class ini dan simpan di container.”

Container bernama `ApplicationContext` menyimpan bean. Kalau kamu meminta sebuah bean, Spring mencarinya berdasarkan tipe atau nama.

```java
@Autowired
ApplicationContext context;

EmailSender sender = context.getBean(EmailSender.class);
```

Di Laravel, `ApplicationContext` mirip service container. `app()->make(EmailSender::class)` adalah padanannya.

### Dependency Injection

Tanpa DI:

```java
class OrderService {
    private final EmailSender sender = new EmailSender();
}
```

Dengan DI:

```java
@Service
public class OrderService {
    private final EmailSender sender;

    public OrderService(EmailSender sender) {
        this.sender = sender;
    }
}
```

Spring melihat constructor membutuhkan `EmailSender`, mencarinya di container, lalu mengirimkannya. Ini disebut **constructor injection** dan merupakan cara yang paling disarankan.

Kenapa lebih baik?

- Class tidak terikat pada implementasi tertentu.
- Mudah diganti dengan mock saat test.
- Dependency terlihat jelas di constructor.
- Object selalu dalam keadaan lengkap.

Di Laravel:

```php
class OrderService {
    public function __construct(private EmailSender $sender) {}
}
```

Laravel service container mengisi `$sender` secara otomatis. Konsepnya sama.

### Annotation Penting

| Annotation | Tempat | Fungsi |
|---|---|---|
| `@Component` | class | membuat bean umum |
| `@Service` | class | bean untuk logika bisnis |
| `@Repository` | class | bean untuk akses database |
| `@Controller` | class | controller MVC yang mengembalikan view |
| `@RestController` | class | controller REST yang mengembalikan JSON |
| `@Configuration` | class | kelas konfigurasi |
| `@Bean` | method | method yang membuat bean |
| `@Autowired` | constructor/field/setter | meminta dependency |
| `@Primary` | bean | menjadikan bean sebagai default |
| `@Qualifier("nama")` | injection point | memilih bean tertentu |
| `@Value("${...}")` | field/parameter | mengambil nilai konfigurasi |
| `@SpringBootApplication` | class utama | gabungan configuration + component scan + auto-configuration |

`@Service`, `@Repository`, dan `@Controller` adalah spesialisasi `@Component`. Secara teknis semuanya bean.

### `@Bean` vs `@Component`

```java
@Component
public class MyService { }
```

Spring menemukan class ini lewat **component scan**.

```java
@Configuration
public class AppConfig {
    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper();
    }
}
```

Spring memanggil method `objectMapper()` dan menyimpan hasilnya sebagai bean. Nama bean default adalah nama method, yaitu `objectMapper`.

Kapan memakai `@Bean`? Saat class berasal dari library pihak ketiga dan tidak bisa kamu beri `@Component`, atau saat object perlu konfigurasi khusus.

### Component Scan

`@SpringBootApplication` melakukan scan dari package class utama dan semua sub-package di bawahnya.

```text
com.example.app
├── Application.java
├── order
│   └── OrderService.java     ← discan
└── payment
    └── PaymentService.java   ← discan
```

Kalau `PaymentService` berada di `com.example.other`, ia **tidak** discan secara default. Solusinya: pindahkan ke bawah `com.example.app`, atau gunakan:

```java
@SpringBootApplication(scanBasePackages = {"com.example.app", "com.example.other"})
```

### Bean Ambiguity: `@Primary` dan `@Qualifier`

Kalau ada dua bean dengan tipe sama:

```java
@Bean
public GreetingService englishGreetingService() {
    return new EnglishGreetingService();
}

@Bean
public GreetingService spanishGreetingService() {
    return new SpanishGreetingService();
}
```

Lalu ada class yang meminta satu `GreetingService`, Spring bingung. Error-nya:

```text
NoUniqueBeanDefinitionException
expected single matching bean but found 2
```

Solusi:

1. **`@Primary`** pada salah satu bean → menjadi pilihan default.

```java
@Bean
@Primary
public GreetingService englishGreetingService() {
    return new EnglishGreetingService();
}
```

2. **`@Qualifier`** di titik injection → memilih bean berdasarkan nama.

```java
public Greeter(@Qualifier("spanishGreetingService") GreetingService service) {
    this.service = service;
}
```

3. **Nama bean** saat mengambil dari context.

```java
GreetingService service = context.getBean("englishGreetingService", GreetingService.class);
```

Analogi: ada dua kasir. `@Primary` adalah kasir default; `@Qualifier` adalah kamu meminta kasir bernama tertentu.

### Nama Bean

- `@Component` → nama class dengan huruf pertama kecil. `EnglishGreetingService` → `englishGreetingService`.
- `@Bean` → nama method. `englishGreetingService()` → `englishGreetingService`.
- Bisa diganti: `@Component("english")` atau `@Bean(name = "english")`.

Nama bean **case-sensitive**. `clock` dan `Clock` berbeda.

### static dan `@Autowired`

Spring mengelola **object bean**, bukan class. Field `static` milik class, sehingga tidak di-inject.

```java
@Component
public class Test {
    @Autowired
    static SimpleDateFormat formatter; // tetap null
}
```

Memanggil `formatter.getClass()` menghasilkan `NullPointerException`. Solusinya: jadikan field biasa dan inject lewat constructor.

### REST Controller

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }

    @GetMapping
    public List<User> findAll() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public User findById(@PathVariable Long id) {
        return service.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public User create(@Valid @RequestBody UserRequest request) {
        return service.create(request);
    }
}
```

Padanan Laravel:

```php
Route::get('/api/users', [UserController::class, 'index']);
Route::post('/api/users', [UserController::class, 'store']);
```

| Spring Boot | Laravel |
|---|---|
| `@RestController` | Controller |
| `@GetMapping` | `Route::get` |
| `@PostMapping` | `Route::post` |
| `@PathVariable` | parameter route `{id}` |
| `@RequestBody` | `$request->all()` / FormRequest |
| `@Valid` | FormRequest validation |
| `ResponseEntity` | `response()->json()` |

### Error Spring yang Sering Muncul

| Error | Penyebab umum | Solusi |
|---|---|---|
| `NoUniqueBeanDefinitionException` | dua bean tipe sama | `@Primary` atau `@Qualifier` |
| `NoSuchBeanDefinitionException` | bean tidak ditemukan | cek package scan, annotation, nama bean |
| `NullPointerException` saat startup | static field di-`@Autowired` | jadikan instance field |
| `Circular dependency` | dua bean saling membutuhkan | pecah tanggung jawab atau pakai setter/lazy |
| `BeanCreationException` | konfigurasi bean gagal | baca stack trace paling bawah |

## Bagian 2 — JavaScript

### `var`, `let`, dan `const`

```js
var a = 1;   // function scope, bisa dideklarasikan ulang
let b = 2;   // block scope, bisa diubah
const c = 3; // block scope, tidak bisa di-assign ulang
```

| Kata kunci | Scope | Reassignment | Hoisting |
|---|---|---|---|
| `var` | function | boleh | di-hoist, nilai `undefined` |
| `let` | block | boleh | di-hoist, tetapi TDZ |
| `const` | block | tidak boleh | di-hoist, tetapi TDZ |

**TDZ (Temporal Dead Zone)** adalah masa antara hoisting dan baris deklarasi, di mana `let`/`const` belum boleh diakses.

```js
console.log(x); // undefined
var x = 5;

console.log(y); // ReferenceError
let y = 10;
```

`const` tidak membuat object menjadi immutable:

```js
const user = { name: 'Ada' };
user.name = 'Grace'; // boleh
// user = {};        // error, reassignment
```

Saran: default `const`, pakai `let` kalau perlu berubah, hindari `var`.

### Destructuring

Array:

```js
const [first, second] = ['a', 'b'];
const [, , third] = ['a', 'b', 'c']; // third = 'c'
const [head, ...rest] = [1, 2, 3];   // head = 1, rest = [2, 3]
```

Object:

```js
const user = { name: 'Ada', role: 'dev' };
const { name, role } = user;
const { name: userName, age = 20 } = user;
```

`name: userName` berarti ambil property `name`, simpan ke variable `userName`. Default `age = 20` hanya dipakai kalau `age` bernilai `undefined`.

### `map`, `filter`, dan `reduce`

```js
const nums = [1, 2, 3, 4, 5];

const doubled = nums.map(n => n * 2);        // [2, 4, 6, 8, 10]
const even = nums.filter(n => n % 2 === 0);  // [2, 4]
const total = nums.reduce((sum, n) => sum + n, 0); // 15
```

- `map` mengubah setiap elemen, panjang array tetap.
- `filter` memilih elemen yang lolos, panjang bisa berkurang.
- `reduce` menggabungkan semua elemen menjadi satu nilai.

Keduanya mengembalikan array baru dan tidak mengubah array asli.

### `undefined` vs `null`

```js
let a;              // undefined
const b = null;     // null, sengaja dikosongkan

console.log(a === undefined); // true
console.log(b === undefined); // false
console.log(b == undefined);  // true (coercion)
console.log(typeof null);     // "object" (quirk JavaScript)
```

- `undefined` → belum diberi nilai.
- `null` → sengaja diberi nilai kosong.
- Gunakan `===` untuk perbandingan yang aman.

### Async dan Fetch

```js
async function loadUsers() {
  try {
    const response = await fetch('/api/users');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const users = await response.json();
    console.log(users);
  } catch (error) {
    console.error(error);
  }
}
```

Poin penting:

- `fetch` tidak melempar error untuk status 404/500; cek `response.ok`.
- `await` menunggu Promise selesai.
- `async` membuat function selalu mengembalikan Promise.
- Gunakan `try/catch` untuk menangani error.

## Bagian 3 — GraphQL dan Quarkus

### GraphQL

GraphQL adalah **query language untuk API**. Client mengirim query, server mengembalikan data dengan bentuk yang sama. Biasanya hanya ada satu endpoint, misalnya `/graphql`.

Istilah:

- **Schema** — kontrak tipe data.
- **Query** — permintaan baca.
- **Mutation** — permintaan ubah data.
- **Resolver** — fungsi yang mengambil data untuk sebuah field.

Kapan cocok:

- Data saling berelasi dan client butuh banyak relasi sekaligus.
- Ada beberapa client dengan kebutuhan field berbeda.
- Ingin mengurangi over-fetching dan under-fetching.

Trade-off:

- Server lebih kompleks: caching, query complexity, N+1 problem.
- Otorisasi per field perlu dipikirkan.
- Untuk CRUD sederhana, REST sering lebih mudah.

Logo GraphQL: polygon/hexagon berwarna pink.

### Quarkus

Quarkus adalah framework Java yang dirancang untuk **Kubernetes** dan **GraalVM**. Fokusnya startup cepat dan memori rendah.

Kelebihan:

- Startup cepat, terutama native image.
- Memori lebih rendah.
- Cocok untuk microservice, serverless, dan container.

Kekurangan:

- Ekosistem lebih kecil dari Spring Boot.
- Build native lebih lama.
- Tidak semua library kompatibel dengan GraalVM.

Logo Quarkus: kotak biru dengan kubus merah-hitam.

Jawaban jujur yang bagus: “Saya belum memakainya di produksi, tetapi saya paham kapan ia lebih cocok daripada Spring Boot.” Jangan mengklaim pengalaman yang tidak ada.

## Checklist Hari 2

- [ ] Menjelaskan bean dan ApplicationContext.
- [ ] Menjelaskan constructor injection.
- [ ] Menjelaskan `@Component` vs `@Bean`.
- [ ] Menjelaskan `@Primary` vs `@Qualifier`.
- [ ] Menjelaskan kenapa static field tidak di-inject.
- [ ] Menjelaskan component scan.
- [ ] Menjelaskan `var` vs `let` vs `const`.
- [ ] Menjelaskan hoisting dan TDZ.
- [ ] Menjelaskan array/object destructuring.
- [ ] Menjelaskan `map` vs `filter`.
- [ ] Menjelaskan `undefined` vs `null`.
- [ ] Menjelaskan GraphQL dan Quarkus beserta trade-off.
- [ ] Mengerjakan Soal 5–9 dan semua latihan Hari 2.

## Latihan di Bank Soal

- Soal inti Spring: [Dua bean, satu output Hello!](#/interview/core-05-spring-primary)
- Soal inti static: [Println mana yang NPE?](#/interview/core-06-static-autowired)
- Soal inti destructuring: [Output array destructuring](#/interview/core-07-array-destructuring)
- Soal inti GraphQL: [GraphQL dan kapan dipakai](#/interview/core-08-graphql)
- Soal inti Quarkus: [Quarkus dan kapan dipakai](#/interview/core-09-quarkus)

Latihan Spring:

- [Memilih bean dengan @Primary](#/interview/spring-01-primary)
- [@Qualifier memilih bean](#/interview/spring-02-qualifier)
- [Nama bean dari @Bean](#/interview/spring-03-bean-name)
- [Component scan](#/interview/spring-04-component-scan)
- [Qualifier pada field](#/interview/spring-05-field-qualifier)

Latihan JavaScript:

- [Object destructuring](#/interview/js-01-object-destructuring)
- [Array rest](#/interview/js-02-array-rest)
- [Scope var vs let](#/interview/js-03-scope)
- [Hoisting dan TDZ](#/interview/js-04-hoisting)
- [Chain map dan filter](#/interview/js-05-map-filter)
- [undefined vs null](#/interview/js-06-undefined-null)

Setelah Hari 2, lanjut ke [Hari 3 — React, Live Coding & Interview](#/lessons/interview-day3).
