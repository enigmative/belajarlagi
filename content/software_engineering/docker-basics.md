# Docker — Image, Container, Dockerfile

## Learning Objective

- Memahami Image vs Container
- Menulis Dockerfile
- Menjalankan container (run, exec, logs, stop)
- Mengelola Environment

---

## Theory

### Image vs Container

- **Image** = template/blueprint (read-only, reusable).
- **Container** = instance hasil image yang berjalan (isolated process).

```bash
docker images            # lihat image
docker run -it python:3.11 bash
docker ps                # container berjalan
docker ps -a             # semua (termasuk stop)
docker logs <id>         # log container
docker exec -it <id> bash
docker stop <id>
docker rm <id>
```

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build & run:

```bash
docker build -t belajar-lagi .
docker run -p 8000:8000 belajar-lagi
```

---

## Analogy

Image = resep kue (tidak bisa "dimakan" langsung). Container = kue hasil memanggang mengikuti resep — kamu bisa memanggang banyak kue dari resep yang sama, masing-masing terpisah di oven (isolated). Dockerfile = urutan langkah memanggang.

---

## Examples

```dockerfile
FROM php:8.3-apache
COPY . /var/www/html/
EXPOSE 80
```

```bash
docker build -t my-php .
docker run -p 8080:80 my-php
```

---

## Code — praktik dengan layer

```dockerfile
# prioritaskan install dulu, baru COPY source → cache layer saat build
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## Explanation

- Image ber-layer; perintah di Dockerfile menggandakan cache jika tak berubah → build lebih cepat.
- `-p host:container` menghubungkan port.
- `-it` interaktif; `-d` daemon/background.
- Container tanpa data disimpan — berhenti = tahan nilai (lihat lesson volume/networking berikut).
- Gunakan image resmi & versi (mis. `python:3.11-slim`) bukan `latest`.

---

## Common Mistakes

1. Mengira container = VM penuh (padahal proses terisolasi).
2. `docker run` tanpa `--rm` → container bekas menumpuk.
3. ENV hardcode password di Dockerfile.
4. COPY seluruh repo termasuk `.git`, node_modules.
5. Jalankan container sebagai root (utamakan user non-root).

---

## Manual Exercises

### Exercise 1
Build image dari Dockerfile python sederhana.

### Exercise 2
Run + `-p` + `docker logs`.

### Exercise 3
Ganti CMD untuk menjalankan `python -c` sekali.

### Exercise 4
`docker exec -it` masuk dan jalankan perintah.

### Exercise 5
Verifikasi layer cache: ubah satu baris, build ulang — mana yang tak rerun?

---

## Challenge — Minimal Exercise

Buat Dockerfile untuk FastAPI app (`requirements.txt` + `app/`) dan run `docker build` + `docker run -p 8000:8000`.

---

## Reflection

1. Apa beda image & container?
2. Kenapa urutan perintah Dockerfile berpengaruh?
3. Apa fungsi `-p host:container`?
4. Mengapa hindari image `latest`?
5. Apa yang terjadi saat container di-stop?

---

## Checklist

- [ ] Bisa build + run container
- [ ] Bisa Dockerfile dasar
- [ ] Bisa exec/logs/stop
- - [ ] Paham image vs container
- - [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["python", "hello.py"]
```

```bash
docker build -t hello .
docker run hello
```

Exercise 5

Layer `RUN pip install` tidak rerun selama `requirements.txt` tidak berubah — hanya layer `COPY . .` yang rerun. Ubah kode, bukan requirements → pip tidak diinstall ulang.

</details>