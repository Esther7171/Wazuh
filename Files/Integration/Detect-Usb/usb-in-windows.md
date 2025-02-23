```C:\Program Files (x86)\ossec-agent\local_internal_options.conf```

```
logcollector.remote_commands=1
```
### Restart wazuh

```
sudo nano /var/ossec/etc/shared/default/agent.conf
```
```
<agent_config os="Windows">
  <localfile>
    <log_format>command</log_format>
    <command>reg QUERY HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR</command>
    <alias>check_usb_connetivity</alias>
  </localfile>
</agent_config>
```

https://documentation.wazuh.com/current/user-manual/capabilities/command-monitoring/use-cases/detect-usb-storage.html

```
logcollector.remote_commands=1
```

```
test
```
