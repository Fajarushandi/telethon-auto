from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import JoinChannelRequest

import asyncio
import json
import os
import random
import shutil

from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

BLUE = Fore.CYAN
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE

config_file = "accounts.json"
dead_groups_file = "dead_groups.json"

def get_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 60


def garis():
    print(BLUE + "─" * get_width())


def header():
    width = get_width()
    title = " TELEGRAM AUTO SENDER — MULTI AKUN "

    print(BLUE + "═" * width)
    print(BLUE + title.center(width))
    print(BLUE + "═" * width)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def load_accounts():
    if not os.path.exists(config_file):
        return {"accounts": []}

    with open(config_file, "r") as f:
        return json.load(f)


def save_accounts(d):

    with open(config_file, "w") as f:
        json.dump(
            d,
            f,
            indent=4,
            ensure_ascii=False
        )


def load_dead_groups():

    if not os.path.exists(dead_groups_file):
        return []

    with open(dead_groups_file, "r") as f:
        return json.load(f)


def save_dead_groups(groups):

    with open(dead_groups_file, "w") as f:
        json.dump(
            groups,
            f,
            indent=4,
            ensure_ascii=False
        )
        
def log_error(text):
    with open("error.log", "a") as f:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{waktu}] {text}\n")


def tambah_akun():
    clear()
    garis()

    print(BLUE + "Tambah Akun Baru")

    garis()

    api_id = int(input("API ID: "))
    api_hash = input("API HASH: ")
    phone = input("Nomor (+62): ")

    session = f"session_{phone.replace('+','')}"

    return {
        "phone": phone,
        "api_id": api_id,
        "api_hash": api_hash,
        "session": session,
        "last_config": None
    }


def input_config():
    clear()

    garis()
    print(BLUE + "Konfigurasi Baru")
    garis()

    msg = []

    print("Pesan (END untuk selesai):")

    while True:
        t = input()

        if t.lower() == "end":
            break

        msg.append(t)

    groups = [
        g.strip()
        for g in input("Grup (pisah koma): ").split(",")
        if g.strip()
    ]

    try:
        delay = int(input("Delay: "))
    except:
        delay = 10

    try:
        interval = int(input("Interval: "))
    except:
        interval = 60

    try:
        rounds = int(input("Putaran: "))
    except:
        rounds = 1

    repeat = input("Loop? (y/n): ").lower().strip()

    return {
        "message": "\n".join(msg),
        "groups": groups,
        "delay": delay,
        "interval": interval,
        "rounds": rounds,
        "repeat": repeat
    }


def bar(cur, total):
    if not total:
        return "-" * 20

    fill = int((cur / total) * 20)

    return "#" * fill + "-" * (20 - fill)


