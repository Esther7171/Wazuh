# Wazuh

> ## Course Outline
* [Introduction to Wazuh](https://github.com/Esther7171/Wazuh#introduction-to-wazuh)
* [HIDS,OSSEC and Wazuh](https://github.com/Esther7171/Wazuh/blob/main/README.md#what-is-hids-)
* Components of Wazuh
* Architecture of Wazuh
* Deployment Methods
* Wazuh Feature
* Wazuh Demo
* [Wazuh Intergration](https://github.com/Esther7171/Wazuh/blob/main/README.md#wazuh-integrations)
* Ubuntu Endpoint agent Enrollement
* Windows Endpoint agent Enrollment
* Wazuh Ruleset & Decoders
* Hands on lab 1: FilE Intergrity Monitoring
* Hands on lab 2: Detecting Network using Suricata IDS 
* Hands on Lab 3: Detecting Vulnerabilities
* Hands on lab 4: Detecting Execution of Malicious Commands
* Hands on lab 5: Detecting and Blocking Brute Force Attack
* Hands on lab 6: Detecting Malaicious files using VirusTotal

> # Introduction to Wazuh
OSSEC is open source HIDS security platform and a Host Intrusion Detection System(HIDS) software. Created by Daniel CID in year 2004, In year 2015 it forked from OSSEC AND Wazuh platform was created  

> # What is HIDS ?
Host-Based Intrusion Detection System that install directly on endpoint or servers. Purpose is basically to identify any Malicious activities or policy violations on individual hosts or devices. Deployed on each device or host that needs to be monitord
For example: Realted to Memory,Suspicious Process, Installlation of  ROOT-KIT , KERNAL LV Activity.
> OSSEC Features
* Log Analysis
* File Integrity
* Rootkit Detection
* Reak-Time Alerts
* Compliance

> # How Wazuh is different from OSSEC ?
* Vulnerability Detection
* Security Configuration Assessment (SCS) ---> (CISB)
* Cloud Security (AWS,AZURE,GOOGLE CLOUD...)
* Comprehensive Dashboard
* Integration
* Better Community Support


> # [Components of Wazuh](https://github.com/Esther7171/Wazuh/edit/main/README.md#components-of-wazuh)

<div align="center">
<img src="https://github.com/user-attachments/assets/f3d5b53d-73a6-4cfd-bbf4-195e2641192d" height=""></img>
</div>

| S.no | Components |
|------|------------|
|1.| Agent|
|2.|Server|
|3.|Indexer|
|4.|Dashboard|


# Wazuh Agent: It Installed on endpoints.

## Agent Modules:

| S.No | Agent Modules | Description|
|------|---------------|------------|
|1.|Active response| Incident Response,Kind of script which will be triggered once specific rules ment|
|2.|Command Execution| Monitor running commands on Terminal |
|3.|Configuration Assessment| used as security audit | 
|4.|Container Security| Docker,Kubernetes,Openshift|
|5.|Cloud Security| Aws,Azure,GCP |
|6.|File Integrity Monitoring | It is used to Monitor any file additon,Edit,deletion, ownership and permission|
|7.|Log Collector| Collect logs|
|8.|Malware Detection| Detect malicious files |
|9.|System Inventory| Monitor installed app,storage|

## Agent Daemon:

| S.No | Agent Modules |
|------|---------------|
|1.|Data Encryption |
|2.|Modules Management |
|3.|Remote Configuration |
|4.|Server Authentication |

## IF any of these Collect Logs It will immediately send it to Centeral Components -> Wazuh Server

## Wazuh Server

<div align="center">
<img width="5567" alt="wazuh-chart" src="https://github.com/user-attachments/assets/0e425c0b-6539-42ab-b06d-3644db5f459a">
</div>





















# Wazuh Integrations
>  ## Antivirus
- [ ] CLamAV
- [ ] Kaspersky Antivirus
- [ ] McAfee
- [ ] Sophos
- [ ] Symantec Endpoint Protection

>  ## Endpoint Detection and Response (EDR)
- [ ] CrowdStrick Falcon
- [ ] Carbon Black
- [ ] Cylance PROTECT
- [ ] Sentinel One
- [ ] Microsoft Defender for Endpoint

>  ## SOAR (Security Orchestration Automation,and Response)
- [ ] Shuffle SOAR
- [ ] Cortex XSOAR
- [ ] Siemplify
- [ ] Swimlane

>  ## Incident Response
- [ ] TheHive
- [ ] MISP (Malware Information Sharing Platform)
- [ ] IR Flow
- [ ] IBM Resilient
- [ ] Splunk Phantom

> ## Threat Intelligence
- [ ] Virus Total
- [ ] AlienValut OTX
- [ ] IBM X-Force Exchange
- [ ] Recorded Future
- [ ] Threat Connect

> ## Intrusion Detection System (IDS) / Intrusion Prevention System (IPS)
- [ ] Suricata
- [ ] Snort
- [ ] Zeek (formerly bro)

> ## Log Management
- [ ] Graylog
- [ ] Grafana
- [ ] Elastic Stack

> ## Cloud Security
- [ ] AWS CloudTrail
- [ ] Azure Security Center
- [ ] Google Cloud Security Command Center
- [ ] Cloudflare
