import os
import subprocess
import json
import requests
from pathlib import Path

CONFIG_PATH = Path("config/settings.json")
LOG_PATH_DEFAULT = "/home/data/cowrie/var/log/cowrie"
SSH_CONFIG_PATH = "/etc/ssh/sshd_config"
COWRIE_CFG = "/home/data/cowrie/cowrie.cfg"
WHITELIST_PATH = Path("lists/whitelist.txt")
BLACKLIST_PATH = Path("lists/blacklist.txt")

BANNER = """
=======================
 Hardenshell Setup 🛡️
=======================
"""

def create_user():
    print("[+] Creating new user 'data' (if not exists)...")
    subprocess.run(["sudo", "useradd", "-m", "data"], stderr=subprocess.DEVNULL)
    subprocess.run([
        "sudo", "apt", "install", "git", "python3-venv", "libssl-dev", "libffi-dev", "build-essential",
        "libpython3-dev", "libxslt1-dev", "zlib1g-dev", "libyaml-dev", "libcap2-bin", "libevent-dev",
        "libpcre3-dev", "libsqlite3-dev", "libjpeg-dev", "libpq-dev", "libxml2-dev", "libldap2-dev",
        "libsasl2-dev", "libmysqlclient-dev", "libmariadb-dev", "libpcap-dev", "-y"
    ])
    print("[+] Installing Cowrie under /home/data/cowrie...")
    subprocess.run([
        "sudo", "-u", "data", "bash", "-c",
        "cd ~ && git clone https://github.com/cowrie/cowrie.git && cd cowrie && "
        "cp cowrie.cfg.dist cowrie.cfg && python3 -m venv cowrie-env && "
        "source cowrie-env/bin/activate && pip install --upgrade pip && "
        "pip install -r requirements.txt"
    ], shell=True)

def setup_config():
    print("\n[+] Let’s configure Telegram integration and Hardenshell settings:")

    token = input("[*] Enter your Telegram Bot Token: ").strip()
    chat_id = input("[*] Enter your Telegram Chat ID (group or user): ").strip()
    print("[*] To find your Telegram user ID, message https://t.me/userinfobot")
    auth_id = input("[*] Enter your Authorized Telegram User ID: ").strip()
    ports = input("[*] Enter ports to monitor (comma-separated, default 22,2222): ").strip()
    threshold = input("[*] Threshold for blocking IPs (default 5): ").strip()
    log_path = input(f"[*] Cowrie JSON log directory [default: {LOG_PATH_DEFAULT}]: ").strip()

    ports = [int(p.strip()) for p in ports.split(",") if p.strip()] if ports else [22, 2222]
    threshold = int(threshold) if threshold else 5
    log_path = log_path if log_path else LOG_PATH_DEFAULT

    config = {
        "telegram_token": token,
        "telegram_chat_id": chat_id,
        "authorized_ids": [auth_id],
        "monitored_ports": ports,
        "threshold": threshold,
        "log_path": log_path
    }

    os.makedirs("config", exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print("\n📄 Configuration saved to config/settings.json")

    # Create whitelist and blacklist files
    os.makedirs("lists", exist_ok=True)
    if not WHITELIST_PATH.exists():
        WHITELIST_PATH.write_text("# Add IPs to whitelist here (one per line)\n")
    if not BLACKLIST_PATH.exists():
        BLACKLIST_PATH.write_text("# Add IPs to blacklist here (one per line)\n")

    print("[+] Whitelist and blacklist initialized in lists/")
    test_telegram_bot(token, chat_id)

def test_telegram_bot(token, chat_id):
    print("[+] Sending test message to verify bot works...")
    msg = "✅ Hardenshell bot successfully configured and is operational."
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        res = requests.post(url, data={"chat_id": chat_id, "text": msg})
        if res.status_code == 200:
            print("[+] Telegram bot is working!")
        else:
            print("[-] Telegram bot test failed. Response:", res.text)
    except Exception as e:
        print("[-] Error sending test message:", str(e))

def install_dependencies():
    print("[+] Installing all required dependencies...")
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run([
        "sudo", "apt", "install", "python3", "python3-pip", "python3-venv",
        "iptables", "ipset", "curl", "wget", "jq", "git", "-y"
    ])
    subprocess.run([
        "pip3", "install", "python-telegram-bot", "requests", "python-whois"
    ])
    print("[+] All dependencies installed successfully.")

def main():
    print(BANNER)
    print("1. Create a new user 'data' and install Cowrie honeypot")
    print("2. Configure Hardenshell (Telegram, ports, etc.)")
    print("3. Test Telegram Bot Status")
    print("4. Harden SSH and change SSH port to 9999")
    print("5. Restore SSH config to default")
    print("6. Configure Cowrie log rotation")
    print("7. Install all required dependencies")
    print("8. Exit")

    while True:
        try:
            choice = input("\nEnter choice [1-8]: ").strip()
            if choice == "1":
                create_user()
            elif choice == "2":
                setup_config()
            elif choice == "3":
                if not CONFIG_PATH.exists():
                    print("[-] config/settings.json not found. Please run option 2 first.")
                else:
                    with open(CONFIG_PATH, "r") as f:
                        cfg = json.load(f)
                        test_telegram_bot(cfg['telegram_token'], cfg['telegram_chat_id'])
            elif choice == "4":
                print("[*] SSH hardening feature moved to CLI engine. Run: python3 main.py --harden-ssh")
            elif choice == "5":
                print("[*] SSH restore moved to CLI engine. Run: python3 main.py --restore-ssh")
            elif choice == "6":
                print("[*] Cowrie config moved to CLI engine. Run: python3 main.py --setup-cowrie")
            elif choice == "7":
                install_dependencies()
            elif choice == "8":
                print("[+] Exiting Hardenshell Setup. Goodbye!")
                break
            else:
                print("[-] Invalid choice.")
        except KeyboardInterrupt:
            print("\n[!] Use option 8 to exit gracefully. Press again to force quit.")

if __name__ == "__main__":
    main()
