#!/bin/bash

#cd ~
#cat ~/.ssh/hassio.pub | cat >> ~/.ssh/authorized_keys

#chmod 700 .ssh
#chmod 600 .ssh/authorized_keys

#sudo apt-get install mc nano htop bmon

#sudo usermod -aG homeassistant $USER

#sudo chmod -R g+rwX /home/homeassistant

#yes | cp -rf ~/cfg/* /home/homeassistant/.homeassistant/

#sudo chown -R homeassistant:homeassistant /srv/homeassistant

#sudo apt-get install vlc
#sudo usermod -a -G audio homeassistant

#sudo systemctl restart home-assistant@homeassistant

#install hassctl
#sudo curl -o /usr/local/bin/hassctl https://raw.githubusercontent.com/dale3h/hassctl/master/hassctl && sudo chmod +x /usr/local/bin/hassctl

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