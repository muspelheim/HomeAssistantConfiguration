#!/bin/bash

#sudo apt-get install vlc

#install MQTT broker
#wget 'http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key' -O ./mosquitto-repo.gpg.key -q && sudo apt-key add ./mosquitto-repo.gpg.key
#echo "deb http://repo.mosquitto.org/debian jessie main"  | sudo tee -a /etc/apt/sources.list.d/mosquitto.list

#sudo apt-get update && sudo apt-get install -y mosquitto mosquitto-clients
#sudo touch /etc/mosquitto/passwd
#sudo mosquitto_passwd -b /etc/mosquitto/passwd hassio MQTT_PASSWORD
#echo "allow_anonymous false"  | sudo tee -a /etc/mosquitto/conf.d/default.conf
#echo "password_file /etc/mosquitto/passwd"  | sudo tee -a /etc/mosquitto/conf.d/default.conf
#sudo systemctl restart mosquitto
#sudo apt-get install net-tools nmap

echo "# Pair Bluetooth devices\n/home/homeassistant/.homeassistant/scripts/pair_bluetooth.sh\nexit 0" >> /etc/rc.local
