This document explains how to integrate **Nmap** and **ChatGPT** with **Wazuh** for security auditing. Here’s a step-by-step breakdown:

---

## **1. Understanding the Tools**
- **Nmap (Network Mapper)**: A security scanner used to discover hosts and services on a network.
- **ChatGPT**: An AI-powered chatbot that can analyze data, summarize security findings, and provide insights.
- **Wazuh**: An open-source security platform for log analysis, vulnerability detection, and threat response.

The goal is to use **Nmap** for scanning open ports and services on endpoints, log this data into **Wazuh**, and then use **ChatGPT** to analyze security risks.

---

## **2. Infrastructure Setup**
To integrate **Nmap** and **ChatGPT** with **Wazuh**, the following infrastructure is required:
1. **Wazuh OVA 4.4.5** (pre-configured virtual machine).
2. **Ubuntu 22.04 LTS endpoint** with **Wazuh agent** installed.
3. **Windows 11 endpoint** with **Wazuh agent** installed.

Each system must have **Nmap** and the **Wazuh agent** installed to collect security data.

---

## **3. Configuration**
Wazuh’s **command monitoring module** will run **Nmap** scans periodically and capture open ports.

- **Command Monitoring Module**: This module executes predefined commands on endpoints and logs the output for analysis.

### **Nmap Integration**
A Python script is used to scan open ports on endpoints.

#### **Step 1: Python Script for Nmap Scan**
A Python script is created to:
- Scan a network subnet.
- Extract details such as **hostnames, protocols, and open ports**.
- Store the output in Wazuh logs.

```python
import nmap
import json
import platform

def scan_subnet(subnet):
    nm = nmap.PortScanner()
    nm.scan(subnet)
    results = []
    
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            if proto not in ["tcp", "udp"]:
                continue
            for port in nm[host][proto].keys():
                json_output = {
                    'nmap_host': host,
                    'nmap_protocol': proto,
                    'nmap_port': port,
                    'nmap_port_name': nm[host][proto][port].get('name', ""),
                    'nmap_port_state': nm[host][proto][port].get('state', ""),
                    'nmap_port_service': nm[host][proto][port].get('product', "") + " " + nm[host][proto][port].get('version', "")
                }
                results.append(json_output)
    return results
```
- The script scans `127.0.0.1` (loopback address) by default.
- Results are appended to **Wazuh’s active response log**.

#### **Step 2: Configure Nmap Scan on Ubuntu**
1. **Install necessary dependencies:**
   ```bash
   sudo apt-get update && sudo apt-get install python3 python3-pip
   sudo apt-get install nmap
   sudo pip3 install python-nmap
   ```

2. **Save the Python script as `nmapscan.py`** in `~/Documents/`.

3. **Edit Wazuh agent configuration** (`/var/ossec/etc/ossec.conf`):
   ```xml
   <localfile>
       <log_format>full_command</log_format>
       <command>python3 /home/<USERNAME>/Documents/nmapscan.py</command>
       <frequency>604800</frequency>
   </localfile>
   ```
   - **`<USERNAME>`**: Replace with your actual user.
   - **`frequency=604800`**: Runs once per week.

4. **Restart Wazuh agent:**
   ```bash
   sudo systemctl restart wazuh-agent
   ```

#### **Step 3: Configure Nmap Scan on Windows**
1. **Install necessary dependencies:**
   - Python 3.8.7 or later.
   - Microsoft Visual C++ 2015 Redistributable.
   - Nmap v7.94 or later (ensure it's added to `PATH`).
   - Install **python-nmap**:
     ```powershell
     pip3 install python-nmap
     ```

2. **Save the Python script as `nmapscan.py`** in `C:\Users\<USERNAME>\Documents\`.

3. **Convert script to an executable:**
   ```powershell
   pip install pyinstaller
   pyinstaller -F C:\Users\<USERNAME>\Documents\nmapscan.py
   ```
   - The `nmapscan.exe` file will be in `C:\Users\<USERNAME>\dist\`.

4. **Move the `nmapscan.exe` to `C:\Users\<USERNAME>\Documents\`.**

5. **Edit Wazuh agent configuration (`ossec.conf`):**
   ```xml
   <localfile>
       <log_format>full_command</log_format>
       <command>C:\Users\<USERNAME>\Documents\nmapscan.exe</command>
       <frequency>604800</frequency>
   </localfile>
   ```

6. **Restart Wazuh agent:**
   ```powershell
   Restart-Service -Name wazuh
   ```

---

## **4. Configuring Wazuh Server Rules**
A rule is created to capture Nmap scan results in Wazuh.

1. **Add the following rule in `/var/ossec/etc/rules/local_rules.xml`:**
   ```xml
   <group name="linux,nmap">
     <rule id="100100" level="3">
       <decoded_as>json</decoded_as>
       <field name="nmap_port">\.+</field>
       <field name="nmap_port_service">\.+</field>
       <description>NMAP: Host scan. Port $(nmap_port) is open and hosting the $(nmap_port_service) service.</description>
       <options>no_full_log</options>
     </rule>
   </group>
   ```
   - **Rule ID `100100`** triggers when an open port is detected.

2. **Restart Wazuh Manager:**
   ```bash
   sudo systemctl restart wazuh-manager
   ```

### **Viewing Scan Results**
- Open **Wazuh Dashboard** → Navigate to **Security Events**.
- Alerts will be displayed for **Ubuntu** and **Windows** endpoints.

---

## **5. ChatGPT Integration**
The goal is to use **ChatGPT** to analyze Nmap scan results and provide insights.

### **Step 1: Create ChatGPT Rules in Wazuh**
1. **Add the following rule in `/var/ossec/etc/rules/local_rules.xml`:**
   ```xml
   <group name="linux,chat_gpt">
     <rule id="100101" level="5">
       <if_sid>100100</if_sid>
       <field name="nmap_port">\d+</field>
       <description>NMAP: Host scan. Port $(nmap_port) is open.</description>
     </rule>
     <rule id="100103" level="5">
       <if_sid>100100</if_sid>
       <field name="nmap_port_service">^\s$</field>
       <description>NMAP: Port $(nmap_port) is open but no service is found.</description>
     </rule>
   </group>
   ```
   - **Rule ID `100101`** triggers if an open port with a service is found.
   - **Rule ID `100103`** triggers if an open port has no detected service.

2. **Restart Wazuh Manager:**
   ```bash
   sudo systemctl restart wazuh-manager
   ```

### **Step 2: Install Python Requests Library**
   ```bash
   pip install requests
   ```

### **Step 3: Create ChatGPT Integration Script**
Save the following script as `/var/ossec/integrations/custom-chatgpt.py`:

```python
import requests
import json

def query_api(nmap_port_service, apikey):
    headers = {'Authorization': f'Bearer {apikey}', 'Content-Type': 'application/json'}
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': f'Tell me about {nmap_port_service} and its vulnerabilities.'}],
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    return response.json()
```
- This script sends **open port service details** to ChatGPT and retrieves information.

---

## **Final Thoughts**
- **Nmap scans** the network and logs data.
- **Wazuh** detects security events and triggers alerts.
- **ChatGPT** analyzes findings and provides insights.

This integration improves **threat detection** and **incident response**, making **Wazuh** more powerful for **security auditing**. 🚀
