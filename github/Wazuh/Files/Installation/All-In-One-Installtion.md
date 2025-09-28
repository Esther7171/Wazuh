# Installing the wazuh All In One Installation.

> **Note**: You need root user privileges to run all the commands described below.

---

### Download this commond utils:
```
sudo apt -y install curl wget nano
```

### Step 1: Create a Directory for Installtion files.
Organize all installtion files in a dedicated directory:

```bash
mkdir wazuh-install
cd wazuh-install
```

---

### Step 2: Initail configuration
Set up your deployment configuration, generate SSL certificates, and create secure random passwords.

### Download the Installtion Assitant and Configuration File:

```bash
curl -sO https://packages.wazuh.com/4.11/wazuh-install.sh
curl -sO https://packages.wazuh.com/4.11/config.yml
```

### Run and Install

```
sudo bash wazuh-install.sh -a 
```

* `-a`: it stand for all.

### After the installtion is complete at the end u will get the id and pass of dashboard.
---