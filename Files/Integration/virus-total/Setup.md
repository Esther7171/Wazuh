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
