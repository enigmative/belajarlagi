"""Bank soal Interview Prep — Hari 1 (Java + trace + NPE).

Semua teks memakai Markdown agar bisa dirender oleh frontend yang sama
dengan lesson biasa. Solusi dan pembahasan tinggal di backend.
"""

QUESTIONS_DAY1 = [
    {
        "id": "core-01-unknown-sequence",
        "day": 1,
        "topic": "Java — Loop & Trace",
        "title": "Tebak output UnknownSequence",
        "kind": "open",
        "origin": "asli",
        "points": 10,
        "concept": """### Variable, loop, dan urutan eksekusi

**Analogi:** variable seperti **kotak berlabel**. `int a = 0` berarti kamu menyiapkan kotak bernama `a` dan mengisinya dengan angka `0`. Java adalah **strongly typed**: kotak `int` hanya boleh diisi bilangan bulat.

Loop `for` adalah instruksi berulang dengan tiga bagian:

```java
for (int i = 2; i < n; i++) { ... }
```

- `int i = 2` → mulai dari 2.
- `i < n` → selama kondisi benar, lanjut.
- `i++` → setelah satu putaran, tambah 1.

Di Laravel/PHP kamu biasa menulis `for ($i = 2; $i < $n; $i++)`. Konsepnya sama; bedanya Java harus menyebut tipe data `int`.

Yang perlu diperhatikan: **assignment** (`a = b`) menimpa isi kotak. Urutan baris sangat penting.""",
        "prompt": """Perhatikan kode Java berikut. Apa yang tercetak di layar?

```java
public class UnknownSequence {
    public static void main(String[] args) {
        int n = 10;
        int a = 0, b = 1;
        System.out.print(a + " " + b + " ");
        for (int i = 2; i < n; i++) {
            int unknown = a + b;
            System.out.print(unknown + " ");
            a = b;
            b = unknown;
        }
    }
}
```

Tulis output lengkapnya, lalu jelaskan kenapa hasilnya begitu.""",
        "hints": [
            "Sebelum loop, program sudah mencetak `a` dan `b`. Loop baru berjalan dari `i = 2` sampai `i = 9`.",
            "Di setiap putaran: hitung `unknown = a + b`, cetak, lalu pindahkan nilai: `a` mengambil nilai `b`, dan `b` mengambil nilai `unknown`.",
        ],
        "answer": """**Output:**

```text
0 1 1 2 3 5 8 13 21 34 
```

Itu adalah **10 angka pertama deret Fibonacci**. Ada spasi setelah angka terakhir karena `System.out.print` tidak membuat baris baru.

**Trace nilai per putaran:**

| Posisi | i | a (awal) | b (awal) | unknown | Output | a (akhir) | b (akhir) |
|---|---:|---:|---:|---:|---|---:|---:|
| sebelum loop | — | 0 | 1 | — | `0 1 ` | 0 | 1 |
| putaran 1 | 2 | 0 | 1 | 1 | `1 ` | 1 | 1 |
| putaran 2 | 3 | 1 | 1 | 2 | `2 ` | 1 | 2 |
| putaran 3 | 4 | 1 | 2 | 3 | `3 ` | 2 | 3 |
| putaran 4 | 5 | 2 | 3 | 5 | `5 ` | 3 | 5 |
| putaran 5 | 6 | 3 | 5 | 8 | `8 ` | 5 | 8 |
| putaran 6 | 7 | 5 | 8 | 13 | `13 ` | 8 | 13 |
| putaran 7 | 8 | 8 | 13 | 21 | `21 ` | 13 | 21 |
| putaran 8 | 9 | 13 | 21 | 34 | `34 ` | 21 | 34 |
| selesai | 10 | 21 | 34 | — | — | 21 | 34 |

**Langkah membacanya:**

1. Sebelum loop: `a = 0`, `b = 1`, langsung cetak `0 1 `.
2. Loop mulai `i = 2`; kondisi `2 < 10` benar.
3. `unknown = a + b = 0 + 1 = 1`; cetak `1`.
4. `a = b` → `a = 1`; `b = unknown` → `b = 1`.
5. Putaran berikutnya mengulang pola yang sama. Karena `a` dan `b` selalu berisi dua angka terakhir, `unknown` selalu angka berikutnya.
6. Loop berhenti saat `i = 10` karena `10 < 10` salah. Total ada 2 angka awal + 8 putaran = 10 angka.""",
        "traps": """- **Mengira loop berjalan 10 kali.** Loop berjalan 8 kali (`i = 2` sampai `9`), lalu ditambah dua angka yang dicetak sebelum loop.
- **Salah urutan update.** Kalau `a = unknown` ditulis sebelum `b = unknown`, nilai `b` yang lama hilang dan deretnya rusak.
- **Mengira `unknown` bisa dipakai setelah loop.** `unknown` dideklarasikan di dalam blok `for`, jadi hanya hidup di dalam blok itu.
- **Lupa spasi/trailing space.** `System.out.print` mencetak persis seperti yang diminta, termasuk spasi terakhir.""",
        "speak": """“Kode ini mencetak deret Fibonacci. Sebelum loop ada dua angka awal, 0 dan 1; di dalam loop, `unknown` adalah jumlah dua angka sebelumnya, lalu `a` dan `b` digeser. Loop berjalan dari i=2 sampai 9, jadi outputnya 10 angka: 0 1 1 2 3 5 8 13 21 34.”""",
    },
    {
        "id": "java-trace-01-reassign",
        "day": 1,
        "topic": "Java Dasar",
        "title": "Trace reassignment sederhana",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Assignment dievaluasi dari kanan

`x = x + 3` bukan persamaan matematika. Artinya: **hitung dulu sisi kanan**, lalu simpan hasilnya ke kotak `x`. Kotak lama ditimpa.

Analogi: kamu punya kotak berisi 5. Kamu mengambil isinya, menambah 3, lalu menaruh hasil 8 kembali ke kotak yang sama.""",
        "prompt": """Apa output dari kode berikut?

```java
int x = 5;
x = x + 3;
x = x * 2;
System.out.println(x);
```""",
        "hints": [
            "Kerjakan satu baris setiap kali. Jangan langsung menghitung semuanya di kepala.",
            "Setelah baris kedua, berapa isi `x`? Gunakan nilai itu untuk baris ketiga.",
        ],
        "answer": """**Output:**

```text
16
```

**Trace:**

| Baris | Perintah | Nilai `x` setelah baris |
|---|---|---:|
| 1 | `int x = 5;` | 5 |
| 2 | `x = x + 3;` | 8 |
| 3 | `x = x * 2;` | 16 |
| 4 | `System.out.println(x);` | 16 |

Baris kedua memakai `x` lama (5), bukan nilai awal program. Baris ketiga memakai `x` yang sudah menjadi 8, sehingga `8 * 2 = 16`.""",
        "traps": """- **Menganggap `x = x + 3` seperti aljabar** yang bisa dicoret menjadi `0 = 3`. Di programming, `=` adalah assignment.
- **Memakai nilai awal 5 untuk baris ketiga.** Nilai `x` sudah berubah menjadi 8.
- **Mengira `*` dijalankan sebelum `+` pada baris berbeda.** Setiap baris selesai sebelum baris berikutnya.""",
        "speak": """“Saya trace dari atas. `x` mulai 5, lalu ditambah 3 menjadi 8, lalu dikali 2 menjadi 16. Jadi outputnya 16.”""",
    },
    {
        "id": "java-trace-02-condition",
        "day": 1,
        "topic": "Java Dasar",
        "title": "Trace if / else if",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Rantai kondisi berhenti di cabang pertama yang benar

`if / else if / else` dibaca dari atas. Begitu satu kondisi bernilai `true`, blok itu dijalankan, lalu seluruh rantai dilewati.

Analogi: satpam mengecek daftar aturan dari atas. Begitu satu aturan cocok, kamu dipersilakan masuk dan aturan di bawahnya tidak dicek lagi.""",
        "prompt": """Apa output dari kode berikut?

```java
int score = 75;
if (score >= 80) {
    System.out.println("A");
} else if (score >= 70) {
    System.out.println("B");
} else {
    System.out.println("C");
}
```""",
        "hints": [
            "Cek kondisi pertama: apakah 75 >= 80?",
            "Kalau kondisi pertama salah, cek kondisi kedua: apakah 75 >= 70?",
        ],
        "answer": """**Output:**

```text
B
```

**Trace:**

| Kondisi | Hasil | Aksi |
|---|---|---|
| `score >= 80` → `75 >= 80` | `false` | lanjut ke `else if` |
| `score >= 70` → `75 >= 70` | `true` | cetak `B`, lewati `else` |
| `else` | tidak dicek | — |

Karena 75 memenuhi syarat kedua, program mencetak `B` dan tidak mencetak `A` atau `C`.""",
        "traps": """- **Mengira `A` dan `B` bisa tercetak bersamaan.** `else if` hanya dicek kalau kondisi sebelumnya salah.
- **Salah memahami `>=`.** `75 >= 70` benar; `70 >= 70` juga benar.
- **Menganggap `else` selalu dijalankan.** `else` hanya jalan kalau semua kondisi di atasnya salah.""",
        "speak": """“Nilainya 75. Kondisi pertama, minimal 80, salah; kondisi kedua, minimal 70, benar. Jadi program masuk ke cabang B dan tidak mengecek else.”""",
    },
    {
        "id": "java-trace-03-sum-loop",
        "day": 1,
        "topic": "Java — Loop & Trace",
        "title": "Trace loop penjumlahan",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Accumulator

Variabel yang terus diperbarui di dalam loop sering disebut **accumulator** (penampung). Pola umumnya:

```java
int total = 0;
for (...) {
    total = total + nilaiBaru;
}
```

`total` menyimpan hasil sejauh ini. Di Laravel/PHP polanya sama, misalnya `$total += $item->price;`.

**Analogi:** seperti celengan—setiap putaran kamu memasukkan koin baru, tetapi saldo yang sudah terkumpul tidak hilang.
""",
        "prompt": """Apa output dari kode berikut?

```java
int sum = 0;
for (int i = 1; i <= 5; i++) {
    sum += i;
}
System.out.println(sum);
```""",
        "hints": [
            "Buat tabel dengan kolom `i` dan `sum`. Mulai dari `sum = 0`.",
            "`sum += i` sama dengan `sum = sum + i`. Hati-hati dengan kondisi `i <= 5`.",
        ],
        "answer": """**Output:**

```text
15
```

**Trace:**

| Putaran | i | sum sebelum | sum sesudah (`sum + i`) |
|---|---:|---:|---:|
| 1 | 1 | 0 | 1 |
| 2 | 2 | 1 | 3 |
| 3 | 3 | 3 | 6 |
| 4 | 4 | 6 | 10 |
| 5 | 5 | 10 | 15 |
| selesai | 6 | 15 | loop berhenti |

Jumlahnya `1 + 2 + 3 + 4 + 5 = 15`.""",
        "traps": """- **Memakai `i < 5`.** Kondisi yang benar adalah `i <= 5`, jadi angka 5 ikut dihitung.
- **Mengira `sum` di-reset setiap putaran.** `sum` dideklarasikan di luar loop dan terus bertambah.
- **Menjumlahkan 0..5 atau 1..4.** Mulai dari 1 dan berhenti setelah 5.""",
        "speak": """“Saya mulai sum nol. Loop jalan untuk i satu sampai lima, dan setiap putaran sum ditambah i. Hasil akhirnya 1 plus 2 plus 3 plus 4 plus 5, yaitu 15.”""",
    },
    {
        "id": "java-trace-04-swap",
        "day": 1,
        "topic": "Java — Loop & Trace",
        "title": "Trace tukar nilai",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Menukar isi dua kotak butuh kotak ketiga

Kalau kamu langsung menulis `a = b`, isi `a` yang lama hilang sebelum sempat dipindahkan. Solusinya: simpan dulu nilai `a` di `temp` (temporary).

Analogi: memindahkan air dari gelas A ke gelas B. Kamu butuh gelas kosong supaya air di A tidak tumpah.""",
        "prompt": """Apa output dari kode berikut?

```java
int a = 3, b = 8;
int temp = a;
a = b;
b = temp;
System.out.println(a + " " + b);
```""",
        "hints": [
            "Catat nilai `a`, `b`, dan `temp` setelah setiap baris.",
            "Perhatikan bahwa `a + \" \" + b` menggabungkan teks, bukan menjumlahkan angka.",
        ],
        "answer": """**Output:**

```text
8 3
```

**Trace:**

| Baris | a | b | temp |
|---|---:|---:|---:|
| `int a = 3, b = 8;` | 3 | 8 | — |
| `int temp = a;` | 3 | 8 | 3 |
| `a = b;` | 8 | 8 | 3 |
| `b = temp;` | 8 | 3 | 3 |
| `println(a + " " + b);` | 8 | 3 | 3 |

Nilai `a` dan `b` berhasil bertukar karena nilai awal `a` disimpan dulu di `temp`.""",
        "traps": """- **Lupa `temp`.** Kalau langsung `a = b; b = a;`, kedua variable bisa berakhir bernilai 8.
- **Mengira `a + " " + b` menghasilkan 11.** Karena ada string `" "`, Java melakukan penggabungan teks menjadi `"8 3"`.
- **Salah urutan.** Simpan `a` ke `temp` sebelum `a` ditimpa.""",
        "speak": """“Kita menyimpan nilai a di temp, lalu a diisi b, lalu b diisi temp. Hasilnya a menjadi 8 dan b menjadi 3. Output-nya 8 spasi 3.”""",
    },
    {
        "id": "java-trace-05-string-loop",
        "day": 1,
        "topic": "Java — Loop & Trace",
        "title": "Trace string di dalam loop",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### String concatenation

Di Java, `+` bisa berarti penjumlahan angka atau **penggabungan string**. Kalau salah satu sisi adalah `String`, hasilnya menjadi `String`.

```java
String result = "";
result = result + 1; // "1", bukan angka 1
```

Di PHP kamu mungkin menulis `$result .= $i;`. Tanda `.=` khusus string; di Java tetap memakai `+`.

**Analogi:** seperti menyambung gerbong kereta; setiap gerbong baru ditempelkan di belakang, bukan dijumlahkan seperti angka.
""",
        "prompt": """Apa output dari kode berikut?

```java
String result = "";
for (int i = 1; i <= 4; i++) {
    result = result + i;
}
System.out.println(result);
```""",
        "hints": [
            "Mulai dengan `result` berisi string kosong `\"\"`.",
            "Di setiap putaran, angka `i` diubah menjadi teks lalu ditempel di belakang `result`.",
        ],
        "answer": """**Output:**

```text
1234
```

**Trace:**

| Putaran | i | result sebelum | result sesudah |
|---|---:|---|---|
| 1 | 1 | `""` | `"1"` |
| 2 | 2 | `"1"` | `"12"` |
| 3 | 3 | `"12"` | `"123"` |
| 4 | 4 | `"123"` | `"1234"` |

Hasilnya adalah teks `"1234"`, bukan angka 10, karena `result` bertipe `String`.""",
        "traps": """- **Menjumlahkan seperti angka.** `"1" + "2"` menghasilkan `"12"`, bukan `3`.
- **Mengira `result` berubah menjadi angka.** Tipe tetap `String` selama penggabungan.
- **Lupa bahwa `result = result + i` membuat string baru.** String di Java immutable; isi lama tidak diubah di tempat.""",
        "speak": """“Result awalnya string kosong. Setiap putaran, angka i ditempelkan sebagai teks. Jadi hasilnya 1234, bukan hasil penjumlahan 10.”""",
    },
    {
        "id": "npe-01-string-null",
        "day": 1,
        "topic": "NullPointerException",
        "title": "NPE pada String null",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Null = kotak berlabel tanpa isi

`null` berarti **tidak ada object**. Variable-nya ada, tetapi tidak menunjuk ke object apa pun.

Kalau kamu memanggil method pada reference yang `null`, Java melempar **NullPointerException (NPE)**. Analogi: kamu punya alamat rumah di kertas, tetapi rumahnya tidak ada. Begitu kamu mengetuk pintu, terjadi error.

Di Laravel/PHP, ini mirip `Call to a member function ... on null`.""",
        "prompt": """Di baris mana error terjadi, error apa namanya, dan bagaimana cara memperbaikinya?

```java
String name = null;
System.out.println(name.length());
```""",
        "hints": [
            "`name` tidak menunjuk ke object String apa pun. Method `length()` butuh object.",
            "Tambahkan pengecekan `name != null` sebelum memanggil `length()`, atau beri nilai default `\"\"`.",
        ],
        "answer": """**Error:** `NullPointerException` pada baris `name.length()`.

**Trace:**

| Baris | Nilai `name` | Yang terjadi |
|---|---|---|
| `String name = null;` | `null` | variable menunjuk ke tidak ada object |
| `name.length();` | `null` | Java mencoba memanggil method pada object yang tidak ada → NPE |

**Perbaikan:**

```java
String name = null;
if (name != null) {
    System.out.println(name.length());
} else {
    System.out.println(0);
}
```

Atau beri nilai awal yang aman:

```java
String name = "";
System.out.println(name.length()); // 0
```

Kalau `null` memang nilai yang sah, gunakan `Optional` atau method yang null-safe, tetapi untuk pemula pengecekan `!= null` sudah cukup jelas.""",
        "traps": """- **Mengira `null` sama dengan string kosong.** `null` = tidak ada object; `""` = object String dengan panjang 0.
- **Memanggil `name.equals("x")` saat `name` null.** Lebih aman `"x".equals(name)` atau cek null dulu.
- **Mengira `System.out.println(null)` error.** `println` menerima `null` dan mencetak `null`; error terjadi saat memanggil method pada `null`.""",
        "speak": """“Name-nya null, jadi tidak ada object String. Saat kita memanggil length, Java melempar NullPointerException. Perbaikannya bisa dengan mengecek name tidak null dulu, atau memberi nilai default string kosong.”""",
    },
    {
        "id": "npe-02-array-default",
        "day": 1,
        "topic": "NullPointerException",
        "title": "NPE pada elemen array",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Array object berisi null secara default

`new String[3]` membuat array dengan **tiga slot**, tetapi setiap slot belum diisi object String. Nilai default untuk tipe object adalah `null`.

Analogi: kamu menyiapkan tiga loker kosong. Lokernya ada, tetapi di dalamnya belum ada barang.""",
        "prompt": """Apa yang terjadi saat kode ini dijalankan?

```java
String[] names = new String[3];
System.out.println(names[0].length());
```

Bagaimana cara memperbaikinya?""",
        "hints": [
            "`new String[3]` hanya membuat array-nya. Isi tiap elemen default-nya apa?",
            "Cek `names[0] != null` sebelum memanggil `length()`, atau isi array dengan string.",
        ],
        "answer": """**Error:** `NullPointerException` pada `names[0].length()`.

**Trace:**

| Langkah | Nilai | Catatan |
|---|---|---|
| `new String[3]` | `[null, null, null]` | tiga slot, isinya belum diisi |
| `names[0]` | `null` | elemen pertama masih null |
| `names[0].length()` | — | memanggil method pada null → NPE |

**Perbaikan:**

```java
String[] names = new String[3];
names[0] = "John";

if (names[0] != null) {
    System.out.println(names[0].length());
}
```

Atau isi seluruh array sejak awal:

```java
String[] names = {"John", "Jane", "Joe"};
```

Perhatikan: `names.length` adalah panjang array (3) dan aman. Yang error adalah `names[0].length()` karena elemennya null.""",
        "traps": """- **Mengira array yang baru dibuat otomatis berisi string kosong.** Untuk `String[]`, default-nya `null`.
- **Mengira `names.length` dan `names[0].length()` sama.** Yang pertama panjang array; yang kedua panjang string di elemen pertama.
- **Lupa mengecek elemen, bukan hanya array-nya.** `names` tidak null, tetapi `names[0]` bisa null.""",
        "speak": """“Array-nya dibuat dengan tiga slot, tapi isinya masih null. Jadi saat kita mengambil names[0] lalu memanggil length, itu null.length dan terjadi NullPointerException. Solusinya isi dulu elemennya atau cek null sebelum memanggil method.”""",
    },
    {
        "id": "npe-03-object-field",
        "day": 1,
        "topic": "NullPointerException",
        "title": "NPE pada field object",
        "kind": "open",
        "origin": "latihan",
        "points": 5,
        "concept": """### Object ada, field-nya belum tentu ada isinya

`new User()` membuat object `User`, tetapi field `String email` di dalamnya belum diisi. Field object default-nya `null`.

Ini berbeda dari variable lokal: variable lokal wajib diinisialisasi sebelum dipakai (kalau tidak, compile error), sedangkan field object otomatis diberi nilai default (`null` untuk object, `0` untuk angka, `false` untuk boolean).

**Analogi:** seperti membeli lemari baru; lemarinya ada, tetapi rak di dalamnya belum tentu sudah diisi.
""",
        "prompt": """Apa yang terjadi pada kode berikut?

```java
class User {
    String email;
}

public class Main {
    public static void main(String[] args) {
        User user = new User();
        System.out.println(user.email.length());
    }
}
```

Apa penyebabnya dan bagaimana cara memperbaikinya?""",
        "hints": [
            "`user` tidak null karena sudah di-`new`. Tapi apakah `user.email` sudah diisi?",
            "Beri nilai awal pada field `email`, atau cek `user.email != null` sebelum memanggil `length()`.",
        ],
        "answer": """**Error:** `NullPointerException` pada `user.email.length()`.

**Trace:**

| Langkah | Nilai | Catatan |
|---|---|---|
| `User user = new User();` | object User | object-nya ada |
| `user.email` | `null` | field String belum diisi, default null |
| `user.email.length()` | — | memanggil method pada null → NPE |

**Perbaikan paling sederhana:**

```java
class User {
    String email = "";
}
```

Atau cek sebelum dipakai:

```java
if (user.email != null) {
    System.out.println(user.email.length());
}
```

Di aplikasi nyata, lebih baik validasi input dan pastikan field wajib tidak null sejak awal. Di Laravel, ini mirip memanggil `$user->email->length()` padahal `email` null.""",
        "traps": """- **Mengira `new User()` otomatis mengisi semua field.** Tidak; field object default-nya null.
- **Mengecek `user != null` saja.** Itu belum cukup; masalahnya ada di `user.email`.
- **Menganggap NPE hanya terjadi pada variable lokal.** Field object, elemen array, dan hasil method yang mengembalikan null juga bisa.""",
        "speak": """“User-nya ada karena sudah di-new, tapi field email belum diisi, jadi nilainya null. Saat kita memanggil length pada email, terjadi NullPointerException. Saya bisa memberi nilai default string kosong atau mengecek email tidak null dulu.”""",
    },
]
