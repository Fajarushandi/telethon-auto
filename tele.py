from telethon import TelegramClient
import asyncio, json, os, datetime
from colorama import Fore, Style, init
init(autoreset=True)

config_file = 'config.json'

def garis():
    print(Fore.CYAN + "─" * 55)

def log(msg, color=Fore.WHITE):
    waktu = datetime.datetime.now().strftime("%H:%M:%S")
    print(color + f"[{waktu}] {msg}")

def input_config():
    garis()
    print(Fore.CYAN + "🌀 Telegram Auto Sender by FR")
    garis()
    api_id = int(input("Masukkan API ID: "))
    api_hash = input("Masukkan API HASH: ")
    phone = input("Masukkan Nomor Telegram (+62...): ")
    message = input("Masukkan Pesan yang Mau Dikirim: ")
    groups_input = input("Masukkan Link Grup (pisahkan dengan koma): ")
    groups = [g.strip() for g in groups_input.split(",") if g.strip()]
    delay = int(input("Atur Delay antar kirim (detik): "))
    interval = int(input("Atur Interval antar putaran (detik): "))
    rounds = int(input("Atur Jumlah putaran: "))
    repeat_choice = input("Looping terus? (y/n): ").lower().startswith('y')
    data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "phone": phone,
        "message": message,
        "groups": groups,
        "delay": delay,
        "interval": interval,
        "rounds": rounds,
        "repeat": repeat_choice
    }
    with open(config_file, "w") as f:
        json.dump(data, f, indent=2)
    return data

def load_config():
    with open(config_file, "r") as f:
        return json.load(f)

if os.path.exists(config_file):
    garis()
    pilih = input("Gunakan konfigurasi sebelumnya? (y/n): ").lower()
    if pilih == 'y':
        cfg = load_config()
    else:
        cfg = input_config()
else:
    cfg = input_config()

client = TelegramClient('fr_session', cfg["api_id"], cfg["api_hash"])
total_success = 0
total_fail = 0

async def send_one_round():
    global total_success, total_fail
    for g in cfg["groups"]:
        try:
            await client.send_message(g, cfg["message"])
            total_success += 1
            log(f"✅ Pesan terkirim ke {g}", Fore.GREEN)
            await asyncio.sleep(cfg["delay"])
        except Exception as e:
            total_fail += 1
            log(f"❌ Gagal kirim ke {g} — {e}", Fore.RED)
            await asyncio.sleep(3)

async def main():
    start_time = datetime.datetime.now()
    await client.start(cfg["phone"])
    garis()
    print(Fore.CYAN + "🚀 Login berhasil! Mulai pengiriman pesan otomatis")
    garis()
    round_no = 0
    while True:
        round_no += 1
        print(Fore.YELLOW + f"\n🔁 PUTARAN #{round_no}")
        garis()
        await send_one_round()
        log(f"🎯 Selesai putaran #{round_no}", Fore.GREEN)
        if not cfg["repeat"]:
            break
        if cfg["rounds"] and round_no >= cfg["rounds"]:
            log("Mencapai batas putaran yang ditentukan. Berhenti.", Fore.CYAN)
            break
        for remaining in range(cfg["interval"], 0, -1):
            if remaining % 60 == 0:
                menit = remaining // 60
                log(f"⏳ Menunggu {menit} menit sebelum putaran berikutnya...", Fore.BLUE)
            await asyncio.sleep(1)
    garis()
    end_time = datetime.datetime.now()
    durasi = str(end_time - start_time).split('.')[0]
    print(Fore.CYAN + f"✅ Semua proses selesai dalam {durasi}")
    print(Fore.GREEN + f"Total sukses: {total_success}")
    print(Fore.RED + f"Total gagal: {total_fail}\n")

with client:
    client.loop.run_until_complete(main())
