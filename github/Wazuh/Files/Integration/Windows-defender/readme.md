## Integrating Wazuh with Microsoft Defender Alerts  

#### Steps to Configure Wazuh  

1. **Access the Wazuh Dashboard**  
   - Open the Wazuh Dashboard.  
   - Click on the menu icon (☰) in the top-left corner.  

<div align="center">
<img src="https://github.com/user-attachments/assets/b321077b-bc37-4c2a-9008-42203f2a5809" height="400"></img>
</div>

2. **Navigate to the Agent Group**  
   - Search for "Group" in the menu.  
   - Click the **Edit** (pencil) icon for the desired agent group.

<div align="center">
<img src="https://github.com/user-attachments/assets/eb1c4361-ad03-400a-b899-a782d7a2c3de" height=""></img>
</div>


3. **Modify the `agent.conf` File**  
   - Add the following rule to the `agent.conf` file via the Wazuh Dashboard:  

   ```xml
   <localfile>
     <location>Microsoft-Windows-Windows Defender/Operational</location>
     <log_format>eventchannel</log_format>
   </localfile>
   ```
   
<div align="center">
<img src="https://github.com/user-attachments/assets/cbb310fd-445a-4970-b385-45d1b3408a32" height=""></img>
</div>

4. **Save and Apply the Changes**  
   - Save the configuration and restart the Wazuh agent if necessary.  

<div align="center">
<img src="https://github.com/user-attachments/assets/d48aba16-881e-4687-a6c5-cf9805c98b59" height="250"></img>
</div>


## Agent.conf
```
notepad.exe 'C:\Program Files (x86)\ossec-agent\ossec.conf'
```
Add this lines:
```xml
<localfile>
  <location>Microsoft-Windows-Windows Defender/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```
