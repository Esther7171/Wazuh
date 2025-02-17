## Copy past this command and It only Change the password of existing User.
```
sudo bash /usr/share/wazuh-indexer/plugins/opensearch-security/tools/wazuh-passwords-tool.sh -u admin -p password@123
```
## Restart Service
```
systemctl restart filebeat
systemctl restart wazuh*
```
