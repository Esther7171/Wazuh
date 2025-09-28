# Windows Agent Configuration

## Steps for Configuration:

### 1. Copy `ossec.conf` for Editing
- Open the agent configuration file located at `C:\Program Files (x86)\ossec-agent`.
- Copy `ossec.conf` to another directory, make the necessary changes, and save it back.

### 2. Modify `syscheck` Block
- Locate the `<syscheck>` block in the `ossec.conf` file at `C:\Program Files (x86)\ossec-agent\ossec.conf`.
- Ensure the `<disabled>` tag is set to `no`:
  
  ```xml
  <syscheck>
    <disabled>no</disabled>
  </syscheck>
    ```
### 3. Monitor Specific Directories
- Add the following line after the`<disabled>` tag to monitor the `/Downloads` directory. Replace `username` with the actual system user:
```xml
<directories realtime="yes">C:\Users\Esther\Downloads</directories>
```
- To monitor the entire C: drive, use the following (Note: This may result in false positives, so it's recommended to exclude system files):
```xml
<directories realtime="yes">C:</directories>
```
### 4. Install Python
Download the Python installer from the [official Python website](https://www.python.org/downloads/).

Open the terminal as Administrator and install the required package:
```xml
pip install pyinstaller
```
### 5. Create Python Script
- Create a new file in Notepad and name it `remove-threat.py`.
- Add the following script to `remove-threat.py`:

```py
#!/usr/bin/python3
# Copyright (C) 2015-2022, Wazuh Inc.
# All rights reserved.

import os
import sys
import json
import datetime

if os.name == 'nt':
    LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\active-responses.log"
else:
    LOG_FILE = "/var/ossec/logs/active-responses.log"

ADD_COMMAND = 0
DELETE_COMMAND = 1
CONTINUE_COMMAND = 2
ABORT_COMMAND = 3

OS_SUCCESS = 0
OS_INVALID = -1

class message:
    def __init__(self):
        self.alert = ""
        self.command = 0

def write_debug_file(ar_name, msg):
    with open(LOG_FILE, mode="a") as log_file:
        log_file.write(str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + ar_name + ": " + msg +"\n")

def setup_and_check_message(argv):

    # get alert from stdin
    input_str = ""
    for line in sys.stdin:
        input_str = line
        break


    try:
        data = json.loads(input_str)
    except ValueError:
        write_debug_file(argv[0], 'Decoding JSON has failed, invalid input format')
        message.command = OS_INVALID
        return message

    message.alert = data

    command = data.get("command")

    if command == "add":
        message.command = ADD_COMMAND
    elif command == "delete":
        message.command = DELETE_COMMAND
    else:
        message.command = OS_INVALID
        write_debug_file(argv[0], 'Not valid command: ' + command)

    return message


def send_keys_and_check_message(argv, keys):

    # build and send message with keys
    keys_msg = json.dumps({"version": 1,"origin":{"name": argv[0],"module":"active-response"},"command":"check_keys","parameters":{"keys":keys}})

    write_debug_file(argv[0], keys_msg)

    print(keys_msg)
    sys.stdout.flush()

    # read the response of previous message
    input_str = ""
    while True:
        line = sys.stdin.readline()
        if line:
            input_str = line
            break

    # write_debug_file(argv[0], input_str)

    try:
        data = json.loads(input_str)
    except ValueError:
        write_debug_file(argv[0], 'Decoding JSON has failed, invalid input format')
        return message

    action = data.get("command")

    if "continue" == action:
        ret = CONTINUE_COMMAND
    elif "abort" == action:
        ret = ABORT_COMMAND
    else:
        ret = OS_INVALID
        write_debug_file(argv[0], "Invalid value of 'command'")

    return ret

def main(argv):

    write_debug_file(argv[0], "Started")

    # validate json and get command
    msg = setup_and_check_message(argv)

    if msg.command < 0:
        sys.exit(OS_INVALID)

    if msg.command == ADD_COMMAND:
        alert = msg.alert["parameters"]["alert"]
        keys = [alert["rule"]["id"]]
        action = send_keys_and_check_message(argv, keys)

        # if necessary, abort execution
        if action != CONTINUE_COMMAND:

            if action == ABORT_COMMAND:
                write_debug_file(argv[0], "Aborted")
                sys.exit(OS_SUCCESS)
            else:
                write_debug_file(argv[0], "Invalid command")
                sys.exit(OS_INVALID)

        try:
            file_path = msg.alert["parameters"]["alert"]["data"]["virustotal"]["source"]["file"]
            if os.path.exists(file_path):
                os.remove(file_path)
            write_debug_file(argv[0], json.dumps(msg.alert) + " Successfully removed threat")
        except OSError as error:
            write_debug_file(argv[0], json.dumps(msg.alert) + "Error removing threat")


    else:
        write_debug_file(argv[0], "Invalid command")

    write_debug_file(argv[0], "Ended")

    sys.exit(OS_SUCCESS)

if __name__ == "__main__":
    main(sys.argv)
```
### 6. Create Executable
Open the terminal without administrator rights and run the following commands to create an executable:
```py
pyinstaller -F C:\path\to\remove-threat.py
```
#### **<div align="center">OR</div>**

```py
pyinstaller -F remove-threat.py
```
### 7. Move Executable to the Agent Directory
Move the generated `remove-threat.exe` to the `C:\Program Files (x86)\ossec-agent\active-response\bin` directory.

### 8. Restart the Wazuh Agent
Restart the Wazuh agent to apply the changes either manually or using the following PowerShell command as admin:
```py
Restart-Service -Name wazuh
```
# Wazuh Server Configuration
### 1. Enable VirusTotal Integration
- Add the following configuration to the bottom of the /var/ossec/etc/ossec.conf file on the Wazuh server:
```xml
<ossec_config>
  <integration>
    <name>virustotal</name>
    <api_key><YOUR_VIRUS_TOTAL_API_KEY></api_key> <!-- Replace with your VirusTotal API key -->
    <group>syscheck</group>
    <alert_format>json</alert_format>
  </integration>
</ossec_config>
```
### 2. Configure Active Response
- Add the following blocks to enable Active Response and trigger the `remove-threat.exe` executable when a VirusTotal query returns a positive match:
```xml
<ossec_config>
  <command>
    <name>remove-threat</name>
    <executable>remove-threat.exe</executable>
    <timeout_allowed>no</timeout_allowed>
  </command>

  <active-response>
    <disabled>no</disabled>
    <command>remove-threat</command>
    <location>local</location>
    <rules_id>87105</rules_id>
  </active-response>
</ossec_config>
```
### 3. Add Custom Rules
- Add the following rules to ```/var/ossec/etc/rules/local_rules.xml``` to alert on Active Response results:
```xml
<group name="virustotal,">
  <rule id="100092" level="12">
    <if_sid>657</if_sid>
    <match>Successfully removed threat</match>
    <description>$(parameters.program) removed threat located at $(parameters.alert.data.virustotal.source.file)</description>
  </rule>

  <rule id="100093" level="12">
    <if_sid>657</if_sid>
    <match>Error removing threat</match>
    <description>Error removing threat located at $(parameters.alert.data.virustotal.source.file)</description>
  </rule>
</group>
```
### 4. Update Local Decoder
- Append the following decoder to ```/var/ossec/etc/decoders/local_decoder.xml```:
```xml
<decoder name="ar_log_fields">
    <parent>ar_log</parent>
    <regex offset="after_parent">^(\S+) Removed positive threat located in (\S+)</regex>
    <order>script_name, path</order>
</decoder>
```
### 5. Restart Wazuh Manager
- Restart the Wazuh manager to apply the configuration changes:
```xml
sudo systemctl restart wazuh-manager
```
### 6. Test Configuration
Disable the defender and download a sample virus from the [Eicar website](https://www.eicar.org/download/eicar_com-zip/?wpdmdl=8847&refresh=67646bd6c1dec1734634454) for testing.
<div align=center>
    <img src="https://github.com/user-attachments/assets/2e3fc361-22d2-43c5-a7dd-fd1e640e0f39"></src>
</div>   