async def worker(acc, cfg, status, done, failmap):

    client = TelegramClient(
        acc["session"],
        acc["api_id"],
        acc["api_hash"]
    )

    await client.start(acc["phone"])

    if not await client.is_user_authorized():

        status[acc["phone"]] = {
            "putaran": "-",
            "total": "-",
            "progress": "[" + "-" * 20 + "]",
            "prog": "-",
            "status": "Session logout",
            "group": "-",
            "sent": "-"
        }

        done[acc["phone"]] = True
        return

    # --- PERBAIKAN INDENTASI DIMULAI ---
    resolved = {}

    dead_groups = load_dead_groups()

    for url in cfg["groups"]:

        if url in dead_groups:

            print(f"SKIP DEAD GROUP: {url}")

            continue

        try:

            ent = await client.get_entity(url)

            resolved[ent.id] = url

        except Exception as e:

            err = str(e).lower()

            if (
                "cannot find" in err
                or "invalid" in err
                or "username not occupied" in err
            ):

                if url not in dead_groups:

                    dead_groups.append(url)

                    save_dead_groups(dead_groups)

            failmap[acc["phone"]].append(
                (url, str(e))
            )

            log_error(
                f"{acc['phone']} | {url} | {str(e)}"
            )

    groups = list(resolved.keys())

    putaran = 1
    sent = 0

    sent_cache = set()

    total_rounds = (
        cfg["rounds"]
        if cfg["repeat"] != "y"
        else "∞"
    )

    while True:

        try:

            for idx, eid in enumerate(groups):

                url = resolved[eid]

                if sent >= 100:

                    status[acc["phone"]]["status"] = (
                        "Limit tercapai"
                    )

                    done[acc["phone"]] = True

                    await client.disconnect()
                    return

                status[acc["phone"]] = {
                    "putaran": putaran,
                    "total": total_rounds,
                    "progress": (
                        f"[{bar(idx+1,len(groups))}]"
                    ),
                    "prog": f"{idx+1}/{len(groups)}",
                    "status": "Mengirim",
                    "group": url,
                    "sent": sent
                }

                final_message = cfg["message"]

                for attempt in range(3):

                    try:

                        key = f"{eid}_{putaran}"

                        if key in sent_cache:
                            continue

                        await client.send_message(
                            eid,
                            final_message,
                            parse_mode="md"
                        )

                        sent_cache.add(key)

                        sent += 1
                        break

                    except FloodWaitError as e:

                        status[acc["phone"]]["status"] = (
                            f"FloodWait {e.seconds}s"
                        )

                        await asyncio.sleep(e.seconds)

                    except Exception as e:

                        if attempt == 2:

                            failmap[acc["phone"]].append(
                                (url, str(e))
                            )

                            log_error(
                                f"{acc['phone']} | "
                                f"{url} | {str(e)}"
                            )

                        else:
                            await asyncio.sleep(2)

                delay_random = random.randint(
                    cfg["delay"],
                    cfg["delay"] + 5
                )

                for s in range(delay_random, 0, -1):

                    status[acc["phone"]]["status"] = (
                        f"Delay {s}"
                    )

                    await asyncio.sleep(1)

            if (
                cfg["repeat"] != "y"
                and putaran >= cfg["rounds"]
            ):

                done[acc["phone"]] = True

                await client.disconnect()
                return

            for s in range(cfg["interval"], 0, -1):

                status[acc["phone"]] = {
                    "putaran": putaran,
                    "total": total_rounds,
                    "progress": "[" + "-" * 20 + "]",
                    "prog": "-",
                    "status": f"Interval {s}",
                    "group": "-",
                    "sent": sent
                }

                await asyncio.sleep(1)

            putaran += 1

        except asyncio.CancelledError:

            await client.disconnect()
            raise

        except Exception as e:

            log_error(
                f"{acc['phone']} | reconnect | {str(e)}"
            )

            status[acc["phone"]] = {
                "putaran": "-",
                "total": "-",
                "progress": "[" + "-" * 20 + "]",
                "prog": "-",
                "status": "Reconnect 10s",
                "group": "-",
                "sent": sent
            }

            await asyncio.sleep(10)


async def dashboard(status, selected, done, failmap):

    try:

        while True:

            print("\033[H\033[J", end="")

            garis()

            print(BLUE + "Mode Paralel — Realtime Monitor")

            garis()

            for phone in selected:

                s = status.get(phone, {
                    "putaran": "-",
                    "total": "-",
                    "progress": "[" + "-" * 20 + "]",
                    "prog": "-",
                    "status": "Menyiapkan",
                    "group": "-",
                    "sent": "-"
                })

                status_text = s["status"]

                if "Delay" in status_text:
                    color = YELLOW

                elif "FloodWait" in status_text:
                    color = RED

                elif "Mengirim" in status_text:
                    color = GREEN

                else:
                    color = WHITE

                print(BLUE + f"┌─ {phone}")

                print(
                    f"│ Putaran : "
                    f"{YELLOW}{s['putaran']} / {s['total']}"
                )

                print(
                    f"│ Progress: "
                    f"{GREEN}{s['progress']} {s['prog']}"
                )

                print(
                    f"│ Status  : "
                    f"{color}{status_text}"
                )

                print(f"│ Grup    : {s['group']}")

                print(
                    f"│ Terkirim: "
                    f"{GREEN}{s['sent']}"
                )

                print(
                    BLUE + "└" + "─" * (get_width() - 1)
                )

            if all(done.get(p, False) for p in selected):
                break

            await asyncio.sleep(1)

    except asyncio.CancelledError:
        return


