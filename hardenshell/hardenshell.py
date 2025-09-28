import json
import time
from pathlib import Path

from core.firewall import block_ip
from core.enrich import enrich_ip
from core.logger import log_event
from core.telegram_control import send_alert
from core.config import CONFIG_PATH, WHITELIST_PATH, BLACKLIST_PATH

# Load settings
with open(CONFIG_PATH) as f:
    config = json.load(f)

TELEGRAM_TOKEN = config.get("telegram_token")
TELEGRAM_CHAT_ID = config.get("telegram_chat_id")
AUTHORIZED_IDS = config.get("authorized_ids", [])
PORTS = config.get("monitored_ports", [22, 2222])
THRESHOLD = config.get("threshold", 5)
LOG_PATH = Path(config.get("log_path"))

# Track hit counts
ip_hits = {}

# Load white/blacklists
def load_list(path):
    if not path.exists():
        return set()
    return set(line.strip().split()[0] for line in path.read_text().splitlines() if line.strip() and not line.startswith("#"))

whitelist = load_list(WHITELIST_PATH)
blacklist = load_list(BLACKLIST_PATH)

# Auto-block blacklisted IPs at start
for ip in blacklist:
    block_ip(ip)

print("[+] Hardenshell started. Monitoring logs...")

# Monitor Cowrie log file in real-time
def monitor():
    with LOG_PATH.open("r") as f:
        f.seek(0, 2)  # go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            try:
                data = json.loads(line)
                if data.get("eventid") != "cowrie.login.failed":
                    continue

                src_ip = data.get("src_ip")
                if not src_ip:
                    continue

                if src_ip in whitelist:
                    continue

                if src_ip in blacklist:
                    block_ip(src_ip)
                    continue

                ip_hits[src_ip] = ip_hits.get(src_ip, 0) + 1
                if ip_hits[src_ip] >= THRESHOLD:
                    block_ip(src_ip)
                    enrich = enrich_ip(src_ip)
                    send_alert(src_ip, enrich, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
                    log_event(src_ip, enrich)
            except Exception as e:
                print("[!] Error:", e)
                continue

if __name__ == "__main__":
    monitor()
