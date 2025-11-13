<div align="center">

# 🌀 Telegram Auto Sender by FR

### 🔥 Simple • Fast • Auto Config • Multiline Support
Script otomatis kirim pesan ke banyak grup Telegram via Termux menggunakan **Telethon**.

<br>

![Telethon](https://img.shields.io/badge/Telethon-Automation-blue?style=for-the-badge)
![Termux](https://img.shields.io/badge/Termux-Supported-green?style=for-the-badge)
![Made By](https://img.shields.io/badge/Made%20By-FR-black?style=for-the-badge)

</div>

---

## 🔑 Cara Ambil API ID & API HASH (WAJIB)

Untuk menjalankan script, kamu membutuhkan API Telegram:

1. Buka: https://my.telegram.org/apps  
2. Login pakai nomor Telegram  
3. Masuk **API Development Tools**  
4. Isi data bebas → Continue  
5. Ambil:
   - **API ID**
   - **API HASH**

Masukkan saat script meminta.

---

## ⚙️ Instalasi Awal (Termux Baru)

Jalankan perintah berikut:

```bash
pkg update -y && pkg upgrade -y
pkg install git python -y
pip install --upgrade pip
```

---

## 🚀 Cara Install & Jalankan

```bash
git clone https://github.com/Fajarushandi/telethon-auto.git
cd telethon-auto
pip install -r requirements.txt
python tele.py
```

---

## 🎯 Fitur Utama

- Multiline message (akhiri dengan `END`)
- Auto looping atau sesuai jumlah putaran
- Countdown animasi di 1 baris
- UI warna premium & clean
- Kirim ke banyak grup sekaligus
- Auto save konfigurasi
- Tidak perlu edit file manual

---

## 📘 Panduan Pemula

### 📝 Cara Isi Pesan Multiline
Ketik pesan → Enter → lanjut.  
Jika selesai ketik:

```
END
```

### 🔗 Cara Isi Link Grup
Pisahkan dengan koma:

```
https://t.me/grup1, https://t.me/grup2, https://t.me/grup3
```

### ⏱ Delay antar pesan
- 3–8 detik → cepat  
- 10–20 detik → aman flood

### 🔁 Interval putaran
Contoh:
```
120 = 2 menit
```

### ♾️ Looping terus?
- `y` → jalan terus  
- `n` → berhenti sesuai jumlah putaran  

---

## ⭐ Support

Kalau script ini membantu, jangan lupa kasih **STAR** biar repo makin keren 😎🔥
