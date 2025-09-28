import requests

def send_alert(ip, enrich, token, chat_id):
    msg = f"🚨 Blocked IP: {ip}\n"
    msg += f"🌐 Country: {enrich.get('country')}\n"
    msg += f"🏢 Org: {enrich.get('org')}\n"
    msg += f"🔍 Hostname: {enrich.get('hostname')}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": msg})
