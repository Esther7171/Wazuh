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
