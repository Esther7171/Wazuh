Step 1 Installing the Wazuh indexer using the assisted installation method

Note You need root user privileges to run all the commands described below.

Create a directory to arrange all the files
```
mkdir wazuh-install
cd wazuh-install
```
1. Initial configuration
Indicate your deployment configuration, create the SSL certificates to encrypt communications between the Wazuh components, and generate random passwords to secure your installation.

Download the Wazuh installation assistant and the configuration file.
```
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
curl -sO https://packages.wazuh.com/4.9/config.yml
```
2. Edit `config.yml` and replace the node names and IP values with the corresponding names and IP addresses. You need to do this for all Wazuh server, Wazuh indexer, and Wazuh dashboard nodes. Add as many node fields as needed.
```yml
nodes:
  # Wazuh indexer nodes
  indexer:
    - name: node-1
      ip: "10.10.10.10"
    #- name: node-2
    #  ip: "<indexer-node-ip>"
    #- name: node-3
    #  ip: "<indexer-node-ip>"

  # Wazuh server nodes
  # If there is more than one Wazuh server
  # node, each one must have a node_type
  server:
    - name: wazuh-1
      ip: "10.10.10.10"
    #  node_type: master
    #- name: wazuh-2
    #  ip: "<wazuh-manager-ip>"
    #  node_type: worker
    #- name: wazuh-3
    #  ip: "<wazuh-manager-ip>"
    #  node_type: worker

  # Wazuh dashboard nodes
  dashboard:
    - name: dashboard
      ip: "10.10.10.10"
```
3. If You are Using `static public Ip` u need to prefrom some changes on the script , else u can skip this:
Just comment Out or delete this code, it will allow u to use `public ip`.
```yml
        for ip in "${all_ips[@]}"; do
            isIP=$(echo "${ip}" | grep -P "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$")
            if [[ -n "${isIP}" ]]; then
                if ! cert_checkPrivateIp "$ip"; then
                    common_logger -e "The IP ${ip} is public."
                    exit 1
                fi
            fi
        done
```
<div align="center">
  <img src="https://github.com/user-attachments/assets/84040969-831b-414e-8843-5b35dad2308a"></img>
</div>
