from telethon import TelegramClient
import asyncio, json, os, datetime, sys
from colorama import Fore, init
init(autoreset=True)

config_file = 'accounts.json'

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

def load_accounts():
    if not os.path.exists(config_file):
        return {"accounts": []}
    with open(config_file, "r") as f:
        return json.load(f)

def save_accounts(data):
    with open(config_file, "w") as f:
        json.dump(data, f)

def menu_pilih_akun(accounts):
    os.system("clear")
    garis()
    print(Fore.CYAN + "📱 Pilih Akun Telegram")
    garis()
    if len(accounts) == 0:
        print("Belum ada akun.")
    for i, acc in enumerate(accounts):
        print(f"{i+1}. {acc['phone']}")
    print(f"{len(accounts)+1}. Tambah akun baru")
    garis()
    return int(input("Pilih nomor: "))

def tambah_akun(acc_data):
    os.system("clear")
    garis()
    print(Fore.CYAN + "➕ Tambah Akun Baru")
    garis()
    api_id = int(input("Masukkan API ID: "))
    api_hash = input("Masukkan API HASH: ")
    phone = input("Masukkan Nomor Telegram (+62...): ")
    session_name = f"session_{phone.replace('+','')}"
    client = TelegramClient(session_name, api_id, api_hash)
    return api_id, api_hash, phone, session_name

def input_config():
    os.system("clear")
    garis()
    print(Fore.CYAN + "⚙️ Konfigurasi Baru")
    garis()
    message_lines = []
    print("Masukkan Pesan (akhiri dengan END):")
    while True:
        ln = input()
        if ln.strip().lower() == "end":
            break
        message_lines.append(ln)
    message = "\n".join(message_lines)
    groups_raw = input("Masukkan Link Grup (pisahkan koma): ")
    groups = [g.strip() for g in groups_raw.split(",") if g.strip()]
    delay = int(input("Delay antar pesan (detik): "))
    interval = int(input("Interval antar putaran (detik): "))
    rounds = int(input("Jumlah putaran: "))
    repeat = input("Loop terus? (y/n): ").lower().strip()
    return {
        "message": message,
        "groups": groups,
        "delay": delay,
        "interval": interval,
        "rounds": rounds,
        "repeat": repeat
    }

data = load_accounts()
acc_list = data["accounts"]
pil = menu_pilih_akun(acc_list)

if pil == len(acc_list) + 1:
    api_id, api_hash, phone, session_name = tambah_akun(acc_list)
    new_acc = {
        "phone": phone,
        "api_id": api_id,
        "api_hash": api_hash,
        "session": session_name,
        "last_config": None
    }
    acc_list.append(new_acc)
    save_accounts(data)
    cfg = input_config()
    new_acc["last_config"] = cfg
    save_accounts(data)
    active = new_acc
else:
    active = acc_list[pil-1]
    if active["last_config"] is not None:
        p = input("Gunakan config sebelumnya? (y/n): ").lower().strip()
        if p == "y":
            cfg = active["last_config"]
        else:
            cfg = input_config()
            active["last_config"] = cfg
            save_accounts(data)
    else:
        cfg = input_config()
        active["last_config"] = cfg
        save_accounts(data)

client = TelegramClient(active["session"], active["api_id"], active["api_hash"])

async def main():
    await client.start(active["phone"])
    putaran = 1
    total_sent = 0
    last_runtime = None
    total_rounds = cfg["rounds"] if cfg["repeat"] != "y" else "∞"

    while True:
        os.system("clear")

        if last_runtime is None:
            est_seconds = int((cfg["delay"] + 1) * len(cfg["groups"]) * 1.05)
            est_text = (datetime.datetime.now() + datetime.timedelta(seconds=est_seconds)).strftime("%H:%M:%S")
        else:
            est_text = (datetime.datetime.now() + datetime.timedelta(seconds=last_runtime)).strftime("%H:%M:%S")

        garis()
        print(Fore.CYAN + f"📱 Akun aktif : {active['phone']}")
        print(Fore.CYAN + f"🔥 Memulai Putaran {putaran}/{total_rounds}")
        print(Fore.CYAN + f"📨 Total pesan terkirim : {total_sent}")
        print(Fore.CYAN + f"⏱ Estimasi selesai putaran ini : {est_text}")
        garis()

        start_time = datetime.datetime.now()

        for g in cfg["groups"]:
            await spinner(Fore.YELLOW + f"Mengirim ke {g}", 0.7)
            try:
                wm = "✨ Powered by FR ✨"
                final_msg = cfg["message"] + "\n\n" + wm
                await client.send_message(g, final_msg)
                log(f"Pesan terkirim ke {g}", Fore.GREEN)
                total_sent += 1
            except:
                log(f"Gagal mengirim ke {g}", Fore.RED)
            await asyncio.sleep(cfg["delay"])

        end_time = datetime.datetime.now()
        last_runtime = (end_time - start_time).total_seconds()

        next_start = datetime.datetime.now() + datetime.timedelta(seconds=cfg["interval"])

        garis()
        print(Fore.MAGENTA + f"✨ Selesai putaran {putaran}/{total_rounds}")
        print(Fore.GREEN + f"📨 Terkirim sejauh ini : {total_sent}")
        print(Fore.CYAN + f"⏱ Putaran selanjutnya mulai : {next_start.strftime('%H:%M:%S')}")
        garis()

        putaran += 1
        if cfg["repeat"] != "y" and putaran > cfg["rounds"]:
            break

        await countdown(cfg["interval"])

with client:
    client.loop.run_until_complete(main())
