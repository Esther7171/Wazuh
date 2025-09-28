import subprocess

def block_ip(ip):
    subprocess.run(["sudo", "iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"])
    print(f"[+] IP Blocked via iptables: {ip}")
