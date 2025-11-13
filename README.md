# 🌀 Telegram Auto Sender by FR

<div align="center">

```
████████╗███████╗██╗      ███████╗██╗  ██╗██╗  ██╗ ██████╗ 
╚══██╔══╝██╔════╝██║      ██╔════╝██║  ██║██║  ██║██╔═══██╗
   ██║   █████╗  ██║      █████╗  ███████║███████║██║   ██║
   ██║   ██╔══╝  ██║      ██╔══╝  ██╔══██║██╔══██║██║   ██║
   ██║   ███████╗███████╗ ███████╗██║  ██║██║  ██║╚██████╔╝
   ╚═╝   ╚══════╝╚══════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
```

**🔥 Telegram Auto Sender by FR 🔥**  
Simple • Fast • Auto Config • No Edit File • Multiline Support

</div>

---

Script otomatis untuk mengirim pesan ke banyak grup Telegram via Termux menggunakan **Telethon**.  
Tidak perlu edit file — semua konfigurasi diisi langsung lewat terminal seperti aplikasi.

---

## 🔑 Cara Ambil API ID & API HASH (WAJIB)

1. Buka website resmi Telegram  
   https://my.telegram.org/apps  
2. Login pakai nomor Telegram  
3. Pilih **API Development Tools**  
4. Isi data bebas → Continue  
5. Catat:
   - API ID  
   - API HASH  

Masukkan saat script meminta.

---

## ⚙️ Instalasi Awal (Untuk Termux Baru)

Jalankan perintah ini terlebih dahulu:

```bash
pkg update -y && pkg upgrade -y
pkg install git python -y
pip install --upgrade pip
```

---

## 🚀 Cara Menjalankan Script

```bash
git clone https://github.com/Fajarushandi/telethon-auto.git
cd telethon-auto
pip install -r requirements.txt
python tele.py
```

---

## 🎯 Fitur Script

- 📝 Input pesan multiline (akhiri dengan `END`)
- 🔄 Auto looping atau putaran terbatas
- ⏳ Countdown animasi hidup
- 🔥 Kirim ke banyak grup sekaligus
- 💾 Auto save konfigurasi
- 🎨 UI warna premium & bersih
- 📂 Cocok untuk pemula, tidak perlu edit file

---

## 📘 Panduan Pemula

### ✨ Cara mengisi pesan multiline
Tulis pesan → Enter → lanjut.  
Jika sudah selesai → ketik:

```
END
```

### ✨ Cara memasukkan list grup
Pisahkan dengan koma:

```
https://t.me/grup1, https://t.me/grup2, https://t.me/grup3
```

### ✨ Delay aman
- 3–8 detik → cepat  
- 10–20 detik → aman flood

### ✨ Interval putaran
Jeda antar putaran.  
Contoh:
```
120 = 2 menit
```

### ✨ Looping terus
- `y` → jalan terus  
- `n` → berhenti sesuai jumlah putaran

---

## ⭐ Support

Kalau script ini membantu, jangan lupa kasih **star** 😎🔥
