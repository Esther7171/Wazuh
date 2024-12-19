# <div align="center">Virus Total Integration with Wazuh</div>

<br>Wazuh uses the integrator module to connect to external APIs and alerting tools such as VirusTotal.

You need a [VirusTotal API key](https://www.virustotal.com/gui/) in this use case to authenticate Wazuh to the VirusTotal API.
Just Create an Account and get your api key

> ## How will it work?
> We'll integrate the VirusTotal API with the Wazuh server. For Windows, a Python-based executable will enable agents to detect and remove malware using VirusTotal data. For Linux, a bash script will serve the
> same purpose. Note: The free VirusTotal API allows up to four requests per minute. With a premium API key, you can increase query frequency and add more rules. You can also configure Wazuh to monitor additional directories beyond C:\Users\<USER_NAME>\Downloads.

First, configure the agent, then the Wazuh server and set rules and decoders
