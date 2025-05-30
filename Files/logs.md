## 📄 Types of Logs in Windows

### 1. **Event Logs (via Event Viewer)**

Windows stores most system, security, and application activity in structured event logs.

| Log Type             | Description                                                                            | Common Source       |
| -------------------- | -------------------------------------------------------------------------------------- | ------------------- |
| **System**           | Logs generated by Windows system components (e.g., services, drivers)                  | OS Kernel, Services |
| **Application**      | Logs from installed applications                                                       | App-specific        |
| **Security**         | Logs related to logon events, policy changes, privilege use (auditing must be enabled) | LSASS, Audit Policy |
| **Setup**            | Events related to application installations and system setup                           | Windows Setup       |
| **Forwarded Events** | Logs forwarded from other systems using event subscriptions                            | Other Windows Hosts |

---

### 2. **Windows Sysmon Logs (via Sysinternals Sysmon)**

| Log Type                | Description                                                              |
| ----------------------- | ------------------------------------------------------------------------ |
| **Process Creation**    | Logs every process creation with hash and parent/child PID relationships |
| **Network Connections** | Outbound TCP/UDP connections initiated by a process                      |
| **Image Load**          | DLLs and EXEs loaded by processes                                        |
| **File Creation Time**  | File creation with timestamp                                             |
| **Registry Events**     | Registry key/value create/delete/modify                                  |
| **Clipboard Events**    | Clipboard activity logging (if enabled)                                  |
| **WMI Events**          | WMI script execution tracking                                            |
| **Driver Load Events**  | Monitors kernel-mode driver loading                                      |
| **Pipe Events**         | Named pipe creation and connection                                       |

---

### 3. **Windows Defender Logs**

| Log Type              | Description                                    |
| --------------------- | ---------------------------------------------- |
| **Protection Events** | Malware detections, quarantines, block actions |
| **Scan Results**      | On-demand or scheduled scan summaries          |
| **Engine Updates**    | Signature and engine update statuses           |

---

### 4. **IIS Logs (for Web Servers)**

If IIS is enabled:

| Log Type        | Description                                                    |
| --------------- | -------------------------------------------------------------- |
| **Access Logs** | HTTP requests, user IP, method, response code                  |
| **Error Logs**  | Application or server errors (e.g., 500 Internal Server Error) |

---

### 5. **PowerShell Logs**

| Log Source                                                       | Description                                           |
| ---------------------------------------------------------------- | ----------------------------------------------------- |
| **Operational Log** (`Microsoft-Windows-PowerShell/Operational`) | Records script block logging, command line use        |
| **Transcript Logs**                                              | Plaintext history of PowerShell sessions (if enabled) |

---

### 6. **Task Scheduler Logs**

| Log Type             | Description                           |
| -------------------- | ------------------------------------- |
| **Operational Logs** | Success/failure of scheduled tasks    |
| **History Tab**      | Per-task history in Task Scheduler UI |

---

### 7. **Windows Firewall Logs**

| Log Type            | Description                          |
| ------------------- | ------------------------------------ |
| **Connections Log** | Inbound/outbound connection activity |
| **Packet Dropping** | Dropped packets by firewall rules    |

> Location: `C:\Windows\System32\LogFiles\Firewall\pfirewall.log`

---

### 8. **DNS Logs (If DNS Server Role is Enabled)**

| Log Type               | Description                        |
| ---------------------- | ---------------------------------- |
| **Query Logs**         | Resolved/unresolved DNS queries    |
| **Zone Transfer Logs** | Zone transfers between DNS servers |

---

### 9. **Audit Logs (via Local Group Policy)**

Once auditing is enabled (under `secpol.msc` or `gpedit.msc`):

| Log Type                | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| **Logon/Logoff Events** | Interactive, network, or RDP logins                  |
| **Object Access**       | File, folder, registry access tracking               |
| **Policy Changes**      | Security settings, user rights, audit policy changes |
| **Privilege Use**       | Administrative or elevated task tracking             |
| **Process Tracking**    | Process start, end, and command-line details         |

