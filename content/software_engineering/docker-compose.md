# Docker — Volume, Network, Environment, Compose

## Learning Objective

- Volume untuk data persisten
- Network antar container
- Environment variable
- Docker Compose multi-service (PHP, Nginx, MySQL, Redis)

---

## Theory

### Volume

Container stateless — data hilang saat berhenti. Volume menyimpannya di host.

```bash
docker volume create data_mysql
docker run -v data_mysql:/var/lib/mysql mysql:8
docker run -v ./src:/app php:8.3-cli php index.php   # bind mount (dev)
```

### Network

Container berkomunikasi lewat network Docker.

```bash
docker network create app_net
docker run --network app_net --name db mysql:8
docker run --network app_net --name api my-api
# api bisa memanggil "db" via nama
```

### Environment

```bash
docker run -e DB_HOST=db -e DB_PASS=secret my-api
docker run --env-file .env my-api
```

---

### Docker Compose

`docker-compose.yml` mendefinisikan semua service sekaligus.

```yaml
services:
  web:
    image: nginx:1.27-alpine
    ports:
      - "8080:80"
    volumes:
      - ./public:/usr/share/nginx/html
    depends_on:
      - php

  php:
    image: php:8.3-fpm
    volumes:
      - ./public:/usr/share/nginx/html

  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: app
    volumes:
      - db_data:/var/lib/mysql

  redis:
    image: redis:7-alpine

volumes:
  db_data:
```

```bash
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
```

---

## Analogy

Volume = lemari arsip terpisah yang tetap ada meski pegawai (container) pulang. Network = lobang telepon antarkamar. Compose = satu file "rencana gedung" yang menyalakan seluruh departemen (web, PHP, DB, Redis) sekaligus.

---

## Examples — PHP + MySQL + Redis via compose

```yaml
# mencontohi belajar.txt Level 17: jalankan PHP, Nginx, MySQL, Redis
services:
  nginx: { image: nginx:1.27, ports: ["8080:80"], volumes: ["./src:/var/www/html"], depends_on: [php] }
  php:   { image: php:8.3-fpm, volumes: ["./src:/var/www/html"] }
  db:    { image: mysql:8, environment: { MYSQL_ROOT_PASSWORD: root, MYSQL_DATABASE: app }, volumes: ["db_data:/var/lib/mysql"] }
  redis: { image: redis:7-alpine }
volumes:
  db_data:
```

---

## Code — .env untuk environment

```text
# .env (bukan masuk git)
DB_HOST=db
DB_NAME=app
DB_USER=root
DB_PASS=secret
```

```yaml
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASS}
    env_file: .env
```

---

## Explanation

- Volume untuk persistence; bind mount untuk dev (sinkron file realtime).
- Compose: satu YAML = seluruh stack, bisa `up`/`down` sekali.
- Service saling panggil via nama (bukan IP).
- `env_file` dan `environment` menyuntikkan konfigurasi ke container.
- `.env` untuk rahasia — pastikan di `.gitignore`.

---

## Common Mistakes

1. Image berjalan tanpa volume → data DB hilang saat `down`.
2. Port bentrok `8080` dipakai dua service.
3. Hardcode creds di compose/`image`.
4. `depends_on` tidak menjamin DB "ready" (perlu retry/healthcheck).
5. Lupa `.gitignore` untuk `.env`.

---

## Manual Exercises

### Exercise 1
Jalankan MySQL dengan volume bernama, buat DB, `down`, cek data tetap ada.

### Exercise 2
Pisahkan dua container dengan network dan panggil lewat nama.

### Exercise 3
Compose: nginx + php-fpm menampilkan `index.php`.

### Exercise 4
Tambahkan MySQL + Redis ke compose.

### Exercise 5
Gunakan `--env-file` untuk konfigurasi.

---

## Challenge — Minimal Exercise

Susun `docker-compose.yml` dengan service `php`, `nginx`, `mysql`, `redis` sesuai contoh belajar.txt, lalu `docker compose up -d`.

---

## Reflection

1. Mengapa container butuh volume?
2. Apa beda bind mount vs named volume?
3. Bagaimana container saling terhubung?
4. Apa keuntungan compose?
5. Kenapa `.env` tidak boleh di-commit?

---

## Checklist

- [ ] Bisa volume persisten
- [ ] Bisa network antar container
- [ ] Bisa env + env-file
- [ ] Bisa compose multi-service
- [ ] Menulis Reflection di Notes

---

## Jawaban Manual Exercises

<details>
<summary>Klik untuk lihat (SETELAH mencoba sendiri)</summary>

Exercise 1

```bash
docker volume create db_data
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -v db_data:/var/lib/mysql -d mysql:8
docker exec -it mysql mysql -uroot -proot -e "CREATE DATABASE app;"
docker rm -f mysql
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -v db_data:/var/lib/mysql -d mysql:8
# database app masih ada → bukti volume persisten
```

Exercise 4

Tambahkan service `mysql` dan `redis` dengan volume untuk mysql seperti contoh utama.

</details>