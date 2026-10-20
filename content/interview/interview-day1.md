# Interview Day 1 — Java & Membaca Kode

Target hari ini: kamu bisa **membaca kode Java sederhana**, menelusuri nilai variable, dan menjelaskan NullPointerException. Kamu belum perlu hafal semua library. Fokusnya adalah cara berpikir.

## Cara Pakai Halaman Ini

1. Baca teori di halaman ini sambil membuka editor atau kertas.
2. Kerjakan **Soal Inti** tanpa melihat jawaban. Tulis tebakanmu dulu.
3. Buka hint satu per satu. Baru setelah itu bandingkan dengan jawaban.
4. Ucapkan penjelasan dengan suara keras. Kalau kamu bisa menjelaskan, kamu sudah paham.
5. Tandai status soal: **belum dicoba**, **salah**, atau **benar**.

Buka bank soalnya di sini: [Interview Prep — Hari 1](#/interview/day1).

## 1. Bentuk Program Java

Java adalah bahasa **compiled**: kode diubah menjadi bytecode lalu dijalankan JVM. Untuk belajar, anggap saja file `.java` dijalankan oleh Java.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello!");
    }
}
```

Arti bagian-bagiannya:

- `public class Hello` → membuat class bernama `Hello`. Nama file harus `Hello.java`.
- `public static void main(String[] args)` → pintu masuk program. Java mulai dari sini.
- `System.out.println(...)` → mencetak teks lalu pindah baris.
- `System.out.print(...)` → mencetak tanpa pindah baris.

Java memakai titik koma `;` di akhir statement dan kurung kurawal `{ }` untuk blok.

Analogi: file Java seperti satu kantor. `class` adalah ruangan, `main` adalah resepsionis yang pertama kali menerima tamu, dan method lain adalah staf di dalamnya.

## 2. Variable dan Tipe Data

Variable adalah **kotak berlabel**. Tipe data menentukan isi kotak dan operasi yang boleh dilakukan.

```java
int umur = 20;
double ipk = 3.75;
boolean lulus = true;
String nama = "Dimas";
```

| Tipe | Isi | Contoh | Catatan |
|---|---|---|---|
| `int` | bilangan bulat | `42`, `-7` | tidak bisa desimal |
| `double` | bilangan desimal | `3.75` | untuk angka pecahan |
| `boolean` | benar/salah | `true`, `false` | hanya dua nilai |
| `char` | satu karakter | `'A'` | memakai kutip tunggal |
| `String` | teks | `"Halo"` | memakai kutip ganda, bukan tipe primitif |

Java adalah **strongly typed**: tipe harus cocok. `int x = "halo";` adalah error.

Perbedaan dengan PHP/Laravel: PHP lebih longgar, Java lebih ketat. Di Laravel kamu bisa menulis `$umur = 20;` tanpa tipe. Di Java kamu menulis `int umur = 20;`. Tipe membuat error lebih cepat terdeteksi.

## 3. Operator

```java
int a = 10;
int b = 3;

System.out.println(a + b);  // 13
System.out.println(a - b);  // 7
System.out.println(a * b);  // 30
System.out.println(a / b);  // 3  (int / int = int, desimal dibuang)
System.out.println(a % b);  // 1  (sisa bagi)
```

Yang perlu diingat:

- `=` adalah **assignment** (mengisi kotak), bukan perbandingan.
- `==` membandingkan nilai primitif.
- `%` adalah modulus, yaitu sisa bagi. Ini sering dipakai di FizzBuzz.

Untuk membandingkan `String`, jangan memakai `==`. Gunakan `.equals()`:

```java
String a = "halo";
String b = "halo";
System.out.println(a.equals(b)); // true
```

`==` pada object membandingkan alamat/reference, bukan isi teks.

## 4. if / else

```java
int score = 75;

if (score >= 80) {
    System.out.println("A");
} else if (score >= 70) {
    System.out.println("B");
} else {
    System.out.println("C");
}
```

Dibaca dari atas. Begitu satu kondisi `true`, blok itu dijalankan dan sisanya dilewati. Output contoh di atas adalah `B`.

Analogi: satpam mengecek daftar aturan dari atas. Aturan pertama yang cocok yang dipakai.

## 5. Loop

### for

```java
for (int i = 1; i <= 5; i++) {
    System.out.println(i);
}
```

Tiga bagian:

- `int i = 1` → mulai.
- `i <= 5` → lanjut selama benar.
- `i++` → tambah 1 setiap putaran.

Outputnya `1` sampai `5`.

### while

```java
int i = 1;
while (i <= 5) {
    System.out.println(i);
    i++;
}
```

Hasilnya sama. Kalau lupa `i++`, loop tidak pernah berhenti (**infinite loop**).

### Accumulator

Pola menjumlahkan nilai di dalam loop:

```java
int sum = 0;
for (int i = 1; i <= 5; i++) {
    sum = sum + i; // atau sum += i
}
System.out.println(sum); // 15
```

`sum` hidup di luar loop, sehingga nilainya terus terbawa. Ini disebut **accumulator**.

## 6. Method

Method adalah blok kode yang bisa dipanggil ulang.

```java
public static int tambah(int a, int b) {
    return a + b;
}

public static void main(String[] args) {
    int hasil = tambah(2, 3);
    System.out.println(hasil); // 5
}
```

- `int` sebelum `tambah` adalah **return type**. Method mengembalikan angka.
- `void` berarti tidak mengembalikan nilai.
- `a` dan `b` adalah **parameter**.
- `return` mengembalikan hasil dan menghentikan method.

Di Laravel/PHP, ini mirip function:

```php
function tambah(int $a, int $b): int {
    return $a + $b;
}
```

## 7. Class dan Object

Class adalah **cetakan**, object adalah **hasil cetakannya**.

```java
class User {
    String name;
    int age;

    User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    void sayHello() {
        System.out.println("Halo, " + name);
    }
}

User user = new User("Dimas", 20);
user.sayHello(); // Halo, Dimas
```

- `new User(...)` membuat object.
- `this.name` merujuk ke field milik object.
- `user.sayHello()` memanggil method pada object.

Analogi: `class` adalah desain rumah; `new` adalah membangun rumah; object adalah rumah yang bisa kamu tempati.

Di Laravel, class dan object juga sama: `class User` adalah cetakan, `new User()` atau object dari Eloquent adalah instance.

## 8. Interface dan Polymorphism

Interface adalah **kontrak**: kumpulan method yang wajib dimiliki implementasinya.

```java
interface GreetingService {
    String greet();
}

class EnglishGreetingService implements GreetingService {
    public String greet() {
        return "Hello!";
    }
}

class SpanishGreetingService implements GreetingService {
    public String greet() {
        return "¡Hola!";
    }
}
```

Kamu bisa memakai tipe interface untuk menampung implementasi mana pun:

```java
GreetingService service = new EnglishGreetingService();
System.out.println(service.greet()); // Hello!
```

Inilah dasar **dependency injection** di Spring: class meminta `GreetingService`, lalu Spring memilih implementasinya.

Di Laravel, ini mirip interface + binding di service container:

```php
interface GreetingService { public function greet(): string; }

$this->app->bind(GreetingService::class, EnglishGreetingService::class);
```

## 9. static

`static` berarti milik **class**, bukan milik object.

```java
class Counter {
    static int total = 0;

    static void tambah() {
        total++;
    }
}

Counter.tambah();
System.out.println(Counter.total); // 1
```

Kamu memanggilnya lewat nama class, bukan lewat object. Yang penting untuk interview: **Spring tidak meng-inject static field**. Ini penyebab umum NullPointerException di soal Spring.

## 10. Cara Trace Kode

Trace artinya menjalankan kode di kepala atau di kertas, baris per baris.

Langkahnya:

1. Tulis semua variable dan nilai awalnya.
2. Baca kode dari atas ke bawah.
3. Setiap ada assignment, perbarui nilai di tabel.
4. Setiap ada loop, catat nilai sebelum dan sesudah putaran.
5. Setiap ada pemanggilan method, masuk ke method lalu kembali.
6. Tulis output sesuai urutan pencetakan.

Contoh:

```java
int a = 2;
int b = 5;
int temp = a;
a = b;
b = temp;
System.out.println(a + " " + b);
```

| Baris | a | b | temp | Output |
|---|---:|---:|---:|---|
| `int a = 2;` | 2 | — | — | — |
| `int b = 5;` | 2 | 5 | — | — |
| `int temp = a;` | 2 | 5 | 2 | — |
| `a = b;` | 5 | 5 | 2 | — |
| `b = temp;` | 5 | 2 | 2 | — |
| `println(a + " " + b);` | 5 | 2 | 2 | `5 2` |

Kunci trace: **jangan mengandalkan ingatan**. Tulis tabel. Interviewer lebih menghargai proses yang jelas daripada jawaban cepat yang salah.

## 11. NullPointerException (NPE)

`null` berarti **tidak ada object**. Variable-nya ada, tetapi tidak menunjuk ke object apa pun.

```java
String name = null;
System.out.println(name.length()); // NullPointerException
```

Kenapa? `length()` adalah method milik object String. Kalau object-nya tidak ada, method tidak bisa dipanggil.

Analogi: kamu punya alamat rumah di kertas, tetapi rumahnya tidak dibangun. Begitu kamu mengetuk pintu, tidak ada yang bisa dibuka.

Contoh lain:

```java
String[] names = new String[3];
System.out.println(names[0].length()); // NPE, elemen default null

class User { String email; }
User user = new User();
System.out.println(user.email.length()); // NPE, field email default null
```

Cara mencegah:

```java
if (name != null) {
    System.out.println(name.length());
}
```

Atau beri nilai default yang aman:

```java
String name = "";
System.out.println(name.length()); // 0
```

Di Laravel/PHP, error yang mirip adalah:

```text
Call to a member function length() on null
```

Konsepnya sama: memanggil method pada nilai null.

## 12. Jembatan dari Laravel

| Laravel / PHP | Java / Spring Boot | Inti yang sama |
|---|---|---|
| `$user = new User()` | `User user = new User()` | membuat object |
| `function tambah($a, $b)` | `int tambah(int a, int b)` | method/function |
| `interface` + `bind()` | `interface` + `@Bean`/`@Component` | kontrak dan implementasi |
| Service container | `ApplicationContext` | tempat object dikelola |
| Constructor type-hint | `@Autowired` / constructor injection | dependency diberikan dari luar |
| `Route::get()` + Controller | `@GetMapping` + `@RestController` | endpoint HTTP |
| `Call to a member function on null` | `NullPointerException` | error pada null |

Kamu tidak memulai dari nol. Kamu hanya mengganti **sintaks** dan **tool**, konsepnya banyak yang sama.

## 13. Checklist Hari 1

Centang kalau kamu sudah bisa tanpa melihat catatan:

- [ ] Menjelaskan perbedaan `int`, `double`, `boolean`, `String`.
- [ ] Menjelaskan arti `=` dan `==`.
- [ ] Menelusuri loop `for` sederhana dengan tabel.
- [ ] Menjelaskan perbedaan `print` dan `println`.
- [ ] Menjelaskan perbedaan class dan object.
- [ ] Menjelaskan fungsi interface.
- [ ] Menjelaskan kenapa `null.length()` error.
- [ ] Menjelaskan kenapa static field tidak di-inject Spring.
- [ ] Mengerjakan Soal Inti Hari 1 dan 8 soal latihan.
- [ ] Merekam suaramu saat menjelaskan satu soal.

## Latihan di Bank Soal

- Soal inti: [Tebak output UnknownSequence](#/interview/core-01-unknown-sequence)
- Trace reassignment: [Latihan 1](#/interview/java-trace-01-reassign)
- Trace if/else: [Latihan 2](#/interview/java-trace-02-condition)
- Trace loop: [Latihan 3](#/interview/java-trace-03-sum-loop)
- Trace swap: [Latihan 4](#/interview/java-trace-04-swap)
- Trace string: [Latihan 5](#/interview/java-trace-05-string-loop)
- NPE String: [Latihan 6](#/interview/npe-01-string-null)
- NPE array: [Latihan 7](#/interview/npe-02-array-default)
- NPE field: [Latihan 8](#/interview/npe-03-object-field)

Setelah Hari 1, lanjut ke [Hari 2 — Spring Boot & JavaScript](#/lessons/interview-day2).
