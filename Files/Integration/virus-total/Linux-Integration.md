# Configuration for Ubuntu Endpoint

This guide provides the necessary steps to configure Wazuh to monitor near real-time changes in the `/root` directory of an Ubuntu endpoint. These instructions are applicable to other Linux distributions as well.

## 1. Ubuntu Endpoint Configuration

Follow these steps to configure Wazuh on the Ubuntu endpoint. This process will enable Wazuh FIM (File Integrity Monitoring) to monitor the `/root` directory and set up an active response script to remove malicious files.

### 1.1 Enable FIM Monitoring for `/root` Directory

1. Open the Wazuh agent configuration file `/var/ossec/etc/ossec.conf`.
2. Search for the `<syscheck>` block and ensure that the `<disabled>` tag is set to `no` to enable Wazuh FIM.
3. Add the following entry within the `<syscheck>` block to monitor the `/root` directory in near real-time:

   ```xml
   <directories realtime="yes">/root</directories>
   ```
- To monitor the entire C: drive, use the following (Note: This may result in false positives, so it's recommended to exclude system files):
```xml
<directories realtime="yes">/</directories>
```
### 1.2 Install `jq` Utility

`jq` is a utility that processes JSON input, which is needed for the active response script.

```bash
sudo apt update
sudo apt -y install jq
```

### 1.3 Create Active Response Script

Create a script to remove malicious files from the endpoint. Save the script as `/var/ossec/active-response/bin/remove-threat.sh`.

```bash
#!/bin/bash

LOCAL=`dirname $0`
cd $LOCAL
cd ../

PWD=`pwd`

read INPUT_JSON
FILENAME=$(echo $INPUT_JSON | jq -r .parameters.alert.data.virustotal.source.file)
COMMAND=$(echo $INPUT_JSON | jq -r .command)
LOG_FILE="${PWD}/../logs/active-responses.log"

# Analyze the command
if [ ${COMMAND} = "add" ]; then
    printf '{"version":1,"origin":{"name":"remove-threat","module":"active-response"},"command":"check_keys", "parameters":{"keys":[]}}\n'
    read RESPONSE
    COMMAND2=$(echo $RESPONSE | jq -r .command)
    if [ ${COMMAND2} != "continue" ]; then
        echo "`date '+%Y/%m/%d %H:%M:%S'` $0: $INPUT_JSON Remove threat active response aborted" >> ${LOG_FILE}
        exit 0
    fi
fi

# Remove file
rm -f $FILENAME
if [ $? -eq 0 ]; then
    echo "`date '+%Y/%m/%d %H:%M:%S'` $0: $INPUT_JSON Successfully removed threat" >> ${LOG_FILE}
else
    echo "`date '+%Y/%m/%d %H:%M:%S'` $0: $INPUT_JSON Error removing threat" >> ${LOG_FILE}
fi

exit 0
```

### 1.4 Set File Permissions

Ensure the script has the correct ownership and permissions.

```bash
sudo chmod 750 /var/ossec/active-response/bin/remove-threat.sh
sudo chown root:wazuh /var/ossec/active-response/bin/remove-threat.sh
```

### 1.5 Restart Wazuh Agent

Restart the Wazuh agent to apply the changes:

```bash
sudo systemctl restart wazuh-agent
```

---

## 2. Wazuh Server Configuration

Follow these steps on the Wazuh server to enable alerts for changes in the endpoint's `/root` directory and integrate with VirusTotal for threat intelligence.

### 2.1 Add Custom Rules

Add the following rules to the `/var/ossec/etc/rules/local_rules.xml` file on the Wazuh server. These rules will alert when changes occur in the `/root` directory.

```xml
<group name="syscheck,pci_dss_11.5,nist_800_53_SI.7,">
    <rule id="100200" level="7">
        <if_sid>550</if_sid>
        <field name="file">/root</field>
        <description>File modified in /root directory.</description>
    </rule>
    <rule id="100201" level="7">
        <if_sid>554</if_sid>
        <field name="file">/root</field>
        <description>File added to /root directory.</description>
    </rule>
</group>
```

### 2.2 Enable VirusTotal Integration

Edit the Wazuh server's `/var/ossec/etc/ossec.conf` file to enable VirusTotal integration. Replace `<YOUR_VIRUS_TOTAL_API_KEY>` with your actual VirusTotal API key.

```xml
<ossec_config>
  <integration>
    <name>virustotal</name>
    <api_key><YOUR_VIRUS_TOTAL_API_KEY></api_key>
    <rule_id>100200,100201</rule_id>
    <alert_format>json</alert_format>
  </integration>
</ossec_config>
```

**Note:** The free VirusTotal API key has a rate limit of four requests per minute. If using a premium API key, you can increase the query frequency and add more rules to monitor additional directories.

### 2.3 Configure Active Response

Add the following configuration to `/var/ossec/etc/ossec.conf` to enable active response for triggering the `remove-threat.sh` script when a suspicious file is detected.

```xml
<ossec_config>
  <command>
    <name>remove-threat</name>
    <executable>remove-threat.sh</executable>
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

### 2.4 Add Active Response Alert Rules

Add the following rules to `/var/ossec/etc/rules/local_rules.xml` to alert on active response results:

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

### 2.5 Restart Wazuh Manager

Restart the Wazuh manager to apply the configuration changes:

```bash
sudo systemctl restart wazuh-manager
```

---

## 3. Attack Emulation

To simulate a threat, download the EICAR test file to the `/root` directory on the Ubuntu endpoint:

```bash
sudo curl -Lo /root/eicar.com https://secure.eicar.org/eicar.com && sudo ls -lah /root/eicar.com
```

---

## 4. Visualize Alerts

You can visualize the alert data in the Wazuh dashboard by using the **Threat Hunting** module. Add the following filters in the search bar to query relevant alerts:

```bash
Linux - rule.id: is one of 553,100092,87105,100201
```

<div align=center>
    <img src="https://github.com/user-attachments/assets/fbad936f-84b4-4bb8-80f6-30556422ffb4"></src>
</div>
