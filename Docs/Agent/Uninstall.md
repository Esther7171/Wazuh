# Uninstalling the Wazuh agent form Agent side
> ### Windows Wazuh agent
#### ```Disable the wazuh service```
#### ```Delete this folder in C Drive```
```
C:\Program Files (x86)\ossec-agent
```

> ### Linux Wazuh agent
#### ```Disable the Service```
```
systemctl disable wazuh-agent
systemctl daemon-reload
```
#### ```Remove the Wazuh agent installation.```
##### ```yum```
```
yum remove wazuh-agent
```
##### ```apt```
```
apt-get remove wazuh-agent -y
apt-get remove --purge wazuh-agent -y
```

### Uninstalling the Wazuh agent form Server side
#### Copy past this
```
/var/ossec/bin/manage_agents
```
### U will get this prompt
```
wazuh@wazuh:~$ sudo /var/ossec/bin/manage_agents


****************************************
* Wazuh v4.9.2 Agent manager.          *
* The following options are available: *
****************************************
   (A)dd an agent (A).
   (E)xtract key for an agent (E).
   (L)ist already added agents (L).
   (R)emove an agent (R).
   (Q)uit.
Choose your action: A,E,L,R or Q:
```
#### Press R/r
```
wazuh@wazuh:~$ sudo /var/ossec/bin/manage_agents


****************************************
* Wazuh v4.9.2 Agent manager.          *
* The following options are available: *
****************************************
   (A)dd an agent (A).
   (E)xtract key for an agent (E).
   (L)ist already added agents (L).
   (R)emove an agent (R).
   (Q)uit.
Choose your action: A,E,L,R or Q: r

Available agents:
   ID: 001, Name: windows-test, IP: any
   ID: 002, Name: on-ubuntu, IP: any
Provide the ID of the agent to be removed (or '\q' to quit):
```
### Give the id of agent u wanna remove