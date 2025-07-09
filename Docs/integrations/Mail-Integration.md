# SMTP Configuration Guide

## Introduction
This guide explains how to configure SMTP settings in Wazuh to enable email alerts for security events. By setting up email notifications, you can receive alerts when specific rules are triggered.

1. Run this command to install the required packages. Select No configuration, if prompted about the mail server configuration type.

```
sudo apt-get update && apt-get install postfix mailutils libsasl2-2 ca-certificates libsasl2-modules
```

<div align=center>
  <img src="https://github.com/user-attachments/assets/882e4fa6-f1ed-49e7-9e06-21013b8dafda"></img>
</div>

2. **Select No Configuration**

3. Append these lines to the `/etc/postfix/main.cf` file to configure Postfix. Create the file if missing.
```
nano /etc/postfix/main.cf
```
```xml
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
smtp_use_tls = yes
smtpd_relay_restrictions = permit_mynetworks, permit_sasl_authenticated, defer_unauth_destination
```

4. **Go to your gmail of the mail you were using and create a [app password](https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4Pv1YWpSOoP-tkrnbgDUE9W5MTey-cZBe3kp-DkJV_cK9s7eEbr4kX8OObm7LyNEdsKuGH-1tRVMoTVjIaSMYRs5fp--ojmFZRF0UDKQtR1jvEW0Ps)**

5. Set the credentials of the sender in the `/etc/postfix/sasl_passwd` file and create a database file for Postfix. Replace the <USERNAME> and <PASSWORD> variables with sender’s email address username and password respectively.

```
echo [smtp.gmail.com]:587 <USERNAME>@gmail.com:<PASSWORD> > /etc/postfix/sasl_passwd
postmap /etc/postfix/sasl_passwd
```

<div align="center">
<img src="https://github.com/user-attachments/assets/1b8b9eaa-ae32-4e7f-b372-a0cbc721226c" height=""></img>
</div>

6. Secure your password DB file so that only the root user has full read and write access to it. This is because the `/etc/postfix/sasl_passwd` and `/etc/postfix/sasl_passwd.db` files have plaintext credentials.

```
chown root:root /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
chmod 0600 /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
```

7. Restart Postfix to effect the configuration changes

```
systemctl restart postfix
```

8. Run the following command to test the configuration

```
echo "Test mail from postfix" | mail -s "Test Postfix" -r "<CONFIGURED_EMAIL>" <RECEIVER_EMAIL>
```

## Alert Management in Wazuh
Wazuh generates alerts based on predefined rules. By default, alerts are stored in:
- `/var/ossec/logs/alerts/alerts.log`
- `/var/ossec/logs/alerts/alerts.json`

To enhance monitoring, you can configure Wazuh to forward alerts via syslog, email, or external databases.

## Configuring Email Alerts
### Step 1: Update Global Email Settings
Edit the Wazuh configuration file located at `/var/ossec/etc/ossec.conf` and add the following configuration under the `<global>` section:

```xml
<ossec_config>
  <global>
    <email_notification>yes</email_notification>
    <email_to>me@test.com</email_to>
    <smtp_server>mail.test.com</smtp_server>
    <email_from>wazuh@test.com</email_from>
  </global>
</ossec_config>
```

### Step 2: Set Alert Level for Emails
Modify the `<alerts>` section in `/var/ossec/etc/ossec.conf` to set the minimum severity level for email alerts:

```xml
<ossec_config>
  <alerts>
    <email_alert_level>10</email_alert_level>
  </alerts>
</ossec_config>
```

The `<email_alert_level>` value determines the minimum alert severity required to trigger an email. The allowed range is from 1 to 16.

## Restarting Wazuh to Apply Changes
After modifying the configuration file, restart the Wazuh manager for the changes to take effect:

```sh
systemctl restart wazuh-manager
```

## Verifying Email Alerts
Once configured, Wazuh will send email notifications when an alert meets the specified threshold. Below is an example of an email notification:

