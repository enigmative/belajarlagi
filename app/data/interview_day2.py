"""Bank soal Interview Prep — Hari 2 (Spring Boot, JavaScript, stack)."""

QUESTIONS_DAY2 = [
    {
        "id": "core-05-spring-primary",
        "day": 2,
        "topic": "Spring Boot",
        "title": "Dua bean, satu output: Hello!",
        "kind": "open",
        "origin": "asli",
        "points": 20,
        "concept": """### Bean dan dependency injection

**Bean** adalah object yang dibuat dan dikelola oleh Spring. Kamu tidak memanggil `new EnglishGreetingService()` sendiri; Spring yang menyiapkan object-nya lalu memberikannya ke class yang membutuhkan.

Analoginya: kamu tidak memasak sendiri di kantor, ada **kantin** (Spring container) yang menyiapkan makanan. Kamu tinggal bilang butuh apa lewat constructor.

Kalau ada dua bean dengan tipe yang sama, Spring bingung harus memberi yang mana. Itulah yang disebut **ambiguous dependency**. Ada dua cara memilih:

- `@Primary` → tandai satu bean sebagai pilihan default.
- `@Qualifier("namaBean")` → pilih bean tertentu di titik injection.

Di Laravel, ini mirip service container yang punya beberapa binding untuk interface yang sama; kamu perlu menentukan binding mana yang dipakai.""",
        "prompt": """Perhatikan kode berikut:

```java
public interface GreetingService {
    String greet();
}

public class EnglishGreetingService implements GreetingService {
    @Override
    public String greet() { return "Hello!"; }
}

public class SpanishGreetingService implements GreetingService {
    @Override
    public String greet() { return "¡Hola!"; }
}

@Configuration
public class GreetingConfiguration {
    @Bean
    public GreetingService englishGreetingService() {
        return new EnglishGreetingService();
    }

    @Bean
    public GreetingService spanishGreetingService() {
        return new SpanishGreetingService();
    }
}
```

Apa modifikasi yang diperlukan agar program yang meminta satu `GreetingService` menghasilkan `Hello!`?""",
        "hints": [
            "Ada dua bean dengan tipe `GreetingService`. Kalau kamu hanya meminta berdasarkan tipe, Spring tidak tahu harus memilih yang mana.",
            "Tandai bean Inggris dengan `@Primary`, atau pilih namanya di titik injection dengan `@Qualifier(\"englishGreetingService\")`.",
        ],
        "answer": """Ada **dua bean bertipe sama**, yaitu `englishGreetingService` dan `spanishGreetingService`. Kalau ada class lain yang melakukan injection seperti ini:

```java
@Service
public class Greeter {
    private final GreetingService greetingService;

    public Greeter(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    public void sayHello() {
        System.out.println(greetingService.greet());
    }
}
```

Spring akan melempar `NoUniqueBeanDefinitionException` karena ada dua kandidat. Ada beberapa perbaikan yang benar.

**Cara 1 — `@Primary` (pilihan default):**

```java
@Configuration
public class GreetingConfiguration {
    @Bean
    @Primary
    public GreetingService englishGreetingService() {
        return new EnglishGreetingService();
    }

    @Bean
    public GreetingService spanishGreetingService() {
        return new SpanishGreetingService();
    }
}
```

Sekarang `GreetingService` yang di-inject otomatis memakai bean Inggris, sehingga output-nya `Hello!`.

**Cara 2 — `@Qualifier` di titik injection:**

```java
@Service
public class Greeter {
    private final GreetingService greetingService;

    public Greeter(@Qualifier("englishGreetingService") GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    public void sayHello() {
        System.out.println(greetingService.greet());
    }
}
```

Output juga `Hello!`.

**Cara 3 — memilih bean berdasarkan nama:**

```java
GreetingService service = context.getBean("englishGreetingService", GreetingService.class);
System.out.println(service.greet()); // Hello!
```

**Cara 4 — menghapus salah satu bean.** Kalau bean Spanyol memang tidak dipakai, menghapusnya juga menghilangkan ambiguitas. Tapi kalau nanti dibutuhkan, `@Primary` atau `@Qualifier` lebih fleksibel.

**Nama bean default:** method `englishGreetingService()` menjadi nama bean `englishGreetingService`. Kalau kamu menulis `@Bean(name = "english")`, maka nama bean-nya berubah menjadi `english`.""",
        "traps": """- **Mengira `@Primary` bisa dipasang di dua bean.** Hanya satu yang boleh menjadi default; kalau dua, Spring tetap bingung.
- **Memasang `@Qualifier` di class yang salah.** Qualifier dipasang di titik injection (constructor/field), bukan di bean method, kecuali kamu memang memberi nama bean.
- **Mengira nama bean otomatis sama dengan nama class.** Untuk `@Bean`, nama default adalah nama method. Untuk `@Component`, nama default adalah nama class dengan huruf pertama kecil.
- **Mengira `@Qualifier` dan `@Primary` konflik.** Kalau keduanya ada, `@Qualifier` yang lebih spesifik biasanya menang.""",
        "speak": """“Di konfigurasi ada dua bean dengan tipe GreetingService, jadi injection by type akan ambigu. Saya bisa menandai bean Inggris dengan @Primary sebagai default, atau memakai @Qualifier englishGreetingService di constructor. Setelah itu output-nya Hello!”""",
    },
    {
        "id": "core-06-static-autowired",
        "day": 2,
        "topic": "Spring Boot",
        "title": "Println mana yang menyebabkan NullPointerException?",
        "kind": "mcq",
        "origin": "asli",
        "points": 10,
        "concept": """### `@Autowired` tidak mengisi static field

Spring melakukan dependency injection pada **object bean**, bukan pada class. Field `static` milik class, bukan milik object, sehingga Spring tidak mengisinya.

`InitializingBean.afterPropertiesSet()` adalah callback yang dipanggil **setelah** property injection selesai. Jadi pada saat method itu berjalan:

- `context` (non-static) sudah terisi.
- `formatter` (static) tetap `null`.
- Memanggil method pada `formatter` menghasilkan `NullPointerException`.

Di Laravel, ini mirip mengandalkan static property yang tidak pernah di-bind oleh service container.

**Analogi:** seperti menaruh papan nama di kursi kosong; namanya ada, tetapi tidak ada orang yang duduk di sana.
""",
        "prompt": """Perhatikan kode berikut:

```java
@Component
public class Test implements InitializingBean {
    @Autowired
    ApplicationContext context;

    @Autowired
    static SimpleDateFormat formatter;

    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println(context.containsBean("formatter") + " ");
        System.out.println(context.getBean("formatter").getClass());
        System.out.println(formatter.getClass());
        System.out.println(context.getClass());
    }
}

@Configuration
class TestConfig {
    @Bean
    public SimpleDateFormat formatter() {
        return new SimpleDateFormat();
    }
}
```

Println mana yang harus dihapus agar tidak terjadi `NullPointerException`?

- A. `formatter.getClass()`
- B. `context.containsBean("formatter")`
- C. `context.getBean("formatter").getClass()`
- D. `context.getClass()`""",
        "hints": [
            "Perhatikan kata `static` pada field `formatter`. Apakah Spring mengelola static field?",
            "`context` dan `formatter` sama-sama diberi `@Autowired`, tetapi hanya satu yang benar-benar diisi oleh Spring.",
        ],
        "answer": """**Jawaban: A. `formatter.getClass()`**

**Kenapa:**

- `context` adalah field biasa (instance field). Spring mengisinya dengan `ApplicationContext`.
- `formatter` adalah field `static`. Spring **tidak mendukung** `@Autowired` pada static field; field itu tetap `null`.
- Saat `formatter.getClass()` dipanggil, artinya memanggil method pada `null` → `NullPointerException`.

**Output baris lainnya (kurang lebih):**

```text
true
class java.text.SimpleDateFormat
class org.springframework.context.annotation.AnnotationConfigApplicationContext
```

- `context.containsBean("formatter")` → `true`, karena bean method bernama `formatter`.
- `context.getBean("formatter").getClass()` → `class java.text.SimpleDateFormat`.
- `context.getClass()` → class implementasi context, misalnya `AnnotationConfigApplicationContext`.

**Perbaikan yang benar:**

Jadikan `formatter` field biasa, lalu inject lewat constructor:

```java
@Component
public class Test implements InitializingBean {
    private final ApplicationContext context;
    private final SimpleDateFormat formatter;

    public Test(ApplicationContext context, SimpleDateFormat formatter) {
        this.context = context;
        this.formatter = formatter;
    }

    @Override
    public void afterPropertiesSet() {
        System.out.println(formatter.getClass());
    }
}
```

Atau, kalau memang butuh static, jangan bergantung pada `@Autowired`; ambil dari context secara eksplisit atau gunakan `@PostConstruct` untuk mengisi field non-static.

**Catatan produksi:** `SimpleDateFormat` tidak thread-safe. Di aplikasi nyata, gunakan `DateTimeFormatter` dari `java.time`.""",
        "traps": """- **Mengira `@Autowired` bekerja di semua field.** Spring mengabaikan static field (biasanya sambil memberi warning).
- **Mengira `afterPropertiesSet` berarti semua field sudah terisi.** Hanya field yang dikelola Spring dan bukan static.
- **Mengira `context.getBean("formatter")` error.** Bean-nya ada; yang error adalah pemanggilan pada field static yang null.
- **Mengira `context` null karena `@Autowired` field.** Field non-static ini tetap di-inject oleh Spring.""",
        "speak": """“Yang error adalah formatter.getClass, karena formatter static dan Spring tidak meng-inject static field. Context-nya terisi, dan bean formatter juga ada di container, jadi tiga println lainnya aman. Solusinya jadikan formatter field biasa dan inject lewat constructor.”""",
    },
    {
        "id": "core-07-array-destructuring",
        "day": 2,
        "topic": "JavaScript",
        "title": "Output array destructuring",
        "kind": "mcq",
        "origin": "asli",
        "points": 10,
        "concept": """### Array destructuring dan “lubang”

Destructuring adalah cara membongkar array/object menjadi variable dengan sintaks singkat.

```js
const [first, second] = ['a', 'b'];
```

Koma tanpa nama di depan berarti **lewati posisi itu**:

```js
const [, , third] = ['a', 'b', 'c']; // third = 'c'
```

**Analogi:** bayangkan kamu mengambil barang dari rak bernomor. Koma pertama berarti “lewati rak 0”, koma kedua “lewati rak 1”, lalu ambil rak 2.""",
        "prompt": """Apa output dari kode berikut?

```js
const [, , animal] = ['Horse', 'Mouse', 'Cat'];
console.log(animal);
```

- A. `Horse`
- B. `Cat`
- C. `Mouse`
- D. `Undefined`""",
        "hints": [
            "Hitung posisi array mulai dari 0: `Horse` = 0, `Mouse` = 1, `Cat` = 2.",
            "Dua koma kosong berarti dua posisi pertama dilewati.",
        ],
        "answer": """**Jawaban: B. `Cat`**

**Trace posisi:**

| Posisi | Nilai | Aksi destructuring |
|---:|---|---|
| 0 | `Horse` | dilewati oleh koma pertama |
| 1 | `Mouse` | dilewati oleh koma kedua |
| 2 | `Cat` | diambil ke variable `animal` |

Jadi `animal` berisi `"Cat"` dan `console.log(animal)` mencetak `Cat`.""",
        "traps": """- **Menghitung koma dengan salah.** `[, , animal]` berarti dua elemen dilewati, bukan satu.
- **Mengira hasilnya `Mouse`.** Kalau hanya ada satu koma (`[, animal]`), maka `animal` adalah `Mouse`.
- **Mengira kekurangan elemen otomatis error.** Kalau array lebih pendek, variable yang tidak dapat nilai menjadi `undefined`.""",
        "speak": """“Array-nya Horse, Mouse, Cat. Dua koma kosong melewati Horse dan Mouse, jadi animal mengambil Cat. Output-nya Cat.”""",
    },
    {
        "id": "core-08-graphql",
        "day": 2,
        "topic": "Stack & Ekosistem",
        "title": "GraphQL: apa itu dan kapan dipakai?",
        "kind": "open",
        "origin": "asli",
        "points": 10,
        "concept": """### GraphQL = bahasa query untuk API

REST biasanya punya banyak endpoint: `/users`, `/users/1/posts`, `/posts/1/comments`. GraphQL biasanya punya **satu endpoint** (`/graphql`) dan client mengirim query yang menentukan field apa saja yang dibutuhkan.

Ada tiga istilah utama:

- **Schema** — kontrak tipe data yang tersedia.
- **Query** — permintaan baca dari client.
- **Resolver** — fungsi di server yang mengambil data untuk setiap field.

Analoginya: REST seperti memesan paket menu yang sudah ditentukan; GraphQL seperti prasmanan, kamu memilih sendiri lauk yang mau diambil.""",
        "prompt": """Kamu melihat logo GraphQL (hexagon/polygon berwarna pink). Jelaskan:

1. Apa itu GraphQL?
2. Kapan sebaiknya dipakai?
3. Apa trade-off dibanding REST?
4. Pernahkah kamu memakainya?""",
        "hints": [
            "Mulai dari masalah yang diselesaikan: over-fetching dan under-fetching pada REST.",
            "Sebutkan satu contoh situasi yang cocok, lalu satu situasi yang lebih baik tetap memakai REST.",
        ],
        "answer": """**Apa itu GraphQL?**

GraphQL adalah **query language untuk API** sekaligus runtime untuk mengeksekusi query tersebut. Client mengirim query yang bentuknya mirip JSON, lalu server mengembalikan data dengan bentuk yang sama. Semua permintaan biasanya masuk ke satu endpoint.

Contoh query:

```graphql
query {
  user(id: 1) {
    name
    posts {
      title
      comments {
        text
      }
    }
  }
}
```

**Kapan dipakai:**

- Data saling berelasi dan client butuh mengambil banyak relasi sekaligus.
- Ada beberapa client (web, mobile, partner) dengan kebutuhan field berbeda.
- Ingin menghindari **over-fetching** (data yang dikirim terlalu banyak) dan **under-fetching** (harus memanggil endpoint berkali-kali).
- Ingin schema yang kuat sebagai kontrak antara frontend dan backend.

**Trade-off dibanding REST:**

- REST lebih sederhana, mudah di-cache di level HTTP, dan cocok untuk CRUD biasa.
- GraphQL lebih fleksibel untuk client, tetapi server lebih kompleks: caching, query complexity, N+1 problem, dan otorisasi per field.
- File upload dan endpoint publik yang sederhana sering lebih mudah dengan REST.

**Jawaban jujur soal pengalaman:**

“Saya belum memakai GraphQL di produksi. Saya memahami konsepnya sebagai alternatif REST untuk data yang kompleks. Untuk CRUD sederhana saya masih akan memilih REST, karena caching dan debugging-nya lebih mudah.”

Kalau pernah mencoba, sebutkan konteksnya dengan jujur, misalnya “pernah membuat query sederhana di project latihan”, tanpa mengklaim pengalaman produksi.""",
        "traps": """- **Mengira GraphQL menggantikan database.** GraphQL hanya lapisan API; resolver tetap mengambil data dari database/service.
- **Mengira GraphQL selalu lebih cepat.** Query yang terlalu dalam bisa lebih berat; butuh batas kedalaman dan query complexity.
- **Mengklaim pengalaman yang tidak ada.** Interviewer biasanya mengejar detail; lebih aman jujur dan jelaskan konsep.
- **Lupa trade-off.** Jawaban bagus bukan “GraphQL lebih baik”, tetapi “tergantung kebutuhan”.""",
        "speak": """“GraphQL adalah query language untuk API dengan satu endpoint. Client menentukan field yang dibutuhkan, jadi cocok untuk data yang saling berelasi dan banyak client. Trade-off-nya, server dan caching lebih kompleks; saya belum memakainya di produksi, tetapi paham kapan ia lebih cocok daripada REST.”""",
    },
    {
        "id": "core-09-quarkus",
        "day": 2,
        "topic": "Stack & Ekosistem",
        "title": "Quarkus: apa itu dan kapan dipakai?",
        "kind": "open",
        "origin": "asli",
        "points": 10,
        "concept": """### Quarkus = Java framework untuk container dan cloud

Quarkus adalah framework Java modern yang dibuat untuk **Kubernetes**, container, dan GraalVM. Fokus utamanya: startup cepat dan memori rendah.

Perbandingan sederhananya:

- **Spring Boot** — ekosistem sangat besar, cocok untuk banyak aplikasi enterprise.
- **Quarkus** — lebih ringan dan cepat, cocok untuk microservice, serverless, atau lingkungan dengan banyak instance.

Logo Quarkus biasanya berupa kotak biru dengan kubus merah-hitam.

**Analogi:** Spring Boot seperti supermarket serba ada, sedangkan Quarkus seperti toko khusus yang lebih ringkas dan cepat dibuka.
""",
        "prompt": """Kamu melihat logo Quarkus (kotak biru dengan kubus merah-hitam). Jelaskan:

1. Apa itu Quarkus?
2. Kapan sebaiknya dipakai?
3. Apa kelebihan dan kekurangannya dibanding Spring Boot?
4. Pernahkah kamu memakainya?""",
        "hints": [
            "Hubungkan dengan kata kunci: Kubernetes, GraalVM, startup cepat, memori rendah.",
            "Bandingkan secara seimbang dengan Spring Boot; jangan hanya mengatakan salah satunya lebih baik.",
        ],
        "answer": """**Apa itu Quarkus?**

Quarkus adalah framework Java yang dirancang untuk **Kubernetes-native** dan **GraalVM**. Ia bisa dijalankan di JVM biasa atau dikompilasi menjadi native executable. Tujuannya mengurangi waktu startup dan konsumsi memori, terutama saat aplikasi berjalan di container.

**Kapan dipakai:**

- Microservice yang perlu cepat naik/turun saat scaling.
- Serverless atau Function-as-a-Service dengan cold start yang sensitif.
- Lingkungan container dengan banyak instance dan memori terbatas.
- Tim yang ingin tetap memakai Java tetapi dengan footprint lebih kecil.

**Kelebihan dibanding Spring Boot:**

- Startup lebih cepat, terutama mode native.
- Memori lebih rendah.
- Integrasi baik dengan Kubernetes, GraalVM, dan reactive programming.

**Kekurangan:**

- Ekosistem dan jumlah tutorial belum sebesar Spring Boot.
- Build native lebih lama dan butuh toolchain tambahan.
- Tidak semua library kompatibel dengan GraalVM native image.
- Untuk aplikasi CRUD biasa, Spring Boot sering lebih praktis karena banyak contoh dan library.

**Jawaban jujur soal pengalaman:**

“Saya belum memakai Quarkus di produksi. Saya mengenalnya sebagai framework Java yang fokus pada startup cepat dan memori rendah untuk Kubernetes. Untuk project saya sebelumnya, Spring Boot lebih familiar; Quarkus akan saya pertimbangkan kalau kebutuhan utamanya adalah efisiensi container.”

Jangan mengklaim pernah memakai kalau belum. Interviewer akan bertanya detail seperti cara build native atau extension yang dipakai.""",
        "traps": """- **Mengira Quarkus hanya untuk native.** Bisa juga berjalan di JVM biasa.
- **Mengira Quarkus selalu lebih baik.** Untuk aplikasi enterprise dengan banyak library, Spring Boot bisa lebih praktis.
- **Menyebut “Java-nya berubah”.** Quarkus tetap Java; yang berubah adalah framework dan cara packaging.
- **Tidak bisa membedakan logo.** Quarkus = kotak biru dengan kubus merah-hitam; GraphQL = hexagon/polygon pink.""",
        "speak": """“Quarkus adalah framework Java yang fokus pada Kubernetes dan GraalVM, dengan startup cepat dan memori rendah. Cocok untuk microservice atau serverless. Saya belum memakainya di produksi; untuk CRUD biasa saya masih memilih Spring Boot karena ekosistemnya lebih besar.”""",
    },
    {
        "id": "spring-01-primary",
        "day": 2,
        "topic": "Spring Boot",
        "title": "Latihan: memilih bean dengan @Primary",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### `@Primary` = kandidat default

Kalau ada beberapa bean dengan tipe sama, `@Primary` menandai salah satunya sebagai pilihan utama. Bean lain tetap ada dan masih bisa dipilih dengan `@Qualifier` atau nama bean.

**Analogi:** seperti menu default di kantin; kalau kamu tidak menyebut pilihan lain, menu default yang diambil.
""",
        "prompt": """Perhatikan kode berikut:

```java
public interface PaymentGateway {
    String pay();
}

@Component
public class StripeGateway implements PaymentGateway {
    public String pay() { return "Stripe"; }
}

@Component
public class MockGateway implements PaymentGateway {
    public String pay() { return "Mock"; }
}

@Service
public class CheckoutService {
    private final PaymentGateway gateway;

    public CheckoutService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public void checkout() {
        System.out.println(gateway.pay());
    }
}
```

Apa yang terjadi saat aplikasi dijalankan? Bagaimana cara membuat output-nya `Stripe`?""",
        "hints": [
            "Ada dua class yang implements `PaymentGateway`. Injection by type tidak tahu harus memilih yang mana.",
            "Tambahkan `@Primary` pada `StripeGateway`, atau `@Qualifier(\"stripeGateway\")` pada constructor.",
        ],
        "answer": """**Yang terjadi tanpa perubahan:** Spring gagal membuat `CheckoutService` karena ada dua kandidat `PaymentGateway`. Error-nya kurang lebih:

```text
NoUniqueBeanDefinitionException:
expected single matching bean but found 2: mockGateway, stripeGateway
```

**Perbaikan 1 — `@Primary`:**

```java
@Component
@Primary
public class StripeGateway implements PaymentGateway {
    public String pay() { return "Stripe"; }
}
```

Sekarang injection memilih `StripeGateway`, output `Stripe`.

**Perbaikan 2 — `@Qualifier`:**

```java
public CheckoutService(@Qualifier("stripeGateway") PaymentGateway gateway) {
    this.gateway = gateway;
}
```

Nama bean default untuk `@Component` adalah nama class dengan huruf pertama kecil: `stripeGateway`.

**Kenapa `@Primary` bukan satu-satunya jawaban:** keduanya benar. Pilih `@Primary` kalau Stripe memang default aplikasi; pilih `@Qualifier` kalau pemilihan bergantung pada class yang membutuhkan.""",
        "traps": """- **Menaruh `@Primary` di interface.** Annotation ini dipasang di class bean, bukan interface.
- **Menaruh `@Qualifier` di constructor tanpa nama bean yang tepat.** Nama default `@Component` adalah `stripeGateway`, bukan `StripeGateway`.
- **Mengira bean kedua hilang.** Keduanya tetap ada; `@Primary` hanya menentukan default.""",
        "speak": """“Ada dua bean PaymentGateway, jadi injection by type ambigu. Saya tandai StripeGateway dengan @Primary supaya menjadi default, atau memakai @Qualifier stripeGateway di constructor. Setelah itu checkout mencetak Stripe.”""",
    },
    {
        "id": "spring-02-qualifier",
        "day": 2,
        "topic": "Spring Boot",
        "title": "Latihan: @Qualifier memilih bean tertentu",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### `@Qualifier` = memanggil bean dengan namanya

**Analogi:** `@Primary` seperti “staf default”, sedangkan `@Qualifier` seperti “saya butuh staf bernama X”. Qualifier dipasang di titik injection dan mengalahkan pilihan default.""",
        "prompt": """Masih memakai `StripeGateway` dan `MockGateway` dari latihan sebelumnya. Perhatikan constructor berikut:

```java
public CheckoutService(@Qualifier("mockGateway") PaymentGateway gateway) {
    this.gateway = gateway;
}
```

Apa output dari `checkout()`? Apa yang terjadi kalau nama qualifier-nya salah, misalnya `@Qualifier("mock")`?""",
        "hints": [
            "Nama bean default dari `@Component` adalah nama class dengan huruf pertama kecil.",
            "Kalau qualifier tidak menemukan bean yang cocok, Spring tidak bisa menyelesaikan dependency.",
        ],
        "answer": """**Output:**

```text
Mock
```

Karena `@Qualifier("mockGateway")` memilih bean `MockGateway`, bukan `StripeGateway`.

**Kalau qualifier salah:**

```java
@Qualifier("mock")
```

Spring akan gagal dengan error kurang lebih:

```text
NoSuchBeanDefinitionException:
No qualifying bean of type 'PaymentGateway' available:
expected at least 1 bean which qualifies as autowire candidate.
```

**Cara memastikan nama bean:**

- Untuk `@Component` / `@Service`, nama default = nama class dengan huruf pertama kecil (`mockGateway`).
- Untuk `@Bean`, nama default = nama method (`mockGateway()`).
- Kamu bisa memberi nama eksplisit: `@Component("mock")` atau `@Bean(name = "mock")`.

**Kapan memakai qualifier:** kalau satu class butuh implementasi tertentu, sementara class lain butuh implementasi default. Ini lebih eksplisit daripada mengandalkan `@Primary`.""",
        "traps": """- **Salah nama bean.** `MockGateway` ≠ `mockGateway`; Spring peka huruf besar/kecil.
- **Memasang qualifier di class bean, bukan di injection point.** Untuk memilih, qualifier diletakkan di constructor/field.
- **Mengira qualifier memperbaiki semua konflik.** Kalau ada dua bean dengan nama sama (tidak mungkin dalam satu context), ada masalah konfigurasi lain.""",
        "speak": """“Qualifier mockGateway memilih bean MockGateway, jadi output-nya Mock. Kalau namanya salah, Spring melempar NoSuchBeanDefinitionException karena tidak ada bean yang cocok.”""",
    },
    {
        "id": "spring-03-bean-name",
        "day": 2,
        "topic": "Spring Boot",
        "title": "Latihan: nama bean dari method @Bean",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Nama bean `@Bean` berasal dari nama method

`@Bean` adalah method di class `@Configuration` yang mengembalikan object. Nama method menjadi **nama bean** secara default.

```java
@Bean
public Clock clock() { ... } // nama bean: clock
```

Kalau kamu menulis `@Bean(name = "jam")`, nama bean-nya menjadi `jam`.

**Analogi:** seperti memberi label pada kotak penyimpanan; nama method adalah label default yang dipakai Spring untuk menemukan kotaknya.
""",
        "prompt": """Perhatikan konfigurasi berikut:

```java
@Configuration
public class AppConfig {
    @Bean
    public Clock clock() {
        return Clock.systemUTC();
    }
}
```

Manakah yang berhasil mengambil bean ini?

- `context.getBean("clock")`
- `context.getBean("Clock")`
- `context.getBean(Clock.class)`

Jelaskan jawabanmu.""",
        "hints": [
            "Nama default bean dari method `clock()` adalah `clock`, bukan `Clock`.",
            "Kalau hanya ada satu bean bertipe `Clock`, mengambil berdasarkan tipe juga bisa.",
        ],
        "answer": """**Yang berhasil:**

- `context.getBean("clock")` → berhasil, karena nama bean = nama method.
- `context.getBean(Clock.class)` → berhasil, karena hanya ada satu bean bertipe `Clock`.
- `context.getBean("Clock")` → **gagal** dengan `NoSuchBeanDefinitionException`, karena nama bean peka huruf besar/kecil dan bukan `Clock`.

**Bukti nama bean:**

```java
System.out.println(context.containsBean("clock")); // true
System.out.println(context.containsBean("Clock")); // false
```

**Kalau ada dua bean bertipe sama**, `getBean(Clock.class)` menjadi ambigu. Kamu harus memakai nama bean atau `@Primary`/`@Qualifier`.

**Di Laravel:** ini mirip `app()->make('clock')` versus `app(Clock::class)`. Nama binding dan tipe class adalah dua hal berbeda.""",
        "traps": """- **Mengira nama bean mengikuti tipe return.** Nama default mengikuti nama method, bukan `Clock`.
- **Mengira `getBean(Class)` selalu aman.** Kalau ada beberapa bean dengan tipe sama, hasilnya ambigu.
- **Lupa bahwa nama bean case-sensitive.** `clock` dan `Clock` berbeda.""",
        "speak": """“Nama bean default-nya clock, diambil dari nama method. Jadi getBean clock berhasil, getBean Clock gagal. getBean berdasarkan Clock.class juga berhasil selama hanya ada satu bean Clock.”""",
    },
    {
        "id": "spring-04-component-scan",
        "day": 2,
        "topic": "Spring Boot",
        "title": "Latihan: kenapa @Component tidak ditemukan?",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Component scan punya batas package

`@SpringBootApplication` melakukan component scan dari package tempat class utama berada, termasuk sub-package di bawahnya.

Kalau class `@Component` berada di package yang berbeda dan bukan sub-package, Spring tidak menemukannya. Dependency injection lalu gagal dengan `NoSuchBeanDefinitionException`.

Analogi: kantor pusat hanya mencari karyawan di gedung dan lantai di bawahnya. Karyawan di gedung sebelah tidak otomatis terdaftar.""",
        "prompt": """Struktur package:

```text
com.example.app
├── Application.java          // @SpringBootApplication
└── order
    └── OrderService.java     // @Service

com.example.other
└── PaymentService.java       // @Service
```

`OrderService` melakukan injection `PaymentService`, tetapi aplikasi gagal start dengan `NoSuchBeanDefinitionException`. Apa penyebabnya dan bagaimana cara memperbaikinya?""",
        "hints": [
            "Dari package mana `@SpringBootApplication` melakukan scan secara default?",
            "Ada dua solusi: pindahkan class ke package yang discan, atau perluas scan-nya.",
        ],
        "answer": """**Penyebab:** `PaymentService` berada di `com.example.other`, sedangkan `Application` berada di `com.example.app`. Component scan default hanya mencakup `com.example.app` dan sub-package-nya (`com.example.app.*`). `com.example.other` bukan sub-package dari `com.example.app`, jadi `PaymentService` tidak terdaftar sebagai bean.

**Perbaikan 1 — pindahkan class:**

Pindahkan `PaymentService` ke `com.example.app.payment` (atau package lain di bawah `com.example.app`). Ini pilihan paling sederhana dan menjaga struktur.

**Perbaikan 2 — perluas component scan:**

```java
@SpringBootApplication(scanBasePackages = {"com.example.app", "com.example.other"})
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

Atau:

```java
@Configuration
@ComponentScan(basePackages = "com.example")
public class AppConfig { }
```

**Perbaikan 3 — daftarkan bean secara eksplisit:**

```java
@Configuration
public class PaymentConfig {
    @Bean
    public PaymentService paymentService() {
        return new PaymentService();
    }
}
```

Tapi kalau class-nya sudah `@Service`, memperluas scan atau memindahkan package lebih konsisten.""",
        "traps": """- **Mengira `@Service` otomatis terdaftar di seluruh aplikasi.** Hanya package yang discan.
- **Mengira `@SpringBootApplication` sama dengan scan seluruh `com.example`.** Default-nya package class utama dan sub-package.
- **Menambahkan `@Bean` untuk class yang sudah `@Service` tanpa perlu.** Bisa menghasilkan dua bean dengan tipe sama dan konflik baru.""",
        "speak": """“Application ada di package com.example.app, jadi scan default hanya ke package itu dan sub-package-nya. PaymentService di com.example.other tidak ikut discan, makanya tidak ditemukan. Saya bisa memindahkannya ke bawah com.example.app atau menambahkan scanBasePackages.”""",
    },
    {
        "id": "spring-05-field-qualifier",
        "day": 2,
        "topic": "Spring Boot",
        "title": "Latihan: @Qualifier pada field",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Field injection juga bisa memakai `@Qualifier`

Selain constructor, `@Qualifier` bisa dipasang pada field. Namun constructor injection lebih disarankan karena dependency terlihat jelas, object selalu dalam keadaan lengkap, dan lebih mudah diuji.

**Analogi:** seperti menempelkan label langsung di pintu kantor; bisa, tetapi alamat lengkap di surat (constructor) lebih jelas.
""",
        "prompt": """Perhatikan kode berikut:

```java
@Service
public class Greeter {
    @Autowired
    @Qualifier("spanishGreetingService")
    private GreetingService greetingService;

    public void greet() {
        System.out.println(greetingService.greet());
    }
}
```

Dengan bean `englishGreetingService` dan `spanishGreetingService` dari Soal 5, apa output dari `greet()`? Apa kelemahan field injection seperti ini?""",
        "hints": [
            "Qualifier memilih bean Spanyol, bukan bean default.",
            "Pikirkan kapan field diisi Spring dan bagaimana kamu menguji class ini tanpa Spring.",
        ],
        "answer": """**Output:**

```text
¡Hola!
```

Karena `@Qualifier("spanishGreetingService")` memilih `SpanishGreetingService`.

**Kelemahan field injection:**

1. **Dependency tidak terlihat di constructor.** Orang yang membaca class harus mencari field yang dianotasi.
2. **Sulit diuji tanpa Spring.** Untuk unit test, kamu harus memakai reflection atau Spring context; constructor injection cukup `new Greeter(mockService)`.
3. **Object bisa dibuat dalam keadaan tidak lengkap.** Kalau kamu `new Greeter()` langsung, field masih null.
4. **Tidak bisa memakai `final`.** Field tidak bisa dijamin tidak berubah.

**Versi yang lebih baik:**

```java
@Service
public class Greeter {
    private final GreetingService greetingService;

    public Greeter(@Qualifier("spanishGreetingService") GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    public void greet() {
        System.out.println(greetingService.greet());
    }
}
```

Output tetap `¡Hola!`, tetapi dependency jelas, immutable, dan mudah diuji.""",
        "traps": """- **Mengira `@Qualifier` hanya bisa di constructor.** Bisa di field dan setter, tetapi constructor lebih disarankan.
- **Mengira field injection selalu salah secara sintaks.** Ia berjalan, tetapi punya kelemahan desain.
- **Lupa nama bean.** `spanishGreetingService` berasal dari nama method `@Bean`; kalau method-nya diganti, qualifier harus ikut diganti.""",
        "speak": """“Qualifier spanishGreetingService memilih bean Spanyol, jadi output-nya ¡Hola!. Tapi field injection membuat dependency tidak terlihat dan sulit diuji. Saya lebih memilih constructor injection dengan qualifier yang sama.”""",
    },
    {
        "id": "js-01-object-destructuring",
        "day": 2,
        "topic": "JavaScript",
        "title": "Latihan: object destructuring + default",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### Object destructuring

```js
const { name, age } = user;
```

Kamu bisa mengganti nama variable dan memberi nilai default:

```js
const { name: userName, age = 20 } = user;
```

`name: userName` berarti ambil property `name`, simpan ke variable `userName`.

**Analogi:** seperti membuka paket dan mengambil hanya barang yang kamu butuhkan, lalu memberi label baru sesuai keperluan.
""",
        "prompt": """Apa output dari kode berikut?

```js
const user = { name: 'Ada', role: 'dev' };
const { name: userName, age = 20 } = user;
console.log(userName, age);
```

- A. `Ada undefined`
- B. `Ada 20`
- C. `name 20`
- D. `undefined 20`""",
        "hints": [
            "`name: userName` mengganti nama variable hasil destructuring.",
            "Property `age` tidak ada di object, jadi nilai default yang dipakai.",
        ],
        "answer": """**Jawaban: B. `Ada 20`**

**Trace:**

| Property | Ada di object? | Hasil |
|---|---|---|
| `name` | ya, `"Ada"` | disimpan ke variable `userName` |
| `age` | tidak | memakai default `20` |

Jadi `console.log(userName, age)` mencetak `Ada 20`.""",
        "traps": """- **Mengira `name: userName` mengambil property `userName`.** Yang diambil tetap `name`; `userName` hanya nama variable barunya.
- **Mengira default berlaku kalau property ada tapi bernilai `null`.** Default hanya dipakai kalau nilainya `undefined`.
- **Mengira urutan output terbalik.** Yang dicetak pertama `userName`, lalu `age`.""",
        "speak": """“Kita mengambil property name dan mengganti namanya menjadi userName, jadi hasilnya Ada. Property age tidak ada, jadi default 20 dipakai. Output-nya Ada 20.”""",
    },
    {
        "id": "js-02-array-rest",
        "day": 2,
        "topic": "JavaScript",
        "title": "Latihan: array destructuring + rest",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### Rest element

Tiga titik `...rest` mengumpulkan sisa elemen menjadi array baru.

```js
const [first, ...rest] = [1, 2, 3];
// first = 1, rest = [2, 3]
```

Koma kosong melewati elemen, seperti pada soal sebelumnya.

**Analogi:** seperti mengambil beberapa buku dari tumpukan; koma kosong berarti melewati buku tanpa mengambilnya, dan `...rest` mengambil sisa tumpukan.
""",
        "prompt": """Apa output dari kode berikut?

```js
const [first, , third, ...rest] = [10, 20, 30, 40, 50];
console.log(first, third, rest);
```

- A. `10 30 [40, 50]`
- B. `10 20 [30, 40, 50]`
- C. `10 30 40`
- D. `10 undefined [40, 50]`""",
        "hints": [
            "Posisi 0 = 10, posisi 1 = 20, posisi 2 = 30, posisi 3 = 40, posisi 4 = 50.",
            "`rest` mengumpulkan semua elemen setelah posisi yang sudah diambil.",
        ],
        "answer": """**Jawaban: A. `10 30 [40, 50]`**

**Trace:**

| Posisi | Nilai | Masuk ke |
|---:|---:|---|
| 0 | 10 | `first` |
| 1 | 20 | dilewati |
| 2 | 30 | `third` |
| 3 | 40 | `rest[0]` |
| 4 | 50 | `rest[1]` |

Jadi `first = 10`, `third = 30`, dan `rest = [40, 50]`.""",
        "traps": """- **Mengira `rest` berisi semua elemen.** Rest hanya berisi sisa setelah posisi yang diambil.
- **Salah menghitung koma.** Satu koma kosong melewati satu elemen.
- **Mengira `rest` menghasilkan angka 40 saja.** Rest selalu berupa array.""",
        "speak": """“First mengambil 10, satu koma melewati 20, third mengambil 30, dan rest mengumpulkan 40 dan 50. Output-nya 10 30 [40, 50].”""",
    },
    {
        "id": "js-03-scope",
        "day": 2,
        "topic": "JavaScript",
        "title": "Latihan: scope var vs let",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### Scope: di mana variable bisa diakses

- `var` → **function scope**. Selama masih di dalam function, variable bisa diakses, bahkan dari luar blok `if`.
- `let` dan `const` → **block scope**. Hanya hidup di dalam blok `{ ... }` tempat ia dideklarasikan.

Analogi: `var` seperti barang yang boleh dipakai di seluruh ruangan function; `let` seperti barang yang hanya boleh dipakai di dalam sekat ruangan.""",
        "prompt": """Apa output dari kode berikut?

```js
function test() {
  if (true) {
    var a = 1;
    let b = 2;
  }
  console.log(a);
  try {
    console.log(b);
  } catch (e) {
    console.log(e.name);
  }
}
test();
```

- A. `1 2`
- B. `1 ReferenceError`
- C. `undefined 2`
- D. `ReferenceError ReferenceError`""",
        "hints": [
            "`var a` bisa diakses di luar blok `if`, selama masih di dalam function.",
            "`let b` hanya hidup di dalam blok `if`. Di luar blok, variable itu tidak ada.",
        ],
        "answer": """**Jawaban: B. `1 ReferenceError`**

**Trace:**

| Variable | Scope | Setelah blok `if` |
|---|---|---|
| `a` (`var`) | seluruh function `test` | masih bisa diakses, nilainya 1 |
| `b` (`let`) | blok `if` saja | tidak ada di scope luar |

`console.log(a)` mencetak `1`.

`console.log(b)` melempar `ReferenceError` karena `b` tidak dideklarasikan di scope itu. Error ditangkap `try/catch`, lalu dicetak `e.name`, yaitu `ReferenceError`.""",
        "traps": """- **Mengira `var` juga block-scoped.** Tidak; `var` bocor ke seluruh function.
- **Mengira `let b` bernilai `undefined` di luar blok.** Variablenya tidak ada, bukan undefined.
- **Mengira `catch` mengubah nilai.** Catch hanya menangkap error dan mencetak namanya.""",
        "speak": """“Var a bisa diakses di luar if karena function scope, jadi tercetak 1. Let b hanya ada di dalam blok if, jadi saat diakses di luar terjadi ReferenceError, dan catch mencetak ReferenceError.”""",
    },
    {
        "id": "js-04-hoisting",
        "day": 2,
        "topic": "JavaScript",
        "title": "Latihan: hoisting dan TDZ",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### Hoisting

JavaScript memindahkan **deklarasi** ke atas scope, tetapi tidak selalu memindahkan **nilai**.

- `var x` di-hoist dan diinisialisasi dengan `undefined`.
- `let y` / `const y` juga di-hoist, tetapi berada di **Temporal Dead Zone (TDZ)**: belum bisa diakses sampai baris deklarasinya dijalankan.

Analogi: kursi sudah disiapkan di ruangan (deklarasi), tetapi barangnya belum boleh dipakai sampai upacara dimulai (baris deklarasi).""",
        "prompt": """Apa yang terjadi pada dua potongan kode berikut?

```js
console.log(x);
var x = 5;
```

```js
console.log(y);
let y = 10;
```

- A. `undefined` lalu `undefined`
- B. `ReferenceError` lalu `ReferenceError`
- C. `undefined` lalu `ReferenceError`
- D. `5` lalu `10`""",
        "hints": [
            "`var` di-hoist dan diberi nilai awal `undefined`.",
            "`let` berada di TDZ sebelum baris deklarasinya dieksekusi.",
        ],
        "answer": """**Jawaban: C. `undefined` lalu `ReferenceError`**

**Potongan pertama:**

```js
console.log(x);
var x = 5;
```

Dianggap seperti:

```js
var x;          // deklarasi di-hoist, nilai undefined
console.log(x); // undefined
x = 5;
```

**Potongan kedua:**

```js
console.log(y);
let y = 10;
```

`let y` sudah diketahui oleh JavaScript, tetapi belum boleh diakses sebelum deklarasinya. Ini disebut **Temporal Dead Zone**. Hasilnya:

```text
ReferenceError: Cannot access 'y' before initialization
```

Kalau kedua potongan dijalankan dalam satu file, baris pertama mencetak `undefined`, lalu program berhenti karena error di potongan kedua.""",
        "traps": """- **Mengira `let` tidak di-hoist.** Ia di-hoist, tetapi berada di TDZ.
- **Mengira `var x` sudah bernilai 5 sebelum assignment.** Nilainya `undefined`.
- **Mengira hoisting memindahkan nilai.** Yang dipindahkan hanya deklarasi; assignment tetap di tempatnya.""",
        "speak": """“Var x di-hoist dan nilainya undefined, jadi console log pertama mencetak undefined. Let y juga di-hoist tapi ada di TDZ, jadi mengaksesnya sebelum deklarasi menghasilkan ReferenceError.”""",
    },
    {
        "id": "js-05-map-filter",
        "day": 2,
        "topic": "JavaScript",
        "title": "Latihan: chain map dan filter",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### `filter` lalu `map`

- `filter` memilih elemen yang lolos kondisi dan mengembalikan array baru.
- `map` mengubah setiap elemen dan mengembalikan array baru dengan panjang yang sama.

Keduanya tidak mengubah array asli. Urutan pemanggilan penting: filter dulu, baru map, supaya map hanya bekerja pada elemen yang lolos.

**Analogi:** seperti menyaring ikan lalu memasaknya; `filter` memilih ikan yang lolos, `map` mengolah setiap ikan yang tersisa.
""",
        "prompt": """Apa output dari kode berikut?

```js
const nums = [1, 2, 3, 4, 5];
const result = nums.filter(n => n % 2 === 0).map(n => n * 10);
console.log(result);
```

- A. `[10, 20, 30, 40, 50]`
- B. `[20, 40]`
- C. `[2, 4]`
- D. `[1, 3, 5]`""",
        "hints": [
            "Filter dulu: angka mana yang genap?",
            "Setelah itu, setiap angka yang lolos dikali 10.",
        ],
        "answer": """**Jawaban: B. `[20, 40]`**

**Trace:**

| Tahap | Hasil |
|---|---|
| `nums` | `[1, 2, 3, 4, 5]` |
| `filter(n => n % 2 === 0)` | `[2, 4]` |
| `map(n => n * 10)` | `[20, 40]` |

Jadi output-nya `[20, 40]`.""",
        "traps": """- **Mengira `map` dijalankan dulu.** Chain dibaca dari kiri ke kanan: filter, lalu map.
- **Mengira `filter` mengubah array asli.** Ia mengembalikan array baru.
- **Mengira hasil map tetap `[2, 4]`.** Map mengubah setiap elemen menjadi `n * 10`.""",
        "speak": """“Filter mengambil angka genap, yaitu 2 dan 4. Setelah itu map mengalikan masing-masing dengan 10, jadi hasilnya 20 dan 40.”""",
    },
    {
        "id": "js-06-undefined-null",
        "day": 2,
        "topic": "JavaScript",
        "title": "Latihan: undefined vs null",
        "kind": "mcq",
        "origin": "latihan",
        "points": 5,
        "concept": """### `undefined` vs `null`

- `undefined` → nilai belum diberikan; sering muncul saat variable dideklarasikan tanpa isi atau property tidak ada.
- `null` → nilai kosong yang **sengaja** diberikan oleh programmer.

`==` melakukan type coercion (konversi otomatis), sedangkan `===` membandingkan nilai dan tipe. Untuk menghindari kejutan, biasakan memakai `===`.

**Analogi:** `undefined` seperti kolom formulir yang belum diisi; `null` seperti kolom yang sengaja ditulis “kosong”.
""",
        "prompt": """Apa output dari kode berikut?

```js
let a;
const b = null;
console.log(a === undefined);
console.log(b === undefined);
console.log(b == undefined);
console.log(typeof null);
```

- A. `true false true "object"`
- B. `true true true "null"`
- C. `false false false "object"`
- D. `true false false "null"`""",
        "hints": [
            "Variable `let a;` tanpa nilai otomatis bernilai `undefined`.",
            "`null == undefined` bernilai true, tetapi `null === undefined` bernilai false. Perhatikan `typeof null`.",
        ],
        "answer": """**Jawaban: A. `true false true "object"`**

**Penjelasan baris per baris:**

| Ekspresi | Hasil | Alasan |
|---|---|---|
| `a === undefined` | `true` | `let a;` tanpa nilai = `undefined` |
| `b === undefined` | `false` | `b` adalah `null`, bukan `undefined` |
| `b == undefined` | `true` | `==` melakukan coercion; `null` dan `undefined` dianggap setara |
| `typeof null` | `"object"` | quirk lama JavaScript; `null` bukan object sungguhan |

**Saran:** gunakan `===` dan `!==` agar tidak bergantung pada coercion. Untuk mengecek null/undefined sekaligus, gunakan `value == null` (sengaja `==`) atau `value ?? defaultValue`.""",
        "traps": """- **Mengira `typeof null` menghasilkan `"null"`.** Hasilnya `"object"`, bug historis JavaScript.
- **Mengira `null === undefined` true.** Strict equality membandingkan tipe, jadi false.
- **Mengira `let a;` error.** Variable otomatis `undefined`.
- **Memakai `==` tanpa sadar.** Ia bisa menyamakan `0`, `""`, dan `false`; gunakan `===`.""",
        "speak": """“A belum diberi nilai, jadi undefined, sehingga a === undefined true. B bernilai null, jadi b === undefined false, tapi b == undefined true karena coercion. typeof null itu object, quirk JavaScript.”""",
    },
]
