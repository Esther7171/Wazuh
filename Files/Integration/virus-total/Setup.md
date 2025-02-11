# VirusTotal Integration with Wazuh

## Overview
Wazuh integrates with external APIs and alerting tools through its integrator module, allowing for enhanced detection and response capabilities. In this guide, we will demonstrate how to integrate the VirusTotal API with Wazuh.

## Prerequisites
- A [VirusTotal API key](https://www.virustotal.com/gui/) is required for this integration. You can obtain your API key by creating an account on VirusTotal.

## How It Works
This integration will enable Wazuh to use VirusTotal data for malware detection and response.

- **Windows**: A Python-based executable will be used to allow Wazuh agents to detect and remove malware using VirusTotal data.
- **Linux**: A Bash script will be used for the same purpose.

**Note**: The free VirusTotal API allows up to four requests per minute. With a premium API key, you can increase the frequency of queries and access additional features, such as monitoring additional directories beyond the default `C:\Users\<USER_NAME>\Downloads`.

## Steps for Integration

### 1. Configure the Wazuh Agent
- Ensure the Wazuh agent is correctly configured to interact with the VirusTotal API.

### 2. Configure the Wazuh Server
- Set up the server to communicate with the VirusTotal API and enable the appropriate rules and decoders.

### 3. Set Up Rules and Decoders
- After configuring the agent and server, apply the necessary rules and decoders to ensure proper functionality and detection.

By following these steps, you'll be able to leverage VirusTotal's threat intelligence within your Wazuh environment for enhanced malware detection and remediation.

---

*For additional information or troubleshooting, please refer to the Wazuh and VirusTotal documentation.*

## Wazuh server
1. add this rules `/var/ossec/etc/rules/local_rules.xml`

```xml
<group name="syscheck,pci_dss_11.5,nist_800_53_SI.7,">
    <!-- Rules for Linux systems -->
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
2. Add Config Get Your api key from virus total past it at `/var/ossec/etc/ossec.conf` add this at bottom before `</ossec_config>`

```xml
<!-- Virus Total Integration Start here-->
  <integration>
    <name>virustotal</name>
    <api_key><YOUR_VIRUS_TOTAL_API_KEY></api_key> <!-- Replace with your VirusTotal API key -->
    <group>syscheck</group>
    <alert_format>json</alert_format>
  </integration>

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

<!-- Virus Total Integration End here-->
```