async def run_parallel(accs, data_reference):

    status = {}
    done = {}

    failmap = {
        a["phone"]: []
        for a in accs
    }

    tasks = []
    selected = []

    for acc in accs:

        if acc["last_config"] != None:

            p = input(
                f"{acc['phone']} "
                f"pakai config sebelumnya? (y/n): "
            ).lower().strip()

            cfg = (
                acc["last_config"]
                if p == "y"
                else input_config()
            )

        else:
            cfg = input_config()

        acc["last_config"] = cfg
        selected.append(acc["phone"])

    # Perbaikan: Menggunakan parameter data_reference
    save_accounts(data_reference)

    for acc in accs:

        tasks.append(
            asyncio.create_task(
                worker(
                    acc,
                    acc["last_config"],
                    status,
                    done,
                    failmap
                )
            )
        )

    tasks.append(
        asyncio.create_task(
            dashboard(
                status,
                selected,
                done,
                failmap
            )
        )
    )

    try:
        await asyncio.gather(*tasks)

    except asyncio.CancelledError:

        for t in tasks:
            t.cancel()

        raise


async def lookup_user(acc):

    user = input(
        "Masukkan username/ID/nomor: "
    ).strip()

    client = TelegramClient(
        None,
        acc["api_id"],
        acc["api_hash"]
    )

    await client.start(acc["phone"])

    try:

        ent = await client.get_entity(user)

        full = await client(
            GetFullUserRequest(ent.id)
        )

        u = full.user

        clear()

        garis()

        print(BLUE + "User Lookup")

        garis()

        print("ID        :", u.id)

        print(
            "Username  :",
            ("@" + u.username)
            if u.username
            else "-"
        )

        print("Nama      :", u.first_name or "-")
        print("Nomor     :", u.phone or "-")

        print(
            "Premium   :",
            "Ya" if u.premium else "Tidak"
        )

        print(
            "Verified  :",
            "Ya" if u.verified else "Tidak"
        )

        print(
            "Bot       :",
            "Ya" if u.bot else "Tidak"
        )

        print(
            "Scam      :",
            "Ya" if u.scam else "Tidak"
        )

        print(
            "Fake      :",
            "Ya" if u.fake else "Tidak"
        )

        print(
            "Restricted:",
            "Ya" if u.restricted else "Tidak"
        )

        print(
            "Bio       :",
            full.full_user.about or "-"
        )

        garis()

    except Exception as e:
        print("Gagal lookup:", e)

    await client.disconnect()
    input("Enter untuk kembali...")


async def join_process(accs):

    links = [
        g.strip()
        for g in input(
            "Link grup (pisah koma): "
        ).split(",")
        if g.strip()
    ]

    for acc in accs:

        client = TelegramClient(
            acc["session"],
            acc["api_id"],
            acc["api_hash"]
        )

        await client.start(acc["phone"])

        for link in links:

            try:

                if "+" in link:

                    code = link.split("+")[1]

                    await client(
                        ImportChatInviteRequest(code)
                    )

                else:

                    username = link.split("/")[-1]

                    await client(
                        JoinChannelRequest(username)
                    )

                print(
                    acc["phone"],
                    "| OK |",
                    link
                )

            except FloodWaitError as e:

                print(
                    acc["phone"],
                    "| WAIT |",
                    e.seconds
                )

                await asyncio.sleep(e.seconds)

            except Exception as e:

                print(
                    acc["phone"],
                    "| ERR |",
                    link,
                    "|",
                    e
                )

            await asyncio.sleep(60)
        
        await client.disconnect()


if __name__ == "__main__":

    data = load_accounts()

    while True:

        clear()

        header()
        garis()

        print(
            GREEN + "[1] " +
            WHITE + "Jalankan 1 akun"
        )

        print(
            GREEN + "[2] " +
            WHITE + "Jalankan semua akun"
        )

        print(
            GREEN + "[3] " +
            WHITE + "Pilih beberapa akun"
        )

        print(
            GREEN + "[4] " +
            WHITE + "Join Grup"
        )

        print(
            GREEN + "[5] " +
            WHITE + "Tambah akun"
        )

        print(
            GREEN + "[6] " +
            WHITE + "Hapus akun"
        )

        print(
            GREEN + "[7] " +
            WHITE + "User Lookup"
        )

        print(
            RED + "[0] Keluar"
        )

        garis()

        pil = input("Pilih: ").strip()

        try:

            if pil == "0":
                break

            elif pil == "5":

                data["accounts"].append(
                    tambah_akun()
                )

                save_accounts(data)

            elif pil == "6":

    for i, a in enumerate(data["accounts"]):
        print(f"{i+1}. {a['phone']}")

    pilih = input(
        "Hapus nomor (Enter untuk kembali): "
    ).strip()

    if not pilih:
        continue

    if not pilih.isdigit():
        print("Input harus angka")
        input("Enter...")
        continue

    h = int(pilih) - 1

    if h < 0 or h >= len(data["accounts"]):
        print("Akun tidak valid")
        input("Enter...")
        continue

    data["accounts"].pop(h)

    save_accounts(data)

            elif pil == "7":

    for i, a in enumerate(data["accounts"]):
        print(f"{i+1}. {a['phone']}")

    pilih = input(
        "Pilih akun (Enter untuk kembali): "
    ).strip()

    if not pilih:
        continue

    if not pilih.isdigit():
        print("Input harus angka")
        input("Enter...")
        continue

    p = int(pilih) - 1

    if p < 0 or p >= len(data["accounts"]):
        print("Akun tidak valid")
        input("Enter...")
        continue

    asyncio.run(
        lookup_user(
            data["accounts"][p]
        )
    )

            elif pil == "1":

    for i, a in enumerate(data["accounts"]):
        print(f"{i+1}. {a['phone']}")

    pilih = input(
        "Pilih akun (Enter untuk kembali): "
    ).strip()

    if not pilih:
        continue

    if not pilih.isdigit():
        print("Input harus angka")
        input("Enter...")
        continue

    p = int(pilih) - 1

    if p < 0 or p >= len(data["accounts"]):
        print("Akun tidak valid")
        input("Enter...")
        continue

    asyncio.run(
        run_parallel(
            [data["accounts"][p]],
            data
        )
    )

            elif pil == "2":

                asyncio.run(
                    run_parallel(
                        data["accounts"],
                        data
                    )
                )

            elif pil == "3":

    for i, a in enumerate(data["accounts"]):
        print(f"{i+1}. {a['phone']}")

    raw = input(
        "Pilih (pisah koma, Enter untuk kembali): "
    ).strip()

    if not raw:
        continue

    try:

        ids = [
            int(x.strip()) - 1
            for x in raw.split(",")
        ]

        sel = [
            data["accounts"][i]
            for i in ids
            if 0 <= i < len(data["accounts"])
        ]

        if not sel:
            print("Tidak ada akun valid")
            input("Enter...")
            continue

        asyncio.run(
            run_parallel(sel, data)
        )

    except:
        print("Format salah")
        input("Enter...")

            elif pil == "4":

                print("1. Join 1 akun")
                print("2. Join semua akun")

                sub = input(
    "Pilih (Enter untuk kembali): "
).strip()

if not sub:
    continue

                if sub == "1":

for i, a in enumerate(data["accounts"]):
    print(f"{i+1}. {a['phone']}")

pilih = input(
    "Pilih akun (Enter untuk kembali): "
).strip()

if not pilih:
    continue

if not pilih.isdigit():
    print("Input harus angka")
    input("Enter...")
    continue

p = int(pilih) - 1

if p < 0 or p >= len(data["accounts"]):
    print("Akun tidak valid")
    input("Enter...")
    continue

asyncio.run(
    join_process(
        [data["accounts"][p]]
    )
)

                elif sub == "2":

                    asyncio.run(
                        join_process(
                            data["accounts"]
                        )
                    )

        except KeyboardInterrupt:

            print(
                "\n" +
                RED +
                "Dihentikan oleh user.\n"
            )
