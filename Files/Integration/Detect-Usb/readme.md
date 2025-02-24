### **Step 1: Enable Audit PNP Activity on Windows**
Windows event logs capture USB insertion events using Event ID **6416**. You need to enable this logging.

1. Press `Win + R`, type **`secpol.msc`**, and press **Enter**.
2. Navigate to:
   - `Advanced Audit Policy Configuration` > `System Audit Policies - Local Group Policy Object` > `Detailed Tracking`
3. Find **Audit PNP Activity**, double-click it, and:
   - Select **"Configure the following audit events"**.
   - Check **"Success"**.
   - Click **OK**.

---

### **Step 2: Configure Wazuh Rules to Detect USB Insertions**
On the Wazuh server, create a custom rule in **`/var/ossec/etc/rules/local_rules.xml`** to detect USB activity.

1. Open the rules file:
   ```bash
   sudo nano /var/ossec/etc/rules/local_rules.xml
   ```
2. Add the following rule inside the `<group name="windows-usb-detect,">` tag:
   ```xml
   <group name="windows-usb-detect,">
      <rule id="111000" level="7">
        <if_sid>60103</if_sid>
        <field name="win.system.eventID">^6416$</field>
        <match>USBSTOR\\Disk</match>
        <options>no_full_log</options>
        <description>Windows: A PNP device $(win.eventdata.deviceDescription) was connected to $(win.system.computer).</description>
      </rule>
   </group>
   ```
3. Save the file and restart Wazuh:
   ```bash
   sudo systemctl restart wazuh-manager
   ```

---

### **Step 3: Create a CDB List for Authorized USBs**
1. Identify a known USB device from a Wazuh alert and extract **deviceId**.
2. Create a **usb-drives** CDB list:
   ```bash
   sudo touch /var/ossec/etc/lists/usb-drives
   ```
3. Add the extracted **deviceId** to the list:
   ```
   USBSTOR\Disk&Ven_ADATA&Prod_USB_Flash_Drive&Rev_1100\273170825011004C&0:
   ```
4. Link the list in **ossec.conf** (`/var/ossec/etc/ossec.conf`):
   ```xml
   <ruleset>
      <list>etc/lists/usb-drives</list>
   </ruleset>
   ```

---

### **Step 4: Create Rules for Authorized & Unauthorized USBs**
Modify **`/var/ossec/etc/rules/local_rules.xml`** to include:

```xml
<rule id="111001" level="5">
  <if_sid>111000</if_sid>
  <options>no_full_log</options>
  <description>Windows: Authorized PNP device $(win.eventdata.deviceDescription) was connected to $(win.system.computer).</description>
</rule>

<rule id="111002" level="8">
  <if_sid>111000</if_sid>
  <list field="win.eventdata.deviceId" lookup="not_match_key">etc/lists/usb-drives</list>
  <options>no_full_log</options>
  <description>Windows: Unauthorized PNP device $(win.eventdata.deviceDescription) was connected to $(win.system.computer).</description>
</rule>
```

Restart Wazuh:
```bash
sudo systemctl restart wazuh-manager
```

---

### **Step 5: Test the Configuration**
1. **Plug in an authorized USB** (from your CDB list).
   - You should see an alert in **Security Events** with rule ID `111001`.
2. **Plug in an unauthorized USB** (not in your CDB list).
   - You should see an alert in **Security Events** with rule ID `111002`.

---

### **Step 6: Import Custom Visualization in Wazuh**
1. Download the visualization file:
   ```
   windows-usb-drive-monitoring-visualization.ndjson
   ```
2. Open **Wazuh Dashboard**.
3. Go to **Management** > **Stack Management** > **Saved Objects**.
4. Click **Import** and select the downloaded file.
5. After import, navigate to **Visualize** > **Windows USB Drive Monitoring**.

---
Detect USB Storage
In this use case, we configured the Wazuh agent to detect when a USB storage device is connected to a Windows endpoint. Then we create rules to generate alerts when the USB device is detected.

Configuration
Windows endpoint
On the Windows endpoint, we want to monitor the output of the USBSTOR registry entry using the reg Query command. Then, we create a rule to trigger an alert when the command output contains a value.

Perform the following steps on the Windows endpoint.

Enable remote command execution on the Windows endpoint by appending the following settings to the C:\Program Files (x86)\ossec-agent\local_internal_options.conf file:

Warning Enable remote command execution with caution as this gives the Wazuh user permission to run any command on the endpoint.

logcollector.remote_commands=1
Restart the Wazuh agent to apply the changes, using PowerShell with administrator privileges:


> Restart-Service -Name wazuh
Wazuh server
Perform the following steps on the Wazuh server.

Append the following configuration to the /var/ossec/etc/shared/default/agent.conf file on the Wazuh server:


<agent_config os="Windows">
  <localfile>
    <log_format>command</log_format>
    <command>reg QUERY HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR</command>
    <alias>check_usb_connetivity</alias>
  </localfile>
</agent_config>
Where:

The value command of the <log_format> tag specifies the output of the command is read as multiple events.

The value reg QUERY HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR of the <command> tag is the command the Logcollector module executes to know if a USB device is attached to the endpoint.

The value check_usb_connetivity of the <alias> tag is a string that represents the reg QUERY HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR command for better identification in creating rules.

Add the following rules to the /var/ossec/etc/rules/local_rules.xml file on the Wazuh server:


<group name="detect_usb_storage,">
  <rule id="100016" level="7">
    <if_sid>530</if_sid>
    <match>^ossec: output: 'check_usb_connetivity':</match>
    <description>New USB device connected</description>
  </rule>
</group>
Restart the Wazuh manager to apply the changes:


sudo systemctl restart wazuh-manager

```
https://wazuh.com/blog/monitoring-usb-drives-in-windows-using-wazuh/
```
