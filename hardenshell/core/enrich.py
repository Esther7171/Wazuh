import socket
import requests

def enrich_ip(ip):
    result = {
        "ip": ip,
        "hostname": None,
        "country": None,
        "org": None
    }
    try:
        result["hostname"] = socket.gethostbyaddr(ip)[0]
    except: pass

    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        result["country"] = geo.get("country")
        result["org"] = geo.get("org")
    except: pass

    return result
