from telethon import TelegramClient
import asyncio, json, os, datetime, sys
from colorama import Fore, init
init(autoreset=True)

config_file = 'config.json'

def garis():
    print(Fore.CYAN + "─" * 55)

def log(msg, color=Fore.WHITE):
    waktu = datetime.datetime.now().strftime("%H:%M:%S")
    print(color + f"[{waktu}] {msg}")

async def spinner(text, duration=1):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = asyncio.get_event_loop().time() + duration
    i = 0
    while asyncio.get_event_loop().time() < end:
        sys.stdout.write(f"\r{text} {frames[i % len(frames)]} ")
        sys.stdout.flush()
        await asyncio.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()

async def countdown(sec):
    for s in range(sec, 0, -1):
        sys.stdout.write(f"\r⏳ Menunggu {s} detik sebelum putaran berikutnya... ")
        sys.stdout.flush()
        await asyncio.sleep(1)
    print()

def input_config():
    os.system("clear")
    garis()
    print(Fore.CYAN + "🚀 Telegram Auto Sender by FR")
    garis()
    api_id = int(input("Masukkan API ID: "))
    api_hash = input("Masukkan API HASH: ")
    phone = input("Masukkan Nomor Telegram (+62...): ")

    while True:
        print("Masukkan Pesan yang Mau Dikirim (akhiri dengan END):")
        lines = []
        while True:
            ln = input()
            if ln.strip().lower() == "end":
                break
            lines.append(ln)
        message = "\n".join(lines)

        print("\n--- PREVIEW ---")
        print(message)
        print("---------------")
        k = input("Pesan sudah benar? (y/n): ").lower().strip()
        if k == "y":
            break
        os.system("clear")
        garis()
        print(Fore.CYAN + "🚀 Telegram Auto Sender by FR")
        garis()

    groups_raw = input("Masukkan Link Grup (pisahkan dengan koma): ")
    groups = [g.strip() for g in groups_raw.split(",") if g.strip()]
    delay = int(input("Atur Delay antar kirim (detik): "))
    interval = int(input("Atur Interval antar putaran (detik): "))
    rounds = int(input("Atur Jumlah putaran: "))
    repeat = input("Looping terus? (y/n): ").lower().strip()

    data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "phone": phone,
        "message": message,
        "groups": groups,
        "delay": delay,
        "interval": interval,
        "rounds": rounds,
        "repeat": repeat
    }
    with open(config_file, "w") as f:
        json.dump(data, f)
    return data

def load_config():
    with open(config_file, "r") as f:
        return json.load(f)

if os.path.exists(config_file):
    garis()
    p = input("Gunakan konfigurasi sebelumnya? (y/n): ").lower().strip()
    cfg = load_config() if p == "y" else input_config()
else:
    cfg = input_config()

client = TelegramClient('fr_session', cfg["api_id"], cfg["api_hash"])

async def main():
    await client.start(cfg["phone"])
    putaran = 1
    while True:
        os.system("clear")
        garis()
        print(Fore.CYAN + f"🔥 MEMULAI PUTARAN #{putaran}")
        garis()

        for g in cfg["groups"]:
            await spinner(Fore.YELLOW + f"Mengirim ke {g}", 0.8)
            try:
                await client.send_message(g, cfg["message"])
                log(f"Pesan terkirim ke {g}", Fore.GREEN)
            except:
                log(f"Gagal mengirim ke {g}", Fore.RED)
            await asyncio.sleep(cfg["delay"])

        log(f"Selesai putaran #{putaran}", Fore.MAGENTA)
        putaran += 1

        if cfg["repeat"] != "y" and putaran > cfg["rounds"]:
            break

        await countdown(cfg["interval"])

with client:
    client.loop.run_until_complete(main())
        
