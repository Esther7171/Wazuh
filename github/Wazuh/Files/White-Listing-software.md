<img width="1861" height="751" alt="image" src="https://github.com/user-attachments/assets/c8f1c085-6d8c-4453-a96b-0bb0a3323656" />

<!--   cHECK OUT THIS SYSMON RULES -->
## Agent config
setup sysmon
after that download this software [pskill](https://download.sysinternals.com/files/PSTools.zip)
or open terminal
```
 curl https://download.sysinternals.com/files/PSTools.zip -o 'C:\PSTools.zip'
```
Extract file
```
Expand-Archive 'C:\PSTools.zip'
```
Remove zip file
```
rm 'C:\PSTools.zip'
```

## Wazuh Server config
#### Defining the software list (proactive mode)
If you already have a list of software (by vendor, product, etc.), use that info to create a Wazuh list. The names used for this list SHOULD match the vendor/product information that Sysmon (event ID =1, Process Started) reports in its “win.eventdata.company” / “win.eventdata.product” fields.

#### Defining the software list (reactive mode)
A software inventory can be reactively built by evaluating the following fields in events where Wazuh’s rule groups = “sysmon_event1”:

Software Company: “win.eventdata.company”.
Software Product/Package: “win.eventdata.product”.
If Sysmon events have been collected for a significant period of time, the list will reflect an inventory of software, vendors or products, used in your environment.

In this document we’ll use Software Company to define the list of approved applications.

Detecting process execution not part of the approved software policy
Create a CDB list with the list of approved software vendors (companies), “/var/ossec/etc/lists/software-vendors”. As an example:

Create a list 
```
nano /var/ossec/etc/lists/software-vendors
```
Add
```
Microsoft Corporation:
Sysinternals - www.sysinternals.com:
The Git Development Community:
Vivaldi Technologies AS:
GitHub, Inc.:
GitHub:
Brave Software, Inc.:
Node.js:
Avira Operations GmbH &amp; Co. KG:
BraveSoftware Inc.:
Sysinternals:
Google LLC:
```
> NOTE: The colon at the end of each line is necessary.
#### after that open osec.conf file
```
nano /var/ossec/etc/ossec.conf
```
Add the new list in ossec.conf (manager), under the "rulset" section:
```
<list>etc/lists/software-vendors</list>
```

![image](https://github.com/user-attachments/assets/184afe2f-b274-4131-867d-06ef3951db18)

Create detection rule to detect processes started where the field “win.eventdata.company” is NOT included in that list (You can also add it at the bottom of this rule file):
```
<group name="Software white-listing">
<!-- Rules 100500 - 100999: Exceptions/Rule Level Mod -->
<rule id="100500" level="10">
<if_sid>101101</if_sid>
<list field="win.eventdata.company" lookup="not_match_key">etc/lists/software-vendors</list>
<description>Software not whitelisted - Sysmon - Event 1: Process $(win.eventdata.description) started but not allowed ><mitre>
<id>T1036</id>
</mitre>
<options>no_full_log</options>
<group>sysmon_event1,software_policy</group>
</rule>
</group>
```
