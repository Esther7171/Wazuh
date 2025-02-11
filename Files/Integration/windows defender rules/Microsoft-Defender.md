Go to Wazuh Dashboard

click on 3 line or burger menu 

<div align="center">
<img src="https://github.com/user-attachments/assets/b321077b-bc37-4c2a-9008-42203f2a5809" height="400"></img>
</div>

Search for Group

<div align="center">
<img src="https://github.com/user-attachments/assets/eb1c4361-ad03-400a-b899-a782d7a2c3de" height=""></img>
</div>

Click on Edit icon look like a pencil

<div align="center">
<img src="https://github.com/user-attachments/assets/cbb310fd-445a-4970-b385-45d1b3408a32" height=""></img>
</div>


Add this rule at group agent.conf file form wazuh dashboard

```xml
<localfile>
  <location>Microsoft-Windows-Windows Defender/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

<div align="center">
<img src="https://github.com/user-attachments/assets/d48aba16-881e-4687-a6c5-cf9805c98b59" height="250"></img>
</div>

