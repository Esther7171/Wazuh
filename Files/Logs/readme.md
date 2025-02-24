Configure Wazuh With Sysmon So we See Incidents More Clearly

1. Open Powershell in Admin At default ```C:``` drive
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

Sysmon installation and configuration
In order to modify the Sysmon default configuration, which is needed for the purpose of this article, it is necessary to create an XML file. Below you can see an XML configuration that would work for Sysmon to generate the right log when Powershell is executed:

Open Powershell as admin
```
notepad.exe 'C:\Program Files (x86)\ossec-agent\ossec.conf'
```
Agent ```Ossec.conf``` add 
```xml

<localfile>
  <location>Microsoft-Windows-PrintService/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
<localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
</localfile>
```

<div align="center">
<img src="https://github.com/user-attachments/assets/54c7a1e4-dec1-4da7-a101-0cd0042ce711"></img>
</div>
    
---
### **🔍 Detect USB and Printer Activity using Sysmon & Wazuh**  

Sysmon does not directly monitor USB insertions or printer usage, but we can **correlate Windows Event Logs with Sysmon** using Wazuh. Here's how:

---

## **📌 Step 1: Enable Sysmon for USB and Printer Monitoring**  

Sysmon doesn’t log USB insertions by default, but we can use **Event ID 3 (Network Connection)** and **Event ID 1 (Process Creation)** to track USB-related activity.

### **1️⃣ Modify Sysmon Configuration**
Use the [SwiftOnSecurity Sysmon config](https://github.com/SwiftOnSecurity/sysmon-config) or create your own.

Download:
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml" -OutFile "sysmon-config.xml"
```
Modify the configuration:
- Add USB-related process monitoring (`rundll32.exe`, `powershell.exe`, `cmd.exe`, etc.):
  ```xml
  <ProcessCreate onmatch="include">
    <Image condition="contains">rundll32.exe</Image>
    <Image condition="contains">powershell.exe</Image>
    <Image condition="contains">cmd.exe</Image>
    <Image condition="contains">printui.exe</Image>
  </ProcessCreate>
  ```
- Enable Event ID `3` for USB network activity tracking:
  ```xml
  <NetworkConnect onmatch="include">
    <Image condition="contains">explorer.exe</Image>
  </NetworkConnect>
  ```

### **2️⃣ Apply Sysmon Configuration**
```powershell
.\sysmon64.exe -c sysmon-config.xml
```

---

## **📌 Step 2: Enable Windows Event Logs for USB & Printer Detection**  

Sysmon does not log USB insertions directly, so we need Windows Event IDs:

- **USB Insertions** → `Event ID 6416` (Audit PNP Device)
- **USB Removals** → `Event ID 2003` (Kernel-PNP)
- **Printer Usage** → `Event ID 307` (PrintService Operational)

### **1️⃣ Enable USB Logging**
Run the following PowerShell commands:
```powershell
auditpol /set /subcategory:"Plug and Play Events" /success:enable /failure:enable
```

### **2️⃣ Enable Printer Logs**
1. Open **Event Viewer** (`eventvwr.msc`).
2. Navigate to:
   ```
   Applications and Services Logs > Microsoft > Windows > PrintService
   ```
3. Right-click **Operational** and select **Enable Log**.

---

## **📌 Step 3: Configure Wazuh to Collect USB & Printer Logs**  

### **1️⃣ Edit `ossec.conf` on Wazuh Agent**
Modify **Wazuh Agent Configuration** (`C:\Program Files (x86)\ossec-agent\ossec.conf`) and add:

```xml
<localfile>
  <log_format>eventchannel</log_format>
  <location>Microsoft-Windows-Kernel-PnP/Device Management</location>
</localfile>

<localfile>
  <log_format>eventchannel</log_format>
  <location>Microsoft-Windows-PrintService/Operational</location>
</localfile>
```

Restart Wazuh Agent:
```powershell
Restart-Service WazuhSvc
```

---

## **📌 Step 4: Add Wazuh Rules for USB & Printer Events**
Edit **Wazuh Rules** on the **Wazuh Manager** (`/var/ossec/ruleset/rules/local_rules.xml`):

### **1️⃣ USB Detection Rules**
```xml
<group name="windows,usb,">
  <rule id="100010" level="7">
    <decoded_as>json</decoded_as>
    <field name="win.system">Microsoft-Windows-Kernel-PnP</field>
    <field name="win.eventdata.DeviceClass">USB</field>
    <description>USB device connected</description>
  </rule>
  
  <rule id="100011" level="7">
    <decoded_as>json</decoded_as>
    <field name="win.system">Microsoft-Windows-Kernel-PnP</field>
    <field name="win.eventdata.DeviceClass">USB</field>
    <description>USB device removed</description>
  </rule>
</group>
```

### **2️⃣ Printer Usage Rules**
```xml
<group name="windows,printer,">
  <rule id="100020" level="5">
    <decoded_as>json</decoded_as>
    <field name="win.system">Microsoft-Windows-PrintService</field>
    <field name="win.eventdata.Param1">Document Printed</field>
    <description>Printer activity detected</description>
  </rule>
</group>
```

### **3️⃣ Restart Wazuh Manager**
```bash
systemctl restart wazuh-manager
```

---

## **📌 Step 5: Verify USB & Printer Logs**
On Wazuh Manager, check for logs:
```bash
tail -f /var/ossec/logs/alerts/alerts.json | jq
```

You should see:
- **USB Insertions & Removals (`100010`, `100011`)**
- **Printer Activity (`100020`)**

use sysmon
```
https://wazuh.com/blog/learn-to-detect-threats-on-windows-by-monitoring-sysmon-events/
```
```
https://wazuh.com/blog/using-wazuh-to-monitor-sysmon-events/
```
