## 🛡️ Integrate Wazuh with Microsoft Defender Logs (Windows)  

#### Steps to Configure Wazuh  

1. **Access the Wazuh Dashboard**  
   - Open the Wazuh Dashboard.  
   - Click on the menu icon (☰) in the top-left corner.  

<div align="center">
<img src="https://github.com/user-attachments/assets/b321077b-bc37-4c2a-9008-42203f2a5809" height="400"></img>
</div>

---

2. **Navigate to the Agent Group**  
   - Search for "Group" in the menu.  
   - Click the **Edit** (pencil) icon for the desired agent group.

<div align="center">
<img src="https://github.com/user-attachments/assets/eb1c4361-ad03-400a-b899-a782d7a2c3de" height=""></img>
</div>

---

3. **Modify the `agent.conf` File**  

   
<div align="center">
<img src="https://github.com/user-attachments/assets/cbb310fd-445a-4970-b385-45d1b3408a32" height=""></img>
</div>

* Add the following rule to the `agent.conf` file via the Wazuh Dashboard:  

```xml
   <localfile>
     <location>Microsoft-Windows-Windows Defender/Operational</location>
     <log_format>eventchannel</log_format>
   </localfile>
```
---

4. **Save and Apply the Changes**  
   - Save the configuration and restart the Wazuh agent if necessary.  

<div align="center">
<img src="https://github.com/user-attachments/assets/d48aba16-881e-4687-a6c5-cf9805c98b59" height=""></img>
</div>


## 📦 Agent.conf

#### 📝 Step 1: Open the Wazuh Agent Configuration File

The Wazuh agent uses a config file to know **what logs to collect**. We need to edit that file and tell it to watch the Microsoft Defender logs.

#### ✅ Do this:

**1. Open the terminal as an administrator, then paste this command to open the Wazuh agent configuration file:**

```
notepad.exe "C:\Program Files (x86)\ossec-agent\ossec.conf"
```
> This opens the Wazuh agent’s config file in Notepad. You might need admin permission. If it asks, click **Yes**.

---

#### 🧩 Step 2: Add the Microsoft Defender Log Source

Scroll down and **paste** this code **before the last `</ossec_config>` line**:

```xml
<localfile>
  <location>Microsoft-Windows-Windows Defender/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

### 🧐 What does this mean?

* `<localfile>` = You're telling Wazuh to look at a new log file.
* `<location>` = This is where Defender stores its events in Windows (inside the Event Viewer).
* `<log_format>` = "eventchannel" tells Wazuh it's reading Windows Event Logs.

---

## 🔁 Step 3: Restart the Wazuh Agent

Now Wazuh knows where to look. You just need to restart it so it starts reading the Defender logs.

### ✅ How to restart:

```ps1
Restart-Service -Name wazuh
```
---

## 📚 More Info

* Wazuh [documentation](https://wazuh.com/blog/detecting-powershell-exploitation-techniques-in-windows-using-wazuh/)

* Defender Logs Path: `Event Viewer > Applications and Services Logs > Microsoft > Windows > Windows Defender > Operational`