```
Wazuh Notification.
2024 Apr 29 08:58:30

Received From: wazuh-server->syscheck
Rule: 553 fired (level 7) -> "File deleted."
Portion of the log(s):

File '/var/ossec/test_dir/somefile.txt' deleted
Mode: realtime

--END OF NOTIFICATION
```
# ⚡Customize your Email Alerts⚡

1. Go to:

```bash
cd /var/ossec/integrations
```

2. Create the script:

```bash
nano custom-email-alert.py
```

3. Paste the full Python code provided earlier. 
```mine
#!/usr/bin/env python3
# Authors: ester7171 and yash
# Last Updated: July 9, 2025
#
# Custom Wazuh Email Integration Script
# License: GNU GPL v2

import json
import sys
import time
import os
import smtplib
from email.utils import formataddr
from email.message import EmailMessage
from json2html import *

# Configuration
email_server = "122.160.144.106"       # SMTP server IP
email_from = "wazuhcybrotech@gmail.com"   # Sender email

# Globals
debug_enabled = False
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
log_file = f'{pwd}/logs/integrations-email.log'
now = time.strftime("%a %b %d %H:%M:%S %Z %Y")

def debug(msg):
    if debug_enabled:
        log_entry = f"{now}: {msg}\n"
        print(log_entry)
        with open(log_file, "a") as f:
            f.write(log_entry)

def send_email(recipients, subject, body):
    TO = recipients.split(',')
    em = EmailMessage()
    em['To'] = TO
    em['From'] = formataddr(('Cybrotech Teams', email_from))
    em['Subject'] = subject
    em.add_header('Content-Type', 'text/html')
    em.set_content(body, subtype='html')

    try:
        mailserver = smtplib.SMTP(email_server, 25)
        mailserver.ehlo()
        mailserver.send_message(em)
        mailserver.close()
        debug(f"Successfully sent email to {TO}")
    except Exception as e:
        debug(f"Failed to send mail to {TO}")
        debug(f"With error: {e}")

def generate_msg(alert):
    try:
        description = alert['rule']['description']
        level = alert['rule']['level']
        agentname = alert['agent']['name']
        timestamp_raw = alert['timestamp'].split('.')[0]
        timestamp = time.strftime('%c', time.strptime(timestamp_raw, '%Y-%m-%dT%H:%M:%S'))
        full_log = alert.get('full_log', '')
    except Exception as e:
        debug(f"Error extracting fields: {e}")
        sys.exit(1)

    subject = f'[Sachet Alert]: Rule level: [ {level} ], from agent: [ {agentname} ], Description: [ {description} ]'

    msg = f"""
    <html><head></head>
    <style>
        table.tabla-detail {{ max-width:800px; margin:0 auto; border-collapse:collapse; font-family:verdana; }}
        table.tabla-detail p {{ margin:0; text-align:left }}
        table.tabla-detail td {{ padding-left:.5em; border:2px solid #38414f }}
        table.tabla-detail .cabecera-tabla {{ background-color:#38414f; color:#c9cbc3; font-weight:700 }}
        table.tabla-detail .celda-detail {{ background-color:#c6d0d7 }}
        table.tabla-detail .logo-cell  {{ text-align: center }}
        table.tabla-detail .logo-image  {{ max-width: 70px; height: auto; display: block; margin: 0 auto; }}
        strong {{ color: #004a75; }}
    </style>
    <body style="font-family: Verdana">
    <table class="tabla-detail">
    <tr>
        <td class="logo-cell" colspan="2">
            <img class="logo-image" src="https://cybrotech.us/wp-content/uploads/2025/02/cropped_image.png" alt="Alert Logo">
        </td>
    </tr>
    <tr><td class="cabecera-tabla" colspan="2">Alert from Sachet</td></tr>
    <tr><td><strong>Date</strong></td><td class="celda-detail"><strong>{timestamp}</strong></td></tr>
    <tr><td><strong>Server</strong></td><td class="celda-detail"><strong>{agentname}</strong></td></tr>
    <tr><td><strong>Rule</strong></td><td class="celda-detail"><strong>{description}</strong></td></tr>
    <tr><td><strong>Severity</strong></td><td class="celda-detail"><strong>{level}</strong></td></tr>
    <tr><td><strong>Event</strong></td><td class="celda-detail"><strong>{full_log}</strong></td></tr>
    </table>
    <br><hr>
    <div>{json2html.convert(json=alert)}</div>
    </body></html>
    """
    return subject, msg

def main(args):
    debug("# Starting")

    if len(args) < 4:
        debug("# Exiting: Not enough arguments.")
        sys.exit(1)

    alert_file_location = args[1]
    recipients = args[3]

    debug("# Webhook")
    debug(recipients)

    debug("# File location")
    debug(alert_file_location)

    alerts = []
    try:
        with open(alert_file_location, encoding='utf-8', errors='replace') as alert_file:
            for line in alert_file:
                line = line.strip()
                if line:
                    try:
                        json_alert = json.loads(line)
                        alerts.append(json_alert)
                    except json.JSONDecodeError as e:
                        debug(f"Skipping malformed JSON line: {e}")
    except Exception as e:
        debug(f"# Error reading/parsing alert JSON: {e}")
        sys.exit(1)

    if not alerts:
        debug("# No valid alerts found.")
        sys.exit(0)

    for alert in alerts:
        subject, msg = generate_msg(alert)
        debug("# Sending message")
        send_email(recipients, subject, msg)

if __name__ == "__main__":
    try:
        bad_arguments = False
        if len(sys.argv) >= 4:
            debug_enabled = len(sys.argv) > 4 and sys.argv[4] == 'debug'
            msg = f'{now} {sys.argv[1]} {sys.argv[2]} {sys.argv[3]} {sys.argv[4] if len(sys.argv) > 4 else ""}'
        else:
            msg = f'{now} Wrong arguments'
            bad_arguments = True

        with open(log_file, 'a') as f:
            f.write(msg + '\n')

        if bad_arguments:
            debug("# Exiting: Bad arguments.")
            sys.exit(1)

        main(sys.argv)

    except Exception as e:
        debug(str(e))
        raise
```
```Real

#!/usr/bin/env python3 
# Copyright (C) 2015-2020, Wazuh Inc.
# October 20, 2020.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.
import json
import sys
import time
import os
import smtplib
from email.utils import formataddr
from email.message import EmailMessage
from json2html import *

email_server = "127.0.0.1" #IP of you email server
email_from = "wazuh-server@local.test" #Sender email address

# ossec.conf configuration:
#  <integration>
#      <name>custom-email-alerts</name>
#      <hook_url>emailrecipient@example.com</hook_url>
#      <level>10</level>
#      <group>multiple_drops|authentication_failures</group>
#      <alert_format>json</alert_format>
#  </integration>

# Global vars

debug_enabled = False
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
json_alert = {}
now = time.strftime("%a %b %d %H:%M:%S %Z %Y")

# Set paths
log_file = '{0}/logs/integrations-email.log'.format(pwd)


def main(args):
    """
    Main function. This will call the functions to prepare the message and send the email 
    """
    debug("# Starting")

    # Read args
    alert_file_location = args[1]
    recipients = args[3]
 
    debug("# Webhook")
    debug(recipients)

    debug("# File location")
    debug(alert_file_location)

    # Load alert. Parse JSON object.
    with open(alert_file_location) as alert_file:
        json_alert = json.load(alert_file)
    debug("# Processing alert")
    debug(json_alert)

    debug("# Generating message")
    subject, msg = generate_msg(json_alert)
    debug(msg)

    debug("# Sending message")
    send_email(recipients, subject, msg)


def send_email(recipients,subject,body):
    """
    Function to send email using an unautheticated email server.
    """
    TO = recipients.split(',')
    em = EmailMessage()
    em['To'] = TO
    # em['From'] = email_from 
    em['From'] = formataddr(('Wazuh Server', email_from))
    em['Subject'] = subject
    em.add_header('Content-Type','text/html')
    em.set_content(body, subtype='html')
    try:
        # SMTP_SSL Example
        mailserver = smtplib.SMTP(email_server, 25)
        mailserver.ehlo() # optional, called by login()
        mailserver.send_message(em)
        mailserver.close()
        debug('Successfully sent the mail to {}'.format(TO))
    except Exception as e:
        debug("Failed to send mail to {}".format(TO))
        debug("With error: {}".format(e))


def debug(msg):
    """
    Function to generate debug logs
    """
    if debug_enabled:
        msg = "{0}: {1}\n".format(now, msg)
        print(msg)
        f = open(log_file, "a")
        f.write(msg)
        f.close()


def generate_msg(alert):
    """
    Function that will provide the custom subject and body for the email.
    It takes as input a dictionary object generated from the json alert
    """
    title = alert['rule']['description'] if 'description' in alert['rule'] else ''
    description = alert['rule']['description']
    level = alert['rule']['level']
    agentname = alert['agent']['name']
    t = time.strptime(alert['timestamp'].split('.')[0],'%Y-%m-%dT%H:%M:%S')
    timestamp = time.strftime('%c',t)
    full_log = alert['full_log']
    subject = '[Wazuh Alert]: Rule level: [ {0} ], from agent: [ {1} ], Description: [ {2} ]'.format(level, agentname, description)

    msg = """
    <html><head></head>
    <style>
	table.tabla-detail {{ max-width:800px; margin:0 auto; border-collapse:collapse; padding:0; font-family:verdana; }}
	table.tabla-detail p {{ margin:0; text-align:left }}
	table.tabla-detail td {{ padding-left:.5em; border:2px solid #38414f }}
	table.tabla-detail .cabecera-tabla {{ background-color:#38414f; color:#c9cbc3; font-family:verdana; font-weight:700 }}
	table.tabla-detail .celda-detail {{ background-color:#c6d0d7 }}
	table.tabla-detail .tabla-codigo td {{ border:none }}
	table.tabla-detail .logo-cell  {{ text-align: center }}
        table.tabla-detail .logo-image  {{ max-width: 70px; height: auto; display: block; margin: 0 auto; }}
	strong {{ color: #004a75; }}
    </style>
    <body style="font-family: Verdana">
    <p>
    <table class="tabla-detail">
    <colgroup><col><col>
    </colgroup>
    <tr>
    <td class="logo-cell" colspan="2"> <img class="logo-image" src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Wazuh-Logo-2022.png" alt="Wazuh Logo"> </td>
    </tr>
    <tr class="tabla-detail">
    <td class="tabla-manual cabecera-tabla" colspan="2">Alert from Wazuh server.</td>
    </tr>
    <tr class="tabla-detail">
    <td class="tabla-manual celda-normal"><p class="Normal"><strong>Date</strong></p></td>
    <td class="tabla-manual celda-detail"><p><strong>{}</strong></p></td>
    </tr>
    <tr class="tabla-detail">
    <td><p class="Normal"><strong>Server</strong></p></td>
    <td class="tabla-manual celda-detail"><p><strong>{}</strong></p></td>
    </tr>
    <tr class="tabla-detail">
    <td><p class="Normal"><strong>Rule</strong></p></td>
    <td class="tabla-manual celda-detail"><p><strong>{}</strong></p></td>
    </tr>
    <tr class="tabla-detail">
    <td><p class="Normal"><strong>Severity</strong></p></td>
    <td class="tabla-manual celda-detail"><p><strong>{}</strong></p></td>
    </tr>
    <tr class="tabla-detail">
    <td><p class="Normal"><strong>Event</strong></p></td>
    <td class="tabla-manual celda-detail"><p><strong>{}</strong></p></td>
    </tr>
    </table>
    </body>
    </html>
    """.format(timestamp,agentname,description,level,full_log, json2html.convert(json = alert) )

    return subject, msg



if __name__ == "__main__":
    try:
        # Read arguments
        bad_arguments = False
        if len(sys.argv) >= 4:
            msg = '{0} {1} {2} {3} {4}'.format(
                now,
                sys.argv[1],
                sys.argv[2],
                sys.argv[3],
                sys.argv[4] if len(sys.argv) > 4 else '',
            )
            debug_enabled = (len(sys.argv) > 4 and sys.argv[4] == 'debug')
        else:
            msg = '{0} Wrong arguments'.format(now)
            bad_arguments = True

        # Logging the call
        f = open(log_file, 'a')
        f.write(msg + '\n')
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
4. Set permissions and ownership:

```bash
chmod 777 custom-email-alert.py
chown root:wazuh custom-email-alert.py
```

5. Install the required dependency:

```bash
pip install json2html --break-system-packages
```

6. Edit the file to customize:
```
sudo nano custom-email-alert.py
```

![image](https://github.com/user-attachments/assets/413dde07-d01c-4dbd-9659-635db57f43d1)


* `email_server` – your SMTP server IP (or hostname) [your wazuh Server Address]
* `email_from` – email configured in SMTP[mail you config form smtp to send mails.]

### Add Integration to ossec.conf

```bash
nano /var/ossec/etc/ossec.conf
```

Paste the following block under the <ossec_config> root node, preferably inside or after the <alerts> section, as shown in the screenshot below:

```xml
<integration>
  <name>custom-email-alert.py</name>
  <hook_url>receiver-mail@gmail.com</hook_url>
  <level>3</level>
  <alert_format>json</alert_format>
