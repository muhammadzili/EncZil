# main.py
# Aplikasi Enkripsi File "ENCZIL"
# Dibuat dengan Python, PyQt6, dan pustaka Cryptography

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox,
    QFrame
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

# Mengimpor modul yang diperlukan dari pustaka cryptography
# Ini adalah pustaka modern dan aman untuk operasi kriptografi di Python.
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag

# --- Variabel Konfigurasi Kriptografi ---
# Salt digunakan untuk melindungi dari serangan tabel pelangi saat membuat kunci dari kata sandi.
SALT_SIZE = 16
# IV (Initialization Vector) memastikan bahwa mengenkripsi data yang sama dua kali akan menghasilkan ciphertext yang berbeda.
IV_SIZE = 16
# Ukuran kunci AES (256 bit = 32 byte).
KEY_SIZE = 32
# Jumlah iterasi untuk PBKDF2. Jumlah yang lebih tinggi lebih aman tetapi lebih lambat.
PBKDF2_ITERATIONS = 390000
# Ukuran blok AES dalam byte.
AES_BLOCK_SIZE = 16


class EncZilApp(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        """Menginisialisasi dan menata antarmuka pengguna (GUI)."""
        self.setWindowTitle('ENCZIL - Enkripsi & Dekripsi File')
        self.setFixedSize(500, 350) # Ukuran jendela tetap

        # Layout utama
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # --- Judul Aplikasi ---
        title_label = QLabel('ENCZIL')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName('titleLabel')
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel('Pilih file, masukkan kata sandi, lalu enkripsi atau dekripsi.')
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setObjectName('subtitleLabel')
        main_layout.addWidget(subtitle_label)

        # --- Area Pemilihan File ---
        file_layout = QHBoxLayout()
        self.file_path_label = QLineEdit('Belum ada file yang dipilih...')
        self.file_path_label.setReadOnly(True)
        self.file_path_label.setObjectName('filePathLabel')
        
        select_button = QPushButton('Pilih File')
        select_button.clicked.connect(self.select_file)
        select_button.setObjectName('actionButton')

        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(select_button)
        main_layout.addLayout(file_layout)

        # --- Area Kata Sandi ---
        password_label = QLabel('Kata Sandi:')
        password_label.setObjectName('regularLabel')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText('Masukkan kata sandi rahasia Anda')
        self.password_input.setObjectName('passwordInput')
        
        main_layout.addWidget(password_label)
        main_layout.addWidget(self.password_input)

        # --- Garis Pemisah ---
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # --- Tombol Aksi (Enkripsi & Dekripsi) ---
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        encrypt_button = QPushButton('🔒 Enkripsi')
        encrypt_button.clicked.connect(self.process_encryption)
        encrypt_button.setObjectName('encryptButton')
        encrypt_button.setFixedHeight(40)

        decrypt_button = QPushButton('🔑 Dekripsi')
        decrypt_button.clicked.connect(self.process_decryption)
        decrypt_button.setObjectName('decryptButton')
        decrypt_button.setFixedHeight(40)

        action_layout.addWidget(encrypt_button)
        action_layout.addWidget(decrypt_button)
        main_layout.addLayout(action_layout)

        # --- Status Label ---
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName('statusLabel')
        main_layout.addWidget(self.status_label)

        # Menerapkan stylesheet untuk tampilan modern
        self.apply_stylesheet()

    def apply_stylesheet(self):
        """Menerapkan gaya (CSS) untuk membuat GUI terlihat modern."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50; /* Biru tua keabu-abuan */
                color: #ecf0f1; /* Putih pudar */
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            #titleLabel {
                font-size: 36px;
                font-weight: bold;
                color: #3498db; /* Biru cerah */
            }
            #subtitleLabel {
                color: #bdc3c7; /* Abu-abu terang */
                font-size: 12px;
            }
            #regularLabel {
                font-size: 14px;
            }
            QLineEdit {
                background-color: #34495e; /* Biru tua sedikit lebih terang */
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            #filePathLabel {
                border: 1px dashed #7f8c8d; /* Abu-abu */
                color: #95a5a6; /* Abu-abu lebih terang */
            }
            QPushButton {
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            #actionButton {
                background-color: #3498db;
                color: white;
            }
            #actionButton:hover {
                background-color: #2980b9; /* Biru lebih gelap */
            }
            #encryptButton {
                background-color: #27ae60; /* Hijau */
                color: white;
            }
            #encryptButton:hover {
                background-color: #229954; /* Hijau lebih gelap */
            }
            #decryptButton {
                background-color: #e67e22; /* Oranye */
                color: white;
            }
            #decryptButton:hover {
                background-color: #d35400; /* Oranye lebih gelap */
            }
            #statusLabel {
                color: #f1c40f; /* Kuning */
                font-style: italic;
            }
        """)

    def select_file(self):
        """Membuka dialog untuk memilih file."""
        file_dialog = QFileDialog(self)
        # Menggunakan getOpenFileName untuk memilih file yang ada.
        file, _ = file_dialog.getOpenFileName(self, "Pilih File untuk Diproses", "", "Semua File (*.*)")
        if file:
            self.file_path = file
            # Menampilkan path file yang disingkat jika terlalu panjang
            display_path = os.path.basename(file)
            self.file_path_label.setText(display_path)
            self.status_label.setText(f"File '{display_path}' dipilih.")

    def get_key_from_password(self, password, salt):
        """Membuat kunci enkripsi dari kata sandi menggunakan PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))

    def process_encryption(self):
        """Memvalidasi input dan memulai proses enkripsi."""
        if not self.file_path:
            self.show_message('Error', 'Silakan pilih file terlebih dahulu.', QMessageBox.Icon.Warning)
            return
        
        password = self.password_input.text()
        if not password:
            self.show_message('Error', 'Kata sandi tidak boleh kosong.', QMessageBox.Icon.Warning)
            return

        output_path = self.file_path + '.enc'
        
        try:
            # Baca konten file asli
            with open(self.file_path, 'rb') as f:
                plaintext = f.read()

            # Hasilkan salt dan IV yang acak dan aman secara kriptografis
            salt = os.urandom(SALT_SIZE)
            iv = os.urandom(IV_SIZE)

            # Buat kunci dari kata sandi
            key = self.get_key_from_password(password, salt)

            # Gunakan padding PKCS7 untuk memastikan data adalah kelipatan dari ukuran blok
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(plaintext) + padder.finalize()

            # Buat cipher AES dalam mode GCM (Galois/Counter Mode)
            # GCM menyediakan enkripsi terotentikasi, yang melindungi dari pemalsuan data.
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            # Enkripsi data
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            # Tulis file terenkripsi: salt + iv + tag otentikasi + ciphertext
            with open(output_path, 'wb') as f:
                f.write(salt)
                f.write(iv)
                f.write(encryptor.tag)
                f.write(ciphertext)

            self.status_label.setText(f"Enkripsi berhasil! File disimpan di {os.path.basename(output_path)}")
            self.show_message('Sukses', f'File berhasil dienkripsi dan disimpan sebagai:\n{output_path}', QMessageBox.Icon.Information)

        except Exception as e:
            self.status_label.setText(f"Error enkripsi: {e}")
            self.show_message('Error Enkripsi', f'Terjadi kesalahan: {e}', QMessageBox.Icon.Critical)

    def process_decryption(self):
        """Memvalidasi input dan memulai proses dekripsi."""
        if not self.file_path:
            self.show_message('Error', 'Silakan pilih file yang akan didekripsi.', QMessageBox.Icon.Warning)
            return
            
        if not self.file_path.endswith('.enc'):
            self.show_message('Error', 'File yang dipilih sepertinya bukan file terenkripsi (.enc).', QMessageBox.Icon.Warning)
            return

        password = self.password_input.text()
        if not password:
            self.show_message('Error', 'Kata sandi tidak boleh kosong.', QMessageBox.Icon.Warning)
            return

        # Menentukan path output dengan menghapus ekstensi .enc
        output_path, _ = os.path.splitext(self.file_path)

        try:
            with open(self.file_path, 'rb') as f:
                # Baca komponen dari file terenkripsi
                salt = f.read(SALT_SIZE)
                iv = f.read(IV_SIZE)
                # Tag GCM selalu 16 byte
                tag = f.read(16)
                ciphertext = f.read()

            # Buat kembali kunci dari kata sandi dan salt yang disimpan
            key = self.get_key_from_password(password, salt)

            # Buat cipher untuk dekripsi
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            
            # Dekripsi data. InvalidTag akan muncul di sini jika kunci/tag salah.
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            # Hapus padding untuk mendapatkan data asli
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

            # Tulis file yang telah didekripsi
            with open(output_path, 'wb') as f:
                f.write(plaintext)

            self.status_label.setText(f"Dekripsi berhasil! File disimpan di {os.path.basename(output_path)}")
            self.show_message('Sukses', f'File berhasil didekripsi dan disimpan sebagai:\n{output_path}', QMessageBox.Icon.Information)

        except InvalidTag:
            self.status_label.setText("Error: Dekripsi gagal. Kata sandi salah atau file rusak.")
            self.show_message('Error Dekripsi', 'Dekripsi gagal. Pastikan kata sandi benar dan file tidak rusak.', QMessageBox.Icon.Critical)
        except Exception as e:
            self.status_label.setText(f"Error dekripsi: {e}")
            self.show_message('Error Dekripsi', f'Terjadi kesalahan: {e}', QMessageBox.Icon.Critical)

    def show_message(self, title, message, icon):
        """Menampilkan kotak pesan popup."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Menambahkan ikon aplikasi (opsional, ganti dengan path ikon Anda jika ada)
    # app_icon = QIcon('path/to/your/icon.png')
    # app.setWindowIcon(app_icon)

    ex = EncZilApp()
    ex.show()
    sys.exit(app.exec())
