import csv
from datetime import datetime

def log_event(ip, enrich_data):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"logs/{today}.csv"
    fieldnames = ["timestamp", "ip", "country", "org", "hostname"]

    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "ip": ip,
            "country": enrich_data.get("country"),
            "org": enrich_data.get("org"),
            "hostname": enrich_data.get("hostname")
        })
