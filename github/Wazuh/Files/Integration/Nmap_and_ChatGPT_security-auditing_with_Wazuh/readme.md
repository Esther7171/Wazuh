1. Download the Python installer from the official [Python](https://www.python.org/downloads/) website.
* Install launcher for all users (recommended).
* Add Python to PATH.

2. [Microsoft Visual C++ 2015 Redistributable](https://aka.ms/vs/16/release/vc_redist.x86.exe).

3. [Nmap](https://nmap.org/dist/nmap-7.95-setup.exe) or later Check in [website](https://nmap.org/download.html#windows). Ensure to add Nmap to PATH.

4. Open powershell as admin and Go To `Documents` and create a file nmap `nmapscan.py`
```
notepad.exe $env:USERPROFILE\Documents\nmapscan.py
```
5. Past this code
```py
#!/var/ossec/framework/python/bin/python3

import nmap
import time
import json
import platform

# The function to perform network scan on a host endpoint
def scan_subnet(subnet):
    nm = nmap.PortScanner()
    nm.scan(subnet)
    results = []

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            if proto not in ["tcp", "udp"]:
                continue

            lport = list(nm[host][proto].keys())
            lport.sort()
# Iterate over each port for the current host and protocol
            for port in lport:
                hostname = ""
                json_output = {
                    'nmap_host': host,
                    'nmap_protocol': proto,
                    'nmap_port': port,
                    'nmap_hostname': "",
                    'nmap_hostname_type': "",
                    'nmap_port_name': "",
                    'nmap_port_state': "",
                    'nmap_port_service': ""
                }
# Get the first hostname and it’s type
                if nm[host]["hostnames"]:
                    hostname = nm[host]["hostnames"][0]["name"]
                    hostname_type = nm[host]["hostnames"][0]["type"]
                    json_output['nmap_hostname'] = hostname
                    json_output['nmap_hostname_type'] = hostname_type
# Get the port name if available
                if 'name' in nm[host][proto][port]:
                    json_output['nmap_port_name'] = nm[host][proto][port]['name']
# Get the port state if available
                if 'state' in nm[host][proto][port]:
                    json_output['nmap_port_state'] = nm[host][proto][port]['state']
# Get the port service version if available
                if 'product' in nm[host][proto][port] and 'version' in nm[host][proto][port]:
                    service = nm[host][proto][port]['product'] + " " + nm[host][proto][port]['version']
                    json_output['nmap_port_service'] = service

                results.append(json_output)
    return results

# The function to append the scan results to the active response log file
def append_to_log(results, log_file):
    with open(log_file, "a") as active_response_log:
        for result in results:
            active_response_log.write(json.dumps(result))
            active_response_log.write("\n")
# Specify the address(es) to scan
subnets = ['127.0.0.1']
# path of the log file
if platform.system() == 'Windows':
    log_file = "C:\\Program Files (x86)\\ossec-agent\\active-response\\active-responses.log"
elif platform.system() == 'Linux':
    log_file = "/var/ossec/logs/active-responses.log"
else:
    log_file = "/Library/Ossec/logs/active-responses.log"

for subnet in subnets:
    results = scan_subnet(subnet)
    append_to_log(results, log_file)
    time.sleep(2)
```
6. Run the command below to install the python-nmap library and all its dependencies using Powershell:
```
pip3 install python-nmap
```
7. Convert the Nmap script to an executable application. Open an administrator PowerShell terminal and use pip to install pyinstaller:
```
pip install pyinstaller
```
8. Create the executable file using pyinstaller:
```
pyinstaller -F $env:USERPROFILE\Documents\nmapscan.py
```
9. You can find the created nmapscan.exe executable in the C:\Users\<USERNAME>\dist\ directory.
```
notepad.exe `C:\Program Files (x86)\ossec-agent\ossec.conf`
```
10. Edit the Wazuh agent C:\Program Files (x86)\ossec-agent\ossec.conf file and add the following command monitoring configuration within the <ossec_config> block:
```xml
<!-- Run nmap python script -->
  <localfile>
    <log_format>full_command</log_format>
    <command>C:\Users\<USERNAME>\Documents\nmapscan.exe</command>
    <frequency>604800</frequency>
  </localfile>
```
11. Replace <USERNAME> placeholder with the name of the user account on the endpoint.
12.  Restart the Wazuh agent using PowerShell for the changes to take effect:
```
Restart-Service -Name wazuh
```

## Wazuh Server Config

1. Add the rule below to the /var/ossec/etc/rules/local_rules.xml file:
```xml
<group name="linux,nmap,">
  <rule id="100100" level="3">
    <decoded_as>json</decoded_as>
    <field name="nmap_port">\.+</field>
    <field name="nmap_port_service">\.+</field>
      <description>NMAP: Host scan. Port $(nmap_port) is open and hosting the $(nmap_port_service) service.</description>
    <options>no_full_log</options>
  </rule>
</group>
```
Where:

* Rule ID 100100 is triggered after a successful Nmap scan on the monitored endpoint.0
  
2. Restart the Wazuh manager to apply the configuration changes:
```
sudo systemctl restart wazuh-manager
```

# Chatgpt Integration

## Wazuh Server

1. Add the below custom rule to the /var/ossec/etc/rules/local_rules.xml file.
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

Where:

Rule ID 100101 is triggered after a successful Nmap scan on the monitored endpoint with the condition that there are one or more open ports with a found service.
Rule ID 100103 is triggered after a successful Nmap scan on the monitored endpoint with the condition that there are one or more open ports without a found service.

2. Install the Python module requests. This HTTP library is necessary for the ChatGPT integration script to work with HTTP requests
```
pip install requests
```
3. Create an integration script called `/var/ossec/integrations/custom-chatgpt.py` and copy the Python script below to custom-chatgpt.py. The Python script below takes note of open ports on an endpoint and sends it to ChatGPT to get information about the open services and past vulnerabilities:
```
sudo nano /var/ossec/integrations/custom-chatgpt.py
```
4. Past this:
```py
#!/var/ossec/framework/python/bin/python3
# Copyright (C) 2015-2023, Wazuh Inc.
# ChatGPT Integration template by @WhatDoesKmean

import json
import sys
import time
import os
from socket import socket, AF_UNIX, SOCK_DGRAM

try:
    import requests
    from requests.auth import HTTPBasicAuth
except Exception as e:
    print("No module 'requests' found. Install: pip install requests")
    sys.exit(1)

# Global vars
debug_enabled = False
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

print(pwd)
#exit()

json_alert = {}
now = time.strftime("%a %b %d %H:%M:%S %Z %Y")
# Set paths
log_file = '{0}/logs/integrations.log'.format(pwd)
socket_addr = '{0}/queue/sockets/queue'.format(pwd)

def main(args):
    debug("# Starting")
    # Read args
    alert_file_location = args[1]
    apikey = args[2]
    debug("# API Key")
    debug(apikey)
    debug("# File location")
    debug(alert_file_location)

    # Load alert. Parse JSON object.
    with open(alert_file_location) as alert_file:
        json_alert = json.load(alert_file)
    debug("# Processing alert")
    debug(json_alert)

    # Request chatgpt info
    msg = request_chatgpt_info(json_alert,apikey)
    # If positive match, send event to Wazuh Manager
    if msg:
        send_event(msg, json_alert["agent"])

def debug(msg):
    if debug_enabled:
        msg = "{0}: {1}\n".format(now, msg)
    print(msg)
    f = open(log_file,"a")
    f.write(str(msg))
    f.close()


def collect(data):
  nmap_port_service = data['nmap_port_service']
  choices = data['content']
  return nmap_port_service, choices


def in_database(data, nmap_port_service):
  result = data['nmap_port_service']
  if result == 0:
    return False
  return True


def query_api(nmap_port_service, apikey):
  # Calling ChatGPT API Endpoint
  headers = {
        'Authorization': 'Bearer ' + apikey,
        'Content-Type': 'application/json',
    }

  json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': 'In 4 or 5 sentences, tell me about this service and if there are past vulnerabilities: ' + nmap_port_service,
            },
        ],
    }

  response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)

  if response.status_code == 200:
      # Create new JSON to add the port service
      ip = {"nmap_port_service": nmap_port_service}
      new_json = {}
      new_json = response.json()["choices"][0]["message"]
      new_json.update(ip)
      json_response = new_json

      data = json_response
      return data
  else:
      alert_output = {}
      alert_output["chatgpt"] = {}
      alert_output["integration"] = "custom-chatgpt"
      json_response = response.json()
      debug("# Error: The chatgpt encountered an error")
      alert_output["chatgpt"]["error"] = response.status_code
      alert_output["chatgpt"]["description"] = json_response["errors"][0]["detail"]
      send_event(alert_output)
      exit(0)


def request_chatgpt_info(alert, apikey):
    alert_output = {}
    # If there is no port service present in the alert. Exit.
    if not "nmap_port_service" in alert["data"]:
        return(0)

    # Request info using chatgpt API
    data = query_api(alert["data"]["nmap_port_service"], apikey)
    # Create alert
    alert_output["chatgpt"] = {}
    alert_output["integration"] = "custom-chatgpt"
    alert_output["chatgpt"]["found"] = 0
    alert_output["chatgpt"]["source"] = {}
    alert_output["chatgpt"]["source"]["alert_id"] = alert["id"]
    alert_output["chatgpt"]["source"]["rule"] = alert["rule"]["id"]
    alert_output["chatgpt"]["source"]["description"] = alert["rule"]["description"]
    alert_output["chatgpt"]["source"]["full_log"] = alert["full_log"]
    alert_output["chatgpt"]["source"]["nmap_port_service"] = alert["data"]["nmap_port_service"]
    nmap_port_service = alert["data"]["nmap_port_service"]

    # Check if chatgpt has any info about the nmap_port_service
    if in_database(data, nmap_port_service):
      alert_output["chatgpt"]["found"] = 1
    # Info about the port service found in chatgpt
    if alert_output["chatgpt"]["found"] == 1:
        nmap_port_service, choices = collect(data)

        # Populate JSON Output object with chatgpt request
        alert_output["chatgpt"]["nmap_port_service"] = nmap_port_service
        alert_output["chatgpt"]["choices"] = choices

        debug(alert_output)

    return(alert_output)


def send_event(msg, agent = None):
    if not agent or agent["id"] == "000":
        string = '1:chatgpt:{0}'.format(json.dumps(msg))
    else:
        string = '1:[{0}] ({1}) {2}->chatgpt:{3}'.format(agent["id"], agent["name"], agent["ip"] if "ip" in agent else "any", json.dumps(msg))

    debug(string)
    sock = socket(AF_UNIX, SOCK_DGRAM)
    sock.connect(socket_addr)
    sock.send(string.encode())
    sock.close()


if __name__ == "__main__":
    try:
        # Read arguments
        bad_arguments = False
        if len(sys.argv) >= 4:
            msg = '{0} {1} {2} {3} {4}'.format(now, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else '')
            debug_enabled = (len(sys.argv) > 4 and sys.argv[4] == 'debug')
        else:
            msg = '{0} Wrong arguments'.format(now)
            bad_arguments = True

        # Logging the call
        f = open(log_file, 'a')
        f.write(str(msg) + '\n')
        f.close()

        if bad_arguments:
            debug("# Exiting: Bad arguments.")
            sys.exit(1)

        # Main function
        main(sys.argv)

    except Exception as e:
        debug(str(e))
        raise
```
5. Grant executable permissions and modify the owner and group of the newly created Python script to belong to Wazuh:
```
chmod 750 /var/ossec/integrations/custom-chatgpt.py
chown root:wazuh /var/ossec/integrations/custom-chatgpt.py
```
6.  Edit the /var/ossec/etc/ossec.conf file and add the integration block with the content below within the <ossec_config> block:
```xml
<!-- ChatGPT Integration -->
<integration>
  <name>custom-chatgpt.py</name>
  <hook_url>https://api.openai.com/v1/chat/completions</hook_url>
  <api_key><YOUR_CHATGPT_API_KEY></api_key>
  <level>5</level>
  <rule_id>100101</rule_id>
  <alert_format>json</alert_format>
</integration>
```

The parameters used in the integration block are as follows:

`<name>` is the name of the custom script that performs the integration. All custom script names must start with custom-.
`<hook_url>` is the API URL provided by ChatGPT.
`<api_key>` is the API key. Replace <YOUR_CHATGPT_API_KEY> with your API key.
`<level>` sets a level filter so that the script does not act upon alerts below a certain level.
`<rule_id>` sets the rules that will trigger this integration. In this article, we use the rule ID 100101  to trigger the ChatGPT integration script when Nmap discovers a service with an open port.
`<alert_format>` indicates the format of the alerts. We recommend the JSON format. The script will receive the alerts in full_log format if you do not set it to JSON.
> Note: The OpenAI API is not free. However, when creating a new account, OpenAI provides you with a free trial usage for the API. You can register for a free API key at https://platform.openai.com/signup. Once your account is created:

Click on the upper-right upper user icon.
Click on View API Keys.
Click Create new secret key.
Confirm that you have free trial usage for the API at https://platform.openai.com/account/usage.
Copy the new key and save it someplace safe as you won’t be able to view the key again.

7. Add the custom rule below to the /var/ossec/etc/rules/local_rules.xml file. This rule will trigger when the port service is known and will also capture the response collected by the ChatGPT integration:
```xml
<group name="local,linux,">
  <rule id="100102" level="6">
    <field name="chatgpt.nmap_port_service">\w+</field>
      <description>The service $(chatgpt.nmap_port_service) is on an open port.</description>
  </rule>
</group>
```
8. Restart the Wazuh manager to apply the configuration changes:
```
systemctl restart wazuh-manager
```
