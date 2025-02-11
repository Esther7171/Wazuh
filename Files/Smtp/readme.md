# Wazuh SMTP Configuration Guide

## Introduction
This guide explains how to configure SMTP settings in Wazuh to enable email alerts for security events. By setting up email notifications, you can receive alerts when specific rules are triggered.

1. Run this command to install the required packages. Select No configuration, if prompted about the mail server configuration type.
```
sudo apt-get update && apt-get install postfix mailutils libsasl2-2 ca-certificates libsasl2-modules
```
<div align=center>
  <img src="https://github.com/user-attachments/assets/882e4fa6-f1ed-49e7-9e06-21013b8dafda"></img>
</div>
2. Select No Configuration
3. Append these lines to the `/etc/postfix/main.cf` file to configure Postfix. Create the file if missing.
```xml
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
smtp_use_tls = yes
smtpd_relay_restrictions = permit_mynetworks, permit_sasl_authenticated, defer_unauth_destination
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

## Additional Configurations
- If you need to forward alerts to multiple email addresses, separate them with commas in the `<email_to>` field.
- Ensure the SMTP server is accessible from the Wazuh server.
- Review Wazuh logs (`/var/ossec/logs/ossec.log`) for troubleshooting email delivery issues.

## Conclusion
By configuring SMTP in Wazuh, you can receive real-time alerts via email, improving incident response and monitoring efficiency. For advanced configurations, refer to the Wazuh documentation.

---
