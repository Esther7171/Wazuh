# Logs Configure Sysmon
1. Open Powershell in Admin At default ```C:``` drive
```
cd c:\
```
2. Download Sysmon
```
curl https://download.sysinternals.com/files/Sysmon.zip -o Sysmon.zip
```
3. Unzip The Sysmon
```ps
Expand-Archive Sysmon.zip
```
4. Remove Sysmon.zip becouse it no longer in use.
```ps
rm Sysmon.zip
```
5. Go to folder.
```
cd Sysmon
```
6. Install Wazuh Sysmon-config file
```ps1
curl -o sysmonconfig.xml https://wazuh.com/resources/blog/emulation-of-attack-techniques-and-detection-with-wazuh/sysmonconfig.xml
```
7. Install Config File 
```ps1
.\sysmon64.exe -accepteula -i .\sysmonconfig.xml
```

# Detecting PowerShell Exploitation Techniques in Windows Using Wazuh
Step 1: Enable PowerShell Logging

* Open Powershell as admin
```ps1
function Enable-PSLogging {
    # Define registry paths for ScriptBlockLogging and ModuleLogging
    $scriptBlockPath = 'HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'
    $moduleLoggingPath = 'HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ModuleLogging'
    
    # Enable Script Block Logging
    if (-not (Test-Path $scriptBlockPath)) {
        $null = New-Item $scriptBlockPath -Force
    }
    Set-ItemProperty -Path $scriptBlockPath -Name EnableScriptBlockLogging -Value 1

    # Enable Module Logging
    if (-not (Test-Path $moduleLoggingPath)) {
        $null = New-Item $moduleLoggingPath -Force
    }
    Set-ItemProperty -Path $moduleLoggingPath -Name EnableModuleLogging -Value 1
    
    # Specify modules to log - set to all (*) for comprehensive logging
    $moduleNames = @('*')  # To specify individual modules, replace * with module names in the array
    New-ItemProperty -Path $moduleLoggingPath -Name ModuleNames -PropertyType MultiString -Value $moduleNames -Force

    Write-Output "Script Block Logging and Module Logging have been enabled."
}

Enable-PSLogging
```

> The output should be 
```
Output Script Block Logging and Module Logging have been enabled.
```

## Atomic Red Team installation
* ART Execution Framework and Atomics folder installation.
* The following command will perform the installation of the Execution Framework as well as the Atomics folder, which contains the tests and binaries that are needed for the emulation:
```ps
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing)
Install-AtomicRedTeam -Force -getAtomics
```
* Importing the ART module
```
Import-Module "C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1" -Force
```
2. After installation finishes, confirm the folder exists:
```
ls C:\AtomicRedTeam\atomics
```
3. Then re-import the module and test again:
```ps
Import-Module "C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1" -Force
Invoke-AtomicTest T1548.002 -ShowDetailsBrief
```

## Virus-Total
* Install Python, Download the Python installer from the official [Python-3.13.5](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe) website.
* Open the terminal as Administrator and install the required package:
```
pip install pyinstaller
```
```
pyinstaller -F --icon=logo.ico remove-threat.py
```






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

<localfile>
  <location>Microsoft-Windows-PowerShell/Operational</location>
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
