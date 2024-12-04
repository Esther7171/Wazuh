#!/bin/bash

# You just need to run this script It will install all necessary components
# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
    echo -e "\e[1;31m This script must be run as root, login to root shell or it will break pkg. Exiting.\e[0m"
    exit 1
fi
Install_all_pkg (){
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
install_package "lolcat"
install_package "python*"
echo -e "\e[32mDone! All required packages have been installed.\e[0m"
}

Install_all_pkg 

mkdir /home/$USER/wazuh-all
cd /home/$USER/wazuh-all 

clear
echo -e "\e[1;31m_______________________________________________\e[0m" #red
echo ""
echo -e "\e[7;1;5;31m Increase max_map_count on your Docker host\e[0m"
echo -e "\e[1;31m_______________________________________________\e[0m
sleep 0.5
sudo sysctl -w vm.max_map_count=262144
clear

echo "__________________________" | lolcat
echo ""
echo " Start the Docker service " | lolcat
echo "__________________________" | lolcat
sleep 0.5
sudo systemctl start docker
clear

echo "_______________________________________" | lolcat
echo ""
echo " Changing Docker User-Group Permission " | lolcat
echo "_______________________________________" | lolcat
usermod -aG docker
sleep 0.5
clear

echo "____________________________" | lolcat
echo " Downloading Docker compose " | lolcat
echo "____________________________" | lolcat
curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /home/$USER/docker-compose
sleep 0.5
clear

echo "_____________________" | lolcat
echo ""
echo " Changing Permission " | lolcat
echo "_____________________" | lolcat
sudo chmod +x /home/$USER/docker-compose
sleep 0.5
clear

echo "____________________________________" | lolcat
echo ""
echo " Moving Docker-compose to Local/bin " | lolcat
echo "____________________________________" | lolcat
sudo mv /home/$USER/docker-compose /usr/local/bin/
sleep 0.5
clear

echo "____________________________" | lolcat
echo ""
echo " Copying Wazuh Docker Image " | lolcat
echo "____________________________" | lolcat

git clone https://github.com/wazuh/wazuh-docker.git -b v4.9.2
sleep 0.5
clear

read -p "Would you like Single or Multi (S/M): " nodex

# Convert input to lowercase for case-insensitivity
nodex=$(echo "$nodex" | tr '[:upper:]' '[:lower:]')

if [[ "$nodex" == "s" ]]; then
    cd  /home/$USER/wazuh-all/wazuh-docker/single-node || exit
    docker-compose -f generate-indexer-certs.yml run --rm generator
    docker-compose up -d
    echo "All done! Single Node has been deployed." | lolcat

elif [[ "$nodex" == "m" ]]; then
    cd  /home/$USER/wazuh-all/wazuh-docker/multi-node || exit
    docker-compose -f generate-indexer-certs.yml run --rm generator
    docker-compose up -d
    echo "All done! Multi Node has been deployed." | lolcat

else
    echo "Wrong option. Please choose 'S' for Single or 'M' for Multi."
fi
