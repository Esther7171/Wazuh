## Integrating Telegram Bot with Wazuh Alerts

This guide will walk you through the process of sending Wazuh alerts directly to a Telegram bot. Let's get started!

---

## Step 1: Create Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://telegram.me/BotFather)

2. Start a chat with BotFather and create a new bot:

```bash
/newbot
```

3. Provide a name for your bot. Example:
```bash
WazuhAlertsBot
```

4. Provide a unique username ending with `_bot`. Example:
```bash
wazuh_alerts_bot
```

5. Copy the API Token provided by BotFather.

![BotFather](https://github.com/user-attachments/assets/bd4e425d-bdde-49b2-878e-67c9b1d909bd)

---

## Step 2: Create a Telegram Group and Add Your Bot

1. Create a new group in Telegram.

2. Add your bot to the group.

3. Promote the bot to admin.

4. Send a random message to the group.

![Create Group](https://github.com/user-attachments/assets/0bd3dc32-5f03-4ead-91fa-1a6ebc926ac4)

---

## Step 3: Get Your Group Chat ID

Access the following URL in your browser:

```bash
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```

Find your `chat_id` (usually starts with a `-` sign).

![Get Chat ID](https://github.com/user-attachments/assets/1d087a90-6372-44ff-9c49-afc6783a2669)

---

## Step 4: Configure Wazuh Server

### Create Bash Script

```bash
nano /var/ossec/integrations/custom-telegram
```

Add the following:

```bash
#!/bin/sh

WPYTHON_BIN="framework/python/bin/python3"

SCRIPT_PATH_NAME="$0"
DIR_NAME="$(cd $(dirname ${SCRIPT_PATH_NAME}); pwd -P)"
SCRIPT_NAME="$(basename ${SCRIPT_PATH_NAME})"

case ${DIR_NAME} in
    */active-response/bin | */wodles*)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/../..; pwd)"
        fi
        PYTHON_SCRIPT="${DIR_NAME}/${SCRIPT_NAME}.py"
    ;;
    */bin)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/..; pwd)"
        fi
        PYTHON_SCRIPT="${WAZUH_PATH}/framework/scripts/${SCRIPT_NAME}.py"
    ;;
     */integrations)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/..; pwd)"
        fi
        PYTHON_SCRIPT="${DIR_NAME}/${SCRIPT_NAME}.py"
    ;;
esac

${WAZUH_PATH}/${WPYTHON_BIN} ${PYTHON_SCRIPT} "$@"
```

---

### Create Python Script for Sending Alerts

```bash
nano /var/ossec/integrations/custom-telegram.py
```

Add the following:

```python
#!/usr/bin/env python

import sys
import json
import requests

CHAT_ID = "<Your Chat ID with - Sign>"

alert_file = open(sys.argv[1])
hook_url = sys.argv[3]

alert_json = json.loads(alert_file.read())
alert_file.close()

alert_level = alert_json.get('rule', {}).get('level', "N/A")
description = alert_json.get('rule', {}).get('description', "N/A")
agent_name = alert_json.get('agent', {}).get('name', "N/A")
agent_id = alert_json.get('agent', {}).get('id', "N/A")
agent_ip = alert_json.get('agent', {}).get('ip', "N/A")
manager_name = alert_json.get('manager', {}).get('name', "N/A")
rule_id = alert_json.get('rule', {}).get('id', "N/A")
timestamp = alert_json.get('timestamp', "N/A")

msg_text = f"""
🔔 *Wazuh Alert*
------------------------
*Agent Name:* {agent_name}
*Agent ID:* {agent_id}
*Agent IP:* {agent_ip}
*Manager:* {manager_name}
*Alert Level:* {alert_level}
*Rule ID:* {rule_id}
*Description:* {description}
*Timestamp:* {timestamp}
"""

msg_data = {
    'chat_id': CHAT_ID,
    'text': msg_text,
    'parse_mode': 'Markdown'
}

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

requests.post(hook_url, headers=headers, data=json.dumps(msg_data))

sys.exit(0)
```

---

### Set Permissions

```bash
chown root:wazuh /var/ossec/integrations/custom-telegram*
chmod 750 /var/ossec/integrations/custom-telegram*
```

---

## Step 5: Configure Wazuh Integration

Edit the configuration file:

```bash
nano /var/ossec/etc/ossec.conf
```

Add the following block:

```xml
<integration>
    <name>custom-telegram</name>
    <level>3</level>
    <hook_url>https://api.telegram.org/bot<YourAPIKey>/sendMessage</hook_url>
    <alert_format>json</alert_format>
</integration>
```

---

## Final Step: Restart Wazuh Manager

```bash
systemctl restart wazuh-manager
```
---

## Integrating Telegran bot

## SO we r going to send Wazuh Alerts on Telegram bot

Step 1. Go to telegram search for [bot father](https://telegram.me/BotFather)

Step 2. Add a bot by sending these messages:

1. Command to add a bot
```
/newbot
```

2. Type a name for your bot example like:
```
Test
```
3. Add a username and end name with _bot, example:
```
test_bot
```
4. Done your bot is ready

![image](https://github.com/user-attachments/assets/bd4e425d-bdde-49b2-878e-67c9b1d909bd)

5. copy the API Token


## Create a Group in telegram and add your bot 

![CRE GROUP](https://github.com/user-attachments/assets/0bd3dc32-5f03-4ead-91fa-1a6ebc926ac4)

Promote your bot to admin 
and send any message in group

![image](https://github.com/user-attachments/assets/f5455571-98b7-4435-a743-11d6598e7c91)

copy the bot api and get your group id
```
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```

![image](https://github.com/user-attachments/assets/1d087a90-6372-44ff-9c49-afc6783a2669)

Copy the chat id even with  `-` 

## Wazuh Server Config 
Create a bash script 
```bash
nano /var/ossec/integrations/custom-telegram
```
Add sCRIPT
```BASH
#!/bin/sh

WPYTHON_BIN="framework/python/bin/python3"

SCRIPT_PATH_NAME="$0"

DIR_NAME="$(cd $(dirname ${SCRIPT_PATH_NAME}); pwd -P)"
SCRIPT_NAME="$(basename ${SCRIPT_PATH_NAME})"

case ${DIR_NAME} in
    */active-response/bin | */wodles*)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/../..; pwd)"
        fi

        PYTHON_SCRIPT="${DIR_NAME}/${SCRIPT_NAME}.py"
    ;;
    */bin)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/..; pwd)"
        fi

        PYTHON_SCRIPT="${WAZUH_PATH}/framework/scripts/${SCRIPT_NAME}.py"
    ;;
     */integrations)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/..; pwd)"
        fi

        PYTHON_SCRIPT="${DIR_NAME}/${SCRIPT_NAME}.py"
    ;;
esac


${WAZUH_PATH}/${WPYTHON_BIN} ${PYTHON_SCRIPT} "$@"
```
Create a python file for alert
```
nano /var/ossec/integrations/custom-telegram.py
```
Add code
> Note: Past the chat id CHAT_ID=
```py
#!/usr/bin/env python

import sys
import json
import requests
from requests.auth import HTTPBasicAuth

CHAT_ID = "Here past your chat id with -"

# Read configuration parameters
alert_file = open(sys.argv[1])
hook_url = sys.argv[3]

# Read the alert file
alert_json = json.loads(alert_file.read())
alert_file.close()

# Extract fields
alert_level = alert_json.get('rule', {}).get('level', "N/A")
description = alert_json.get('rule', {}).get('description', "N/A")
agent_name = alert_json.get('agent', {}).get('name', "N/A")
agent_id = alert_json.get('agent', {}).get('id', "N/A")
agent_ip = alert_json.get('agent', {}).get('ip', "N/A")
manager_name = alert_json.get('manager', {}).get('name', "N/A")
rule_id = alert_json.get('rule', {}).get('id', "N/A")
timestamp = alert_json.get('timestamp', "N/A")

# Optional Windows Event Data
event_data = alert_json.get('data', {}).get('win', {}).get('eventdata', {})

# Prepare Message Text
msg_text = f"""
🔔 *Wazuh Alert*
------------------------
*Agent Name:* {agent_name}
*Agent ID:* {agent_id}
*Agent IP:* {agent_ip}
*Manager:* {manager_name}
*Alert Level:* {alert_level}
*Rule ID:* {rule_id}
*Description:* {description}
*Timestamp:* {timestamp}
"""

if event_data:
    msg_text += "\n*Event Data:*"
    for key, value in event_data.items():
        msg_text += f"\n- {key}: {value}"

# Prepare Request
msg_data = {
    'chat_id': CHAT_ID,
    'text': msg_text,
    'parse_mode': 'Markdown'
}

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

# Send the request
requests.post(hook_url, headers=headers, data=json.dumps(msg_data))

sys.exit(0)
```
Chnage the permission 
```
chown root:wazuh /var/ossec/integrations/custom-telegram*
chmod 750 /var/ossec/integrations/custom-telegram*
```
Add Integration to `ossec.conf`
```
nano /var/ossec/etc/ossec.conf
```
Add
```
<integration>
        <name>custom-telegram</name>
        <level>3</level>
        <hook_url>https://api.telegram.org/bot*YOUR--API---KEY*/sendMessage</hook_url>
        <alert_format>json</alert_format>
</integration>
```

And Restart Manager 
```
systemctl restart wazuh-manager
 ```
