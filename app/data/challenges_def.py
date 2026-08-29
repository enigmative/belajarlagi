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
]
