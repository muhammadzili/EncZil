# 🔐 ENCZIL - File Encryption & Decryption Tool

ENCZIL adalah aplikasi desktop yang memungkinkan Anda mengenkripsi dan mendekripsi file dengan mudah menggunakan antarmuka grafis yang bersih dan modern. Proyek ini dibuat dengan Python, PyQt6, dan pustaka Cryptography untuk memberikan keamanan data yang kuat dan pengalaman pengguna yang intuitif.

## 🧩 Fitur

- Enkripsi file menggunakan AES-256 GCM (authenticated encryption)
- Dekripsi file `.enc` yang telah dienkripsi oleh aplikasi
- UI modern dan sederhana berbasis PyQt6
- Validasi input pengguna (file dan kata sandi)
- Enkripsi berbasis password dengan derivasi kunci menggunakan PBKDF2-HMAC

## 🖥️ Tampilan Aplikasi

<img src="https://vwemainzbfouvuosljie.supabase.co/storage/v1/object/sign/arsip-files/8310a489-f44e-458d-bafa-7b699dceb5ad/Screenshot%20from%202025-07-14%2016-13-55.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9mNTA1YWFlMC02NjlkLTRlMjktOGY4ZS04YjBhNTE5YjIyYjYiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJhcnNpcC1maWxlcy84MzEwYTQ4OS1mNDRlLTQ1OGQtYmFmYS03YjY5OWRjZWI1YWQvU2NyZWVuc2hvdCBmcm9tIDIwMjUtMDctMTQgMTYtMTMtNTUucG5nIiwiaWF0IjoxNzUyNDg0NDQ4LCJleHAiOjE3NTI0ODgwNDh9.x4m0nOF2GVZUbYT2Tke0G3SmI2_J0GbnmY1qPfMHZo0" alt="ENCZIL Screenshot" width="500"/>

## ⚙️ Instalasi

1. **Clone repositori:**

```bash
git clone https://github.com/muhammadzili/EncZil.git
cd EncZil
```

2. **Instal dependensi:**

```bash
pip install -r requirements.txt
```

## 🚀 Menjalankan Aplikasi

```bash
python main.py
```

## 🧪 Struktur File

```
enczil/
├── main.py              # File utama aplikasi GUI
├── requirements.txt     # Daftar dependensi
└── README.md            # Dokumentasi ini
```

## 🔒 Cara Kerja Enkripsi

- Enkripsi menggunakan algoritma **AES-256 GCM**
- Kata sandi pengguna diubah menjadi kunci dengan **PBKDF2-HMAC-SHA256**
- File output mencakup: `salt + IV + tag + ciphertext`
- Mode GCM memberikan integritas dan otentikasi data

## ⚠️ Catatan

- Jangan lupa kata sandi Anda. Tanpa itu, file tidak dapat didekripsi!
- File hasil enkripsi akan memiliki ekstensi `.enc`
- Pastikan file `.enc` berasal dari aplikasi ini agar kompatibel saat didekripsi

## 📦 Dependensi

- [PyQt6](https://pypi.org/project/PyQt6/)
- [cryptography](https://pypi.org/project/cryptography/)

Semua dependensi tercantum di `requirements.txt`.

## 👨‍💻 Kontributor

- Muhammad Zili – [mzili.my.id](https://mzili.my.id)

## 📄 Lisensi

MIT License – bebas digunakan dan dimodifikasi dengan atribusi.

---

**Selamat mengenkripsi data dengan aman!**
