# 🌀 Telegram Auto Sender by FR

Script otomatis kirim pesan ke grup Telegram via Termux menggunakan **Telethon**.  
Tidak perlu edit file — cukup jalankan dan isi konfigurasi langsung dari terminal.

---

## ⚙️ Instalasi Awal (Wajib untuk Termux Baru)

Kalau kamu baru pertama kali pakai Termux, jalankan ini dulu:

```bash
pkg update -y && pkg upgrade -y
pkg install git python -y
pip install --upgrade pip

## 🚀 Cara Jalankan
```bash
git clone https://github.com/username/telethon-auto.git
cd telethon-auto
pip install -r requirements.txt
python tele.py