</integration>
```
📌 Best placement: Directly after the <alerts> block for better readability and structure, like this:

![image](https://github.com/user-attachments/assets/3388bace-3b32-4144-a883-476608e88b8b)

This ensures the integration is triggered when alerts of level 3 or higher are generated.

Restart Wazuh:

```bash
sudo systemctl restart wazuh-manager
```

### Test Manually

```bash
./var/ossec/integrations/custom-email-alert.py /var/ossec/logs/alerts/alerts.json dummy your-reciever-mail@gmail.com debug
```

---

## Additional Configurations for Custom Alert

You can further customize the alert appearance and branding:

### ✅ Change Sender Name

Edit:

```python
em['From'] = formataddr(('Deathesther Alerting', email_from))
```

Replace `'Deathesther Alerting'` with your custom name.

---

### ✅ Customize Subject Line

Edit:

```python
subject = f'[Esther Alert]: Rule level: [ {level} ], from agent: [ {agentname} ], Description: [ {description} ]'
```

You can change `[Esther Alert]` to anything else.

---

### ✅ Change Logo

Replace the logo URL in the HTML template:

```html
<img class="logo-image" src="https://yourcompany.com/logo.png" alt="Alert Logo">
```

Make sure the image is accessible via HTTPS and in `.png` or `.jpg` format.

---

## Troubleshooting

| Issue                          | Solution                                                          |
| ------------------------------ | ----------------------------------------------------------------- |
| No email received              | Check Postfix status: `systemctl status postfix`                  |
| Email sent but not received    | Check spam folder or domain restrictions                          |
| Script errors                  | Run with `debug` flag: `./custom-email-alert.py ... debug`        |
| Invalid JSON or no alerts sent | Ensure alert format is `json` and Wazuh rule level matches config |
| Missing module error           | Run `pip install json2html --break-system-packages`               |
| SMTP Timeout or Refused        | Ensure port 25/587 is open and server allows relays for your IP   |
| Wrong From address             | Match `email_from` with authenticated SMTP address                |

---


## Conclusion

By configuring SMTP in Wazuh and adding a custom integration, you can create well-formatted, branded email alerts for improved threat visibility and faster response. This setup provides full flexibility to modify sender names, logos, and subject formats to match your organizational standards.

---

### Reference

* 📄 [Wazuh Documentation - Email Alerts](https://documentation.wazuh.com/current/user-manual/manager/alert-management.html#configuring-email-alerts)


