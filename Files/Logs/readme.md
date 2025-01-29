```ps1
curl https://github.com/olafhartong/sysmon-modular/blob/master/sysmonconfig.xml -o sysmonconfig.xml
```
```ps1
.\sysmon64.exe -accepteula -i .\sysmonconfig.xml
```

Sysmon installation and configuration
In order to modify the Sysmon default configuration, which is needed for the purpose of this article, it is necessary to create an XML file. Below you can see an XML configuration that would work for Sysmon to generate the right log when Powershell is executed:



Ossec.conf
```xml
<localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
</localfile>
```

/var/ossec/etc/rules/local_rules.xml For Injection detection rule.
```xml
<group name="windows,sysmon">
  <rule id="100200" level="12">
    <if_sid>61610</if_sid>
    <description>Possible process injection activity detected from "$(win.eventdata.sourceImage)" on "$(win.eventdata.targetImage)"</description>
    <mitre>
      <id>T1055.001</id>
    </mitre>
  </rule>
 
  <rule id="100100" level="0">
    <if_sid>100200</if_sid>
    <field name="win.eventdata.sourceImage" type="pcre2">(C:\\\\Windows\\\\system32)|chrome.exe</field>
    <description>Ignore Windows binaries and Chrome</description>
  </rule>
</group>
<group name="windows, sysmon, sysmon_process-anomalies,">
   <rule id="100000" level="12">
     <if_group>sysmon_event1</if_group>
     <field name="win.eventdata.image">mimikatz.exe</field>
     <description>Sysmon - Suspicious Process - mimikatz.exe</description>
   </rule>

   <rule id="100001" level="12">
     <if_group>sysmon_event8</if_group>
     <field name="win.eventdata.sourceImage">mimikatz.exe</field>
     <description>Sysmon - Suspicious Process mimikatz.exe created a remote thread</description>
   </rule>

   <rule id="100002" level="12">
     <if_group>sysmon_event_10</if_group>
     <field name="win.eventdata.sourceImage">mimikatz.exe</field>
     <description>Sysmon - Suspicious Process mimikatz.exe accessed $(win.eventdata.targetImage)</description>
   </rule>
</group>
```


use sysmon
```
https://wazuh.com/blog/learn-to-detect-threats-on-windows-by-monitoring-sysmon-events/
```
```
https://wazuh.com/blog/using-wazuh-to-monitor-sysmon-events/
```
