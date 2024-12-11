#!/bin/bash

sudo apt update
sudo apt install -y apt-transport-https
sudo apt install openjdk-11-jdk -y
clear
echo "Checking java version"
sleep 3
java -version
echo "JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"" | sudo tee -a /etc/environment
source /etc/environment
clear
echo $JAVA_HOME
echo "checking env of java"
sleep 3 
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update
sudo apt-get install elasticsearch
sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch
sudo systemctl status elasticsearch
sleep 3
clear
echo "copy ip u have 10 sec and past that ip in network column and discovery.seed_hosts: []"
sleep 3
ifconfig 
sleep 10
sudo nano /etc/elasticsearch/elasticsearch.yml
sudo systemctl restart elasticsearch
