# Python Easy challenges for Belajar Lagi
# Each test: {"args": [pos_args...], "expected": <value>}
# User's function is named `solve` and called as solve(*args).
# Solutions must live in the backend, never in the frontend source.

CHALLENGES = [
    {
        "slug": "largest-number",
        "title": "Find Largest Number",
        "language": "python",
        "difficulty": "easy",
        "topic": "list",
        "statement": (
            "Buat fungsi `solve(numbers)` yang menerima sebuah list angka "
            "dan mengembalikan angka terbesarnya.\n\n"
            "Contoh:\n"
            "```\n"
            "solve([10, 5, 20, 8]) -> 20\n"
            "```"
        ),
        "starter_code": "def solve(numbers):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Mulai dengan menganggap elemen pertama adalah yang terbesar, lalu bandingkan satu per satu.",
        "hint2": "Gunakan variabel `max_so_far` dan loop `for n in numbers`. Alternatif cepat: `max(numbers)`.",
        "test_json": '{"tests": [{"args": [[10, 5, 20, 8]], "expected": 20}, {"args": [[-10, -20]], "expected": -10}, {"args": [[5]], "expected": 5}, {"args": [[5, 5, 5]], "expected": 5}]}',
    },
    {
        "slug": "sum-list",
        "title": "Sum of List",
        "language": "python",
        "difficulty": "easy",
        "topic": "list",
        "statement": (
            "Buat fungsi `solve(numbers)` yang mengembalikan jumlah semua elemen list.\n\n"
            "Contoh:\n"
            "```\n"
            "solve([1, 2, 3]) -> 6\n"
            "```"
        ),
        "starter_code": "def solve(numbers):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Mulai `result = 0`, lalu tambahkan setiap elemen.",
        "hint2": "Ada fungsi bawaan `sum(numbers)` — tapi coba pahami loop manualnya dulu.",
        "test_json": '{"tests": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}, {"args": [[7]], "expected": 7}, {"args": [[-5, 5]], "expected": 0}]}',
    },
    {
        "slug": "is-even",
        "title": "Is It Even?",
        "language": "python",
        "difficulty": "easy",
        "topic": "operators",
        "statement": (
            "Buat fungsi `solve(n)` yang mengembalikan `True` jika `n` genap, "
            "dan `False` jika ganjil.\n\n"
            "Contoh:\n"
            "```\n"
            "solve(4) -> True\n"
            "solve(7) -> False\n"
            "```"
        ),
        "starter_code": "def solve(n):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Angka genap habis dibagi 2. Operator apa yang menjawab 'habis dibagi'?",
        "hint2": "Gunakan modulus `%`: `n % 2 == 0`.",
        "test_json": '{"tests": [{"args": [4], "expected": true}, {"args": [7], "expected": false}, {"args": [0], "expected": true}, {"args": [-3], "expected": false}, {"args": [100], "expected": true}]}',
    },
    {
        "slug": "reverse-string",
        "title": "Reverse String",
        "language": "python",
        "difficulty": "easy",
        "topic": "string",
        "statement": (
            "Buat fungsi `solve(text)` yang mengembalikan string secara terbalik.\n\n"
            "Contoh:\n"
            "```\n"
            "solve(\"hello\") -> \"olleh\"\n"
            "```"
        ),
        "starter_code": "def solve(text):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "String di Python bisa di-slice. Bagaimana membalik urutan slice?",
        "hint2": "Gunakan slice dengan step negatif: `text[::-1]`.",
        "test_json": '{"tests": [{"args": ["hello"], "expected": "olleh"}, {"args": ["a"], "expected": "a"}, {"args": [""], "expected": ""}, {"args": ["12345"], "expected": "54321"}]}',
    },
    {
        "slug": "count-chars",
        "title": "Count Characters",
        "language": "python",
        "difficulty": "easy",
        "topic": "dict",
        "statement": (
            "Buat fungsi `solve(text)` yang mengembalikan dictionary berisi "
            "jumlah kemunculan setiap karakter.\n\n"
            "Contoh:\n"
            "```\n"
            "solve(\"aabbabc\") -> {\"a\":3, \"b\":3, \"c\":1}\n"
            "```"
        ),
        "starter_code": "def solve(text):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Gunakan dictionary untuk menyimpan count per karakter.",
        "hint2": "Loop `for c in text`, lalu `counts[c] = counts.get(c, 0) + 1`.",
        "test_json": '{"tests": [{"args": ["aabbabc"], "expected": {"a": 3, "b": 3, "c": 1}}, {"args": [""], "expected": {}}, {"args": ["xyz"], "expected": {"x": 1, "y": 1, "z": 1}}, {"args": ["aa"], "expected": {"a": 2}}]}',
    },
    {
        "slug": "fizzbuzz",
        "title": "FizzBuzz",
        "language": "python",
        "difficulty": "easy",
        "topic": "loop",
        "statement": (
            "Buat fungsi `solve(n)` yang mengembalikan list berisi hasil FizzBuzz "
            "dari 1 sampai `n`.\n\n"
            "- Kelipatan 3 -> `\"Fizz\"`\n"
            "- Kelipatan 5 -> `\"Buzz\"`\n"
            "- Kelipatan 15 -> `\"FizzBuzz\"`\n"
            "- lainnya -> angkanya sendiri\n\n"
            "Contoh:\n"
            "```\n"
            "solve(5) -> [1, 2, \"Fizz\", 4, \"Buzz\"]\n"
            "```"
        ),
        "starter_code": "def solve(n):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Mulai dengan list kosong dan loop `for i in range(1, n+1)`. Cek kelipatan 15 lebih dulu.",
        "hint2": "Pakai `%`: `i % 15 == 0`, lalu `i % 3 == 0`, lalu `i % 5 == 0`. Append hasil ke list.",
        "test_json": '{"tests": [{"args": [5], "expected": [1, 2, "Fizz", 4, "Buzz"]}, {"args": [1], "expected": [1]}, {"args": [15], "expected": [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"]}]}',
    },
    {
        "slug": "leap-year",
        "title": "Is Leap Year?",
        "language": "python",
        "difficulty": "easy",
        "topic": "conditional",
        "statement": (
            "Buat fungsi `solve(year)` yang mengembalikan `True` jika tahun kabisat, "
            "selain itu `False`.\n\n"
            "Aturan: habis dibagi 4, kecuali habis dibagi 100, kecuali habis dibagi 400.\n"
            "```\n"
            "solve(2024) -> True\n"
            "solve(1900) -> False\n"
            "```"
        ),
        "starter_code": "def solve(year):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Gunakan `%` dan gabungkan dengan `and` / `or`.",
        "hint2": "Rumus: `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`.",
        "test_json": '{"tests": [{"args": [2024], "expected": true}, {"args": [1900], "expected": false}, {"args": [2000], "expected": true}, {"args": [2023], "expected": false}, {"args": [4], "expected": true}]}',
    },
    {
        "slug": "factorial",
        "title": "Factorial",
        "language": "python",
        "difficulty": "easy",
        "topic": "loop",
        "statement": (
            "Buat fungsi `solve(n)` yang mengembalikan `n!` (factorial).\n\n"
            "Contoh:\n"
            "```\n"
            "solve(5) -> 120\n"
            "```\n"
            "Definisi: `5! = 5 x 4 x 3 x 2 x 1`, dan `0! = 1`."
        ),
        "starter_code": "def solve(n):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Mulai `result = 1`, lalu loop `for i in range(1, n+1)` kalikan terus.",
        "hint2": "`result *= i` untuk setiap `i` dari 1 sampai n.",
        "test_json": '{"tests": [{"args": [5], "expected": 120}, {"args": [0], "expected": 1}, {"args": [1], "expected": 1}, {"args": [3], "expected": 6}]}',
    },
    {
        "slug": "count-vowels",
        "title": "Count Vowels",
        "language": "python",
        "difficulty": "easy",
        "topic": "string",
        "statement": (
            "Buat fungsi `solve(text)` yang mengembalikan jumlah vokal "
            "(`a, i, u, e, o`) dalam sebuah string. Abaikan huruf besar/kecil.\n\n"
            "Contoh:\n"
            "```\n"
            "solve(\"hello\") -> 2\n"
            "```"
        ),
        "starter_code": "def solve(text):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Turunkan dengan `.lower()` lalu loop tiap karakter, cek apakah dalam set vokal.",
        "hint2": "Gunakan `vowels = set(\"aeiou\")` dan cek `if c in vowels`.",
        "test_json": '{"tests": [{"args": ["hello"], "expected": 2}, {"args": ["aeiou"], "expected": 5}, {"args": ["bcdfg"], "expected": 0}, {"args": ["HELLO"], "expected": 2}, {"args": [""], "expected": 0}]}',
    },
    {
        "slug": "second-largest",
        "title": "Second Largest",
        "language": "python",
        "difficulty": "easy",
        "topic": "list",
        "statement": (
            "Buat fungsi `solve(nums)` yang mengembalikan elemen/angka **terbesar kedua** "
            "dari sebuah list (nilai, bukan index). Jalankan dengan asumsi list punya >= 2 elemen.\n\n"
            "Contoh:\n"
            "```\n"
            "solve([3, 1, 4, 1, 5]) -> 4\n"
            "```"
        ),
        "starter_code": "def solve(nums):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Urutkan salinan list lalu ambil elemen kedua dari belakang, atau cari dua nilai terbesar dengan loop.",
        "hint2": "`sorted(nums)[-2]` (perhatikan duplikat). Atau guard dengan variabel `first` dan `second`.",
        "test_json": '{"tests": [{"args": [[3, 1, 4, 1, 5]], "expected": 4}, {"args": [[5, 5, 4]], "expected": 5}, {"args": [[1, 2]], "expected": 1}, {"args": [[10, 10, 10]], "expected": 10}]}',
    },
    {
        "slug": "binary-search",
        "title": "Binary Search",
        "language": "python",
        "difficulty": "medium",
        "topic": "search",
        "statement": (
            "Buat fungsi `solve(nums, target)` yang melakukan **binary search** pada "
            "list angka **terurut** dan mengembalikan index target, atau `-1` jika tidak ada.\n\n"
            "Contoh:\n"
            "```\n"
            "solve([1, 3, 5, 7, 9], 7) -> 3\n"
            "solve([1, 3, 5, 7, 9], 2) -> -1\n"
            "```"
        ),
        "starter_code": "def solve(nums, target):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Pakai dua penunjuk `lo` dan `hi`. Kondisi loop: `while lo <= hi`.",
        "hint2": "Hitung `mid = (lo + hi) // 2`. Jika `nums[mid] == target` kembalikan `mid`; jika lebih kecil naikkan `lo = mid + 1`, jika lebih besar turunkan `hi = mid - 1`.",
        "test_json": '{"tests": [{"args": [[1, 3, 5, 7, 9], 7], "expected": 3}, {"args": [[1, 3, 5, 7, 9], 2], "expected": -1}, {"args": [[1], 1], "expected": 0}, {"args": [[], 5], "expected": -1}, {"args": [[2, 4, 6, 8, 10, 12], 12], "expected": 5}]}',
    },
    {
        "slug": "two-sum",
        "title": "Two Sum (Index)",
        "language": "python",
        "difficulty": "medium",
        "topic": "dict",
        "statement": (
            "Buat fungsi `solve(nums, target)` yang mengembalikan list berisi dua index "
            "angka yang jumlahnya sama dengan `target`. Dijamin ada tepat satu solusi, "
            "dan angka yang sama tidak boleh dipakai dua kali.\n\n"
            "Contoh:\n"
            "```\n"
            "solve([2, 7, 11, 15], 9) -> [0, 1]\n"
            "```"
        ),
        "starter_code": "def solve(nums, target):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Lewati array sekali sambil mencatat `{angka: index}` di dictionary.",
        "hint2": "Untuk tiap `nums[i]`, cek apakah `target - nums[i]` sudah ada di dict. Jika ya, kembalikan `[d[complement], i]`.",
        "test_json": '{"tests": [{"args": [[2, 7, 11, 15], 9], "expected": [0, 1]}, {"args": [[3, 2, 4], 6], "expected": [1, 2]}, {"args": [[3, 3], 6], "expected": [0, 1]}, {"args": [[1, 2, 3, 4, 5], 8], "expected": [2, 4]}]}',
    },
    {
        "slug": "missing-number",
        "title": "Find Missing Number",
        "language": "python",
        "difficulty": "medium",
        "topic": "list",
        "statement": (
            "Buat fungsi `solve(nums)` di mana `nums` berisi `n` angka unik dari rentang "
            "`0` sampai `n` (dengan tepat satu angka hilang). Kembalikan angka yang hilang.\n\n"
            "Contoh:\n"
            "```\n"
            "solve([3, 0, 1]) -> 2\n"
            "```"
        ),
        "starter_code": "def solve(nums):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Total lengkap `0..n` = `sum(range(n+1))`. Kurangi dengan jumlah elemen yang ada.",
        "hint2": "`n = len(nums)`. Jawaban = `sum(range(n+1)) - sum(nums)`.",
        "test_json": '{"tests": [{"args": [[3, 0, 1]], "expected": 2}, {"args": [[0, 1]], "expected": 2}, {"args": [[1]], "expected": 0}, {"args": [[0, 2, 3, 4]], "expected": 1}, {"args": [[]], "expected": 0}]}',
    },
    {
        "slug": "balanced-brackets",
        "title": "Balanced Brackets",
        "language": "python",
        "difficulty": "medium",
        "topic": "data-structures",
        "statement": (
            "Buat fungsi `solve(s)` yang mengembalikan `True` jika string berisi kombinasi "
            "tanda kurung `()`, `[]`, `{}` seimbang (setiap pembuka punya penutup yang cocok "
            "dan berurutan dengan benar).\n\n"
            "Contoh:\n"
            "```\n"
            "solve(\"( {[]} )\".replace(\" \", \"\")) -> True\n"
            "solve(\"( ]\") -> False\n"
            "```"
        ),
        "starter_code": "def solve(s):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Gunakan stack (list). Taruh pembuka, pop saat ketemu penutup, dan cek kecocokan.",
        "hint2": "Buat pasangan `pairs = {\")\": \"(\", \"]\": \"[\", \"}\": \"{\"}`. Jika penutup tidak cocok dengan top stack, return False.",
        "test_json": '{"tests": [{"args": ["()"], "expected": true}, {"args": ["()[]{}"], "expected": true}, {"args": ["(]" ], "expected": false}, {"args": ["([)]"], "expected": false}, {"args": ["{[()]}"], "expected": true}, {"args": [""], "expected": true}]}',
    },
    {
        "slug": "sort-list",
        "title": "Sort List",
        "language": "python",
        "difficulty": "medium",
        "topic": "sort",
        "statement": (
            "Buat fungsi `solve(nums)` yang mengembalikan list angka urut naik "
            "**(tanpa memakai `sorted()` atau `.sort()`)**.\n\n"
            "Contoh:\n"
            "```\n"
            "solve([4, 1, 3, 2]) -> [1, 2, 3, 4]\n"
            "```"
        ),
        "starter_code": "def solve(nums):\n    # tulis kode kamu di sini\n    pass\n",
        "hint1": "Implementasi insertion sort: mulai dari index 1, pindahkan tiap elemen ke tempat yang tepat di bagian kiri.",
        "hint2": "Selagi `j >= 0 and a[j] > key`, geser `a[j+1] = a[j]`, lalu taruh `key` di posisinya.",
        "test_json": '{"tests": [{"args": [[4, 1, 3, 2]], "expected": [1, 2, 3, 4]}, {"args": [[1]], "expected": [1]}, {"args": [[5, 4, 3, 2, 1]], "expected": [1, 2, 3, 4, 5]}, {"args": [[3, 3, 1]], "expected": [1, 3, 3]}, {"args": [[]], "expected": []}]}',
    },
]
