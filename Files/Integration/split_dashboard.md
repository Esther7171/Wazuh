1. Configure Sysmon
2. Open Powershell in Admin At default ```C:``` drive
```
cd c:\
```
3. Download Sysmon
```
curl https://download.sysinternals.com/files/Sysmon.zip -o Sysmon.zip
```
4. Unzip The Sysmon
```ps
Expand-Archive Sysmon.zip
```
5. Remove Sysmon.zip becouse it no longer in use.
```ps
rm Sysmon.zip
```
6. Go to folder.
```
cd Sysmon
```
7. Install Wazuh Sysmon-config file
```ps1
curl -o sysmonconfig.xml https://wazuh.com/resources/blog/emulation-of-attack-techniques-and-detection-with-wazuh/sysmonconfig.xml
```
8. Install Config File 
```ps1
.\sysmon64.exe -accepteula -i .\sysmonconfig.xml
```

* Open Powershell as admin
```
notepad.exe 'C:\Program Files (x86)\ossec-agent\ossec.conf'
```
* Agent Ossec.conf add
```xml
<localfile>
  <location>Microsoft-Windows-Windows Defender/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>

<localfile>
  <location>Microsoft-Windows-PrintService/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>

<localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
</localfile>

<!-- CPU Usage -->
    <wodle name="command">
        <disabled>no</disabled>
        <tag>CPUUsage</tag>
        <command>Powershell -c "@{ winCounter = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples[0] } | ConvertTo-Json -compress"</command>
        <interval>1m</interval>
        <ignore_output>no</ignore_output>
        <run_on_start>yes</run_on_start>
        <timeout>0</timeout>
    </wodle>
<!-- Memory Usage -->
    <wodle name="command">
        <disabled>no</disabled>
        <tag>MEMUsage</tag>
        <command>Powershell -c "@{ winCounter = (Get-Counter '\Memory\Available MBytes').CounterSamples[0] } | ConvertTo-Json -compress"</command>
        <interval>1m</interval>
        <ignore_output>no</ignore_output>
        <run_on_start>yes</run_on_start>
        <timeout>0</timeout>
    </wodle>
<!-- Network Received -->
    <wodle name="command">
        <disabled>no</disabled>
        <tag>NetworkTrafficIn</tag>
        <command>Powershell -c "@{ winCounter = (Get-Counter '\Network Interface(*)\Bytes Received/sec').CounterSamples[0] } | ConvertTo-Json -compress"</command>
        <interval>1m</interval>
        <ignore_output>no</ignore_output>
        <run_on_start>yes</run_on_start>
        <timeout>0</timeout>
    </wodle>
<!-- Network Sent -->
    <wodle name="command">
        <disabled>no</disabled>
        <tag>NetworkTrafficOut</tag>
        <command>Powershell -c "@{ winCounter = (Get-Counter '\Network Interface(*)\Bytes Sent/sec').CounterSamples[0] } | ConvertTo-Json -compress"</command>
        <interval>1m</interval>
        <ignore_output>no</ignore_output>
        <run_on_start>yes</run_on_start>
        <timeout>0</timeout>
    </wodle>
<!-- Disk Free -->
    <wodle name="command">
        <disabled>no</disabled>
        <tag>DiskFree</tag>
        <command>Powershell -c "@{ winCounter = (Get-Counter '\LogicalDisk(*)\Free Megabytes').CounterSamples[0] } | ConvertTo-Json -compress"</command>
        <interval>1m</interval>
        <ignore_output>no</ignore_output>
        <run_on_start>yes</run_on_start>
        <timeout>0</timeout>
    </wodle>
```
# Server
1. Create a Group
2. edit group and past this:
```xml
<agent_config>
       <labels>
               <label key="group">Team_A</label>
       </labels>
       
       <localfile>
           <location>Microsoft-Windows-Windows/Operational</location>
           <log_format>eventchannel</log_format>
       </localfile>
</agent_config>
```
