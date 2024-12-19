# <div align="center">Virus Total Integration with Wazuh</div>

<br>Wazuh uses the integrator module to connect to external APIs and alerting tools such as VirusTotal.

You need a [VirusTotal API key](https://www.virustotal.com/gui/) in this use case to authenticate Wazuh to the VirusTotal API.
Just Create an Account and get your api key

> ## How will it work?
> We'll integrate VirusTotal API with the Wazuh server and create a Python-based executable for agents to detect and remove malware using VirusTotal data.
> ### Note The free VirusTotal API rate limits requests to four per minute. If you have a premium VirusTotal API key, with a high frequency of queries allowed, you can add more rules besides these two. You can configure Wazuh to monitor more directories besides `C:\Users\<USER_NAME>\Downloads`.

First, configure the agent, then the Wazuh server and set rules and decoders
