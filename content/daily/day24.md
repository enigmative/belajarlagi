# Day 24 — Git

## Learning Objective

- Menguasai alur dasar: init, status, add, commit, push, pull
- Paham working directory, staging area, commit, branch, remote
- Membuat branch & menggabungkan (merge)
- Menangani merge conflict
- Menggunakan log & diff untuk menelusuri perubahan

---

## Theory

### Alur dasar

```bash
git init                    # mulai repository
git status                  # lihat keadaan file
git add belajar.txt          # stagging (masuk antrean commit)
git commit -m "pesan"       # simpan snapshot
git log --oneline           # riwayat commit
git diff                    # perbedaan kerja vs staged
```

### Bekerja dengan branch

```bash
git branch feature-x        # buat branch
git switch feature-x        # pindah branch
git switch main             # kembali
git merge feature-x         # gabungkan ke main
```

### Remote (GitHub dsb.)

```bash
git remote add origin <url>
git push origin main        # kirim ke remote
git pull origin main        # tarik dari remote
```

### Merge conflict

Terjadi saat dua branch mengubah baris yang sama:

```bash
<<<<<<< HEAD
perubahan di branch ini
=======
perubahan di branch lain
>>>>>>> feature-x
```

Kamu pilih yang benar, hapus penanda, lalu `add` + `commit`.

---

## Analogy

Git seperti **mesin waktu + catatan revisi dokumen**:
- `commit` = membuat titik simpan ("di sini aku bebas bereksperimen, bisa kembali lagi").
- `branch` = garis waktu paralel untuk jangan merusak yang sudah jalan.
- `merge` = menyatukan garis waktu.
- `checkout/switch` = pindah ke titik simpan lain.

---

## Examples

```bash
git init
git add .
git commit -m "feat: tambah employee CRUD"
git branch fix-email-bug
git switch fix-email-bug
# ...ubah kode...
git add app/main.py
git commit -m "fix: validasi email"
git switch main
git merge fix-email-bug
```

---

## Code

```bash
# alur harian yang disarankan
git status                     # apa yang berubah
git diff                       # apa bedanya
git add -p                     # stage sebagian (perpotongan)
git commit -m "fix: ..."       # pesan jelas, bukan "update"
git push
```

---

## Explanation

- **Working directory**: file di disk.
- **Staging area**: file yang siap di-commit.
- **Commit**: snapshot permanen di history.
- **Branch**: jalur development terpisah.
- **Remote**: salinan repository di server.
- Commit kecil & berpesan jelas memudahkan tracing bug (git bisect, git blame).

---

## Common Mistakes

1. `commit -m` tidak diisi → not allowed / editor terbuka.
2. Pesan commit tidak deskriptif ("update", "fix").
3. Commit raksasa semua perubahan → susah di-review.
4. Merge conflict ditangani dengan menimpa asal & melempar kode orang lain.
5. Push ke main langsung tanpa test.

---

## Manual Exercises

### Exercise 1
`git init`, buat file, `add`, `commit`, lihat `log`.

### Exercise 2
Ubah file, `git diff`, stage, commit lagi.

### Exercise 3
Buat branch, ubah file, merge ke main.

### Exercise 4
Simulasi merge conflict dan selesaikan.

### Exercise 5
Pakai `git log --oneline` dan `git show <hash>` untuk menelusuri.

---

## Challenge — Minimal Exercise

Buat repository kecil, lakukan 3 commit kecil dengan pesan yang jelas, lalu buat branch fitur dan merge.

---

## Reflection

1. Apa beda working directory, staging, commit?
2. Kenapa commit kecil lebih baik?
3. Apa fungsi branch?
4. Bagaimana menangani merge conflict dengan aman?
5. Apa itu remote dan kenapa perlu push/pull?

---

## Checklist

- [ ] Bisa init/add/commit/log
- [ ] Bisa branch & merge
- [ ] Bisa selesaikan conflict
- [ ] Bisa push/pull
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 3

```bash
git switch -c feature
# edit file
git add .
git commit -m "feat: ..."
git switch main
git merge feature
```

Exercise 4

Saat conflict muncul di file: buka file, pilih baris yang benar, hapus `<<<<<<<`, `=======`, `>>>>>>>`, lalu `git add file` dan `git commit`.

</details>