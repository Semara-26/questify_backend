# 🚀 Questify Backend API

Repository ini berisi *source code* backend untuk aplikasi **Questify** (Proyek UAS Pemrograman Piranti Bergerak). Dibangun menggunakan **FastAPI**, **PostgreSQL**, dan **JWT Authentication** dengan arsitektur yang berfokus pada Gamifikasi (Quests & Rewards).

**Backend Lead / Maintainer:** Kadek Semaradana

---

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Database:** PostgreSQL (via SQLAlchemy ORM)
* **Authentication:** JWT (Bcrypt Hashing)
* **Server:** Uvicorn

---

## ⚙️ Cara Setup di Komputer Lokal

Ikuti langkah-langkah di bawah ini untuk menjalankan server API secara lokal agar bisa dihubungkan ke aplikasi Flutter.

### 1. Persiapan Database (PostgreSQL)
Pastikan kamu sudah menginstal PostgreSQL dan pgAdmin 4.
* Buka pgAdmin 4.
* Buat database baru dengan nama: `questify_db`
* (*Optional*) Sesuaikan *username* dan *password* postgres kamu jika berbeda dari standar.

### 2. Clone Repository & Install Dependencies
Buka terminal dan jalankan perintah berikut secara berurutan:

```bash
# Clone repo ini
git clone [URL_GITHUB_REPO_KAMU_DISINI]
cd questify_backend

# Buat Virtual Environment (Opsional tapi sangat direkomendasikan)
python -m venv venv
venv\Scripts\activate  # Untuk pengguna Windows
# source venv/bin/activate # Untuk pengguna Mac/Linux

# Install semua library yang dibutuhkan
pip install -r requirements.txt

```

### 3. Konfigurasi Environment Variables (.env)

**⚠️ PENTING:** Aplikasi ini menggunakan sistem *fail-safe* keamanan. Server **akan crash** jika file `.env` tidak ada!

* Buat file baru bernama `.env` di folder paling luar (sejajar dengan file `main.py` atau `README.md`).
* *Copy-paste* konfigurasi di bawah ini ke dalam file `.env` tersebut:

```env
# Ganti 'postgres:postgres' dengan username & password postgresql di laptopmu
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/questify_db

# Kunci rahasia untuk enkripsi JWT
SECRET_KEY=masukkan_kunci_rahasia_bebas_disini_tanpa_spasi

```

### 4. Jalankan Server API

Setelah database siap dan file `.env` sudah dibuat, jalankan server dengan perintah:

```bash
uvicorn app.main:app --reload

```

Jika sukses, terminal akan menampilkan tulisan `Application startup complete`.

---

## 📖 Dokumentasi API (Swagger UI)

Seluruh dokumentasi *endpoint* (Routes), *schema request/response*, dan fitur *testing* API sudah otomatis di-*generate*.

Setelah server menyala, buka *browser* dan akses:
👉 **http://127.0.0.1:8000/docs**

### 💡 Catatan untuk Tim Frontend (Flutter):

* Selalu sertakan `Authorization: Bearer <token_jwt>` di *header* untuk setiap *endpoint* yang terkunci (selain *Register* dan *Login*).
* Untuk *testing* awal di Swagger UI, buat akun dummy via `POST /api/auth/register`, lalu `POST /api/auth/login` untuk mendapatkan *token*, dan masukkan *token* tersebut ke menu **Authorize** di pojok kanan atas.
