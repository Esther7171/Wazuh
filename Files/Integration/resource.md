```
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
