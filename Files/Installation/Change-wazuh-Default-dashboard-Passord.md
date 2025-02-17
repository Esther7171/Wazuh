# 🔐 Wazuh Admin Password Reset & Service Restart Guide  

This guide provides instructions to securely reset the Wazuh admin password and restart essential services.  

---

## 🚀 Reset Wazuh Admin Password  

To update the password for an existing Wazuh user (e.g., `admin`), execute the following command:  

```bash
sudo bash /usr/share/wazuh-indexer/plugins/opensearch-security/tools/wazuh-passwords-tool.sh -u admin -p NewSecurePassword123
```

🔹 **Replace `NewSecurePassword123` with a strong and secure password.**  

---

## 🔄 Restarting Wazuh Services  

After changing the password, restart the necessary services to apply the changes:  

```bash
systemctl restart filebeat
systemctl restart wazuh*
```

This ensures that Wazuh components function correctly with the updated credentials.  

---

## ⚠️ Security Recommendations  

✔️ Use a **strong and unique** password.  
✔️ Follow **best security practices** when managing credentials.  
✔️ Restrict access to administrative commands to **authorized users only**.  

---

📌 **Need Help?** If you encounter any issues, feel free to open an **issue** in this repository!  
```
