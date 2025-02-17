#!/bin/bash

# You just need to run this script It will install all necessary components
# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
    echo -e "\e[1;31m This script must be run as root, login to root shell or it will break pkg. Exiting.\e[0m"
    exit 1
fi

# Spinner function
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Function to install packages
install_package() {
    local package=$1
    echo -e "\e[32m[*] Installing $package...\e[0m"
    sudo apt install -y "$package" &> /dev/null &
    spinner $!
    if [ $? -eq 0 ]; then
        echo -e "\e[32m[✔] $package installed successfully.\e[0m"
    else
        echo -e "\e[31m[✘] Failed to install $package.\e[0m"
    fi
}

# Main script
echo "Installing Required Packages..."
install_package "git"
install_package "curl"
install_package "figlet"
install_package "python*"
install_package "docker.io"

echo -e "\e[32mDone! All required packages have been installed.\e[0m"

clear
figlet "Wazuh Setup Begins"
sleep 1

mkdir -p /root/wazuh-all
cd /root/wazuh-all || { echo "Error: Unable to create /root/wazuh-all"; exit 1; }

clear
echo -e "\e[1;31m_______________________________________________\e[0m" # Red
echo ""
echo -e "\e[7;1;5;31m Increase max_map_count on your Docker host \e[0m"
echo -e "\e[1;31m_______________________________________________\e[0m"
echo ""
sleep 1
sysctl -w vm.max_map_count=262144
clear

echo -e "\e[1;31m__________________________\e[0m" 
echo ""
echo -e "\e[1;31m Start the Docker service \e[0m" 
echo -e "\e[1;31m__________________________\e[0m" 
echo ""
sleep 1
systemctl start docker
clear

echo -e "\e[1;31m_______________________________________\e[0m" 
echo ""
echo -e "\e[1;31m Changing Docker User-Group Permission \e[0m" 
echo -e "\e[1;31m_______________________________________\e[0m" 
usermod -aG docker "$USER"
sleep 0.5
clear

echo -e "\e[1;31m____________________________\e[0m" 
echo -e "\e[1;31m Downloading Docker Compose \e[0m" 
echo -e "\e[1;31m____________________________\e[0m" 
curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /root/docker-compose
sleep 0.5
clear

echo -e "\e[1;31m_____________________\e[0m" 
echo ""
echo -e "\e[1;31m Changing Permission \e[0m" 
echo -e "\e[1;31m_____________________\e[0m" 
chmod +x /root/docker-compose
sleep 0.5
clear

echo -e "\e[1;31m____________________________________\e[0m" 
echo ""
echo -e "\e[1;31m Moving Docker-compose to /usr/local/bin \e[0m" 
echo -e "\e[1;31m____________________________________\e[0m" 
mv /root/docker-compose /usr/local/bin/docker-compose
sleep 0.5
clear

echo -e "\e[1;31m____________________________\e[0m" 
echo ""
echo -e "\e[1;31m Cloning Wazuh Docker Repository \e[0m" 
echo -e "\e[1;31m____________________________\e[0m" 

git clone https://github.com/wazuh/wazuh-docker.git -b v4.9.2
sleep 0.5
clear

# Prompt user for input
read -p "Would you like Single or Multi (S/M) => " nodex

# Convert input to lowercase for case-insensitivity
nodex=$(echo "$nodex" | tr '[:upper:]' '[:lower:]')

# Define base directory
BASE_DIR="/root/wazuh-all/wazuh-docker"

if [[ "$nodex" == "s" ]]; then
    cd "$BASE_DIR/single-node" || { echo "Error: Directory not found."; exit 1; }
    docker-compose -f generate-indexer-certs.yml run --rm generator
    docker-compose up -d
    echo -e "\e[1;7;32m All done! Single Node has been deployed. All the files are in /root directory. \e[0m" 

elif [[ "$nodex" == "m" ]]; then
    cd "$BASE_DIR/multi-node" || { echo "Error: Directory not found."; exit 1; }
    docker-compose -f generate-indexer-certs.yml run --rm generator
    docker-compose up -d
    echo -e "\e[1;7;32m All done! Multi Node has been deployed. All the files are in /root directory. \e[0m" 

else
    echo -e "\e[31mInvalid option. Please choose 'S' for Single or 'M' for Multi.\e[0m"
fi
