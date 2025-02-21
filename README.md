# <div align="center">Wazuh</div>
<div align="center">
<img src="https://github.com/user-attachments/assets/818c4229-e59a-41b6-a10a-ef8d4775c076" height="200"></img>
</div>

 
> # Topics
* [Introduction to Wazuh](#introduction-to-wazuh)
* [HIDS,OSSEC and Wazuh](#what-is-hids-)
* [Components of Wazuh](#components-of-wazuh)
* [Architecture of Wazuh](https://github.com/Esther7171/Wazuh/blob/main/README.md#architecture-of-wazuh)
* [Deployment Methods](https://github.com/Esther7171/Wazuh/blob/main/README.md#deployment-methods)
* [Wazuh Feature](https://github.com/Esther7171/Wazuh/edit/main/README.md#wazuh-features-and-capabilities)
* [Wazuh Installation]( )
* [Wazuh Intergration](#wazuh-integrations)
* [Installing the Wazuh Agent on an Ubuntu Endpoint: Enrollment Guide]()
* [Installing the Wazuh Agent on an Windows Endpoint: Enrollment Guide]()
* [Installing the Wazuh Agent on an Ubuntu Endpoint: Enrollment Guide]()
* [Uninstalling the Wazuh agent](#uninstalling-the-wazuh-agent-form-agent-side)
* [Wazuh Ruleset & Decoders]
* [File Integrity Monitoring (FIM) Configuration](./Files/Integration/FIM/readme.md)
* [Detecting and removing malware using VirusTotal integration](./Files/Integration/virus-total)
* [Detecting Network using Suricata `IDS`]()
* [Detecting Vulnerabilities]
* [Detecting Execution of Malicious Commands]
* [Detecting and Blocking Brute Force Attack]
* [Get Wazuh Alert on Mail (Configure smtp)](Files/Smtp/readme.md)
* [Linux-Server Hardening]

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

## What is Difference between Component and Architecture
| Component |  Architecture |
|-----------|---------------|
| The component talks about smaller scope focuing majorly on functionality and on differenet services mor different modules | This is all baout high level structure of your software this is about preformace of your system, The preformance of the system improvced when you have better scalability and elasticity and databse and Securitiy Function and how do youi maintain the entire infrastructure |

# Architecture of Wazuh

<div align="center">
<img src="https://github.com/user-attachments/assets/2bc6cbbd-a09a-4911-8101-2a1bae2c83a7">
</div>

<div align="center">
<img width="2959" alt="wazuh arch" src="https://github.com/user-attachments/assets/93e45c66-f9f1-4032-8032-8a0f85322f3d">
</div>



# Deployment Methods

* Distributed Servers
* Virtual Machine
* Amazon Machine Image (AMI)
* Docker
* Kubernetes

Single node 
1. all in one
Multi node deployment we have 2 nodes
1. master
2. worker
3. it will be indexer
4. dashboard

## Wazuh Features and Capabilities

| S.no | Feature | Discription |
|------|---------|-------------|
| 1. | Intrusion Detection | Scan and Monitor Endpoints. Llook for rootkit, malware, detect hidden file and unregiter network listners.
| 2. | Log Data Analysis | Read os logs and app logs  then encript it and send it to manager or server on rule base analysis. We still get data form sys logs like ```Router or switches```
| 3. | File Integrity Monitoring | Wazuh Monitor the file system  Identify any changes in the content, permission, ownership and different attributes of file and generates an alert when there is any unauthorized changes. We can join pci  










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


# Uninstalling the Wazuh agent form Agent side
> ### Windows Wazuh agent
#### ```Disable the wazuh service```
#### ```Delete this folder in C Drive```
```
C:\Program Files (x86)\ossec-agent
```

> ### Linux Wazuh agent
#### ```Disable the Service```
```
systemctl disable wazuh-agent
systemctl daemon-reload
```
#### ```Remove the Wazuh agent installation.```
##### ```yum```
```
yum remove wazuh-agent
```
##### ```apt```
```
apt-get remove wazuh-agent -y
apt-get remove --purge wazuh-agent -y
```

### Uninstalling the Wazuh agent form Server side
#### Copy past this
```
/var/ossec/bin/manage_agents
```
### U will get this prompt
```
wazuh@wazuh:~$ sudo /var/ossec/bin/manage_agents


****************************************
* Wazuh v4.9.2 Agent manager.          *
* The following options are available: *
****************************************
   (A)dd an agent (A).
   (E)xtract key for an agent (E).
   (L)ist already added agents (L).
   (R)emove an agent (R).
   (Q)uit.
Choose your action: A,E,L,R or Q:
```
#### Press R/r
```
wazuh@wazuh:~$ sudo /var/ossec/bin/manage_agents


****************************************
* Wazuh v4.9.2 Agent manager.          *
* The following options are available: *
****************************************
   (A)dd an agent (A).
   (E)xtract key for an agent (E).
   (L)ist already added agents (L).
   (R)emove an agent (R).
   (Q)uit.
Choose your action: A,E,L,R or Q: r

Available agents:
   ID: 001, Name: windows-test, IP: any
   ID: 002, Name: on-ubuntu, IP: any
Provide the ID of the agent to be removed (or '\q' to quit):
```
### Give the id of agent u wanna remove
check out
