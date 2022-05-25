#!/bin/bash

if [ $# -lt 1 ]
then
  echo "Invalid argument".
  echo "Arg 1: (s)ender, (r)eciever"
  exit 1
fi

# Stop the mixcan service
sudo systemctl disable mixcan
sudo systemctl stop mixcan

# Dependencies
pip3 install paho-mqtt python-can

# Create directories
MIXCAN_PATH=../../modules/dias-mixcan/python/
SERVICE_PATH=../../../toolchain/services/mixcan-service
cd $MIXCAN_PATH

sudo mkdir -p /usr/lib/python3/dist-packages/mixcan/
sudo mkdir -p /etc/mixcan/
sudo mkdir -p /etc/mixcan/keys
sudo mkdir -p /var/log/mixcan

# Permissions
sudo chown -R $USER:$USER /var/log/mixcan/
sudo chown -R $USER:$USER /etc/mixcan/
sudo chown -R $USER:$USER /etc/mixcan/keys/

# Source Scripts
sudo cp mixcan.py /usr/lib/python3/dist-packages/mixcan/mixcan.py
sudo cp client_mqtt.py /usr/lib/python3/dist-packages/mixcan/client_mqtt.py
sudo cp manager.py /usr/lib/python3/dist-packages/mixcan/manager.py
sudo cp pycan.py /usr/lib/python3/dist-packages/mixcan/pycan.py
sudo cp logger.py /usr/lib/python3/dist-packages/mixcan/logger.py
sudo cp utils.py /usr/lib/python3/dist-packages/mixcan/utils.py

# Initial Key
sudo cp last_key.dat /etc/mixcan/keys/last_key.dat

# Configuration
if [ "$1" == "s" ]; then
    echo "Installing sender version"
    sudo cp config.ini /etc/mixcan/config.ini
elif [ "$1" == "r" ]; then
    echo "Installing reciever version"
    sudo cp recv_config.ini /etc/mixcan/config.ini
else
    echo "Invalid argument"
fi

# Service
sudo cp $SERVICE_PATH/mixcan.service /lib/systemd/system/mixcan.service
sudo sed -i "/User=/c\User=$USER" /lib/systemd/system/mixcan.service

sudo systemctl enable mixcan
sudo systemctl start mixcan









