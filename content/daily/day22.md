# Day 22 — Data Structures

## Learning Objective

- Mengimplementasikan Stack dan Queue
- Menggunakan `deque` dari `collections`
- Memahami Linked List dan Tree (konsep)
- Memilih struktur data yang tepat
- Menerapkan struktur data pada soal sederhana

---

## Theory

### Stack — LIFO (Last In, First Out)

```python
stack = []
stack.append(1)      # push
stack.append(2)
print(stack.pop())   # 2 (pop dari atas)
```

Analog: tumpukan piring — yang terakhir ditaruh, diambil duluan.

### Queue — FIFO (First In, First Out)

```python
from collections import deque

q = deque()
q.append(1)          # enqueue
q.append(2)
print(q.popleft())   # 1 (keluar dari depan)
```

Analog: antrean kasir — yang pertama datang, dilayani duluan.

### deque

```python
from collections import deque
d = deque([1, 2, 3])
d.append(4)          # tambah kanan
d.appendleft(0)      # tambah kiri
print(d)             # deque([0,1,2,3,4])
```

### Linked List (konsep)

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

a = Node(1)
b = Node(2)
a.next = b

# traversal
cur = a
while cur:
    print(cur.value)
    cur = cur.next
```

### Binary Tree (konsep)

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

root = TreeNode(10)
root.left = TreeNode(5)
root.right = TreeNode(15)
```

---

## Analogy

- Stack = tumpukan piring/surat — ambil dari atas.
- Queue = antrean — masuk belakang, keluar depan.
- Linked List = rangkaian gerbong kereta — tiap gerbong tahu gerbong berikutnya.
- Tree = struktur organisasi / folder — tiap node punya anak.

---

## Examples

### Balanced parentheses (Stack)

```python
def is_balanced(s):
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    for c in s:
        if c in "({[":
            stack.append(c)
        elif c in ")}]":
            if not stack or stack.pop() != pairs[c]:
                return False
    return not stack

print(is_balanced("({[]})"))   # True
print(is_balanced("({[})"))    # False
```

---

## Code

```python
from collections import deque

# simulasi antrian
queue = deque()
for i in range(1, 6):
    queue.append(f"orang-{i}")

while queue:
    print("melayani", queue.popleft())
```

---

## Explanation

- Stack: push/pop di ujung yang sama — pakai `list` biasa.
- Queue: push kiri, pop kanan (atau sebaliknya) — pakai `deque` (list `pop(0)` itu O(n)).
- Linked list bagus untuk insert/delete di tengah tanpa shift (bukan prioritas utama di Python — list sudah bagus).
- Tree berguna untuk data hierarkis & pencarian cepat (binary search tree).

---

## Common Mistakes

1. Memakai `list.pop(0)` untuk queue → O(n); pakai `deque.popleft()`.
2. Lupa mengecek stack kosong saat pop (exception/undefined).
3. Linked list tanpa null guard saat traversal.
4. Memakai tree untuk data yang cukup pakai list/dict.
5. Saling menukar konsep LIFO/FIFO.

---

## Manual Exercises

### Exercise 1
Implement stack untuk membalik string (push semua lalu pop).

### Exercise 2
Implement queue memakai `deque` untuk memproses antrean.

### Exercise 3
Cek string tanda kurung seimbang `()`.

### Exercise 4
Buat linked list 3 node dan cetak seluruhnya.

### Exercise 5
Buat binary tree sederhana root → 2 anak, traversal manual.

---

## Challenge — Minimal Exercise

Fungsi `solve(s)` yang mengembalikan `True` jika tanda kurung `(),[],{}` seimbang.

---

## Reflection

1. Apa beda stack dan queue?
2. Kenapa `deque` lebih baik dari list untuk queue?
3. Kapan linked list berguna?
4. Apa itu binary tree dan kapan dipakai?
5. Jelaskan LIFO vs FIFO dengan contoh sehari-hari.

---

## Checklist

- [ ] Bisa implement stack
- [ ] Bisa implement queue dengan deque
- [ ] Paham konsep linked list & tree
- [ ] Bisa cek balanced parentheses
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```python
def reverse_str(s):
    stack = []
    for c in s:
        stack.append(c)
    out = ""
    while stack:
        out += stack.pop()
    return out
```

Exercise 3

```python
def balanced(s):
    stack = []
    for c in s:
        if c == "(":
            stack.append(c)
        elif c == ")":
            if not stack:
                return False
            stack.pop()
    return not stack
```

</details>