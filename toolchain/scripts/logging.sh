#!/bin/bash

# Create directories
sudo mkdir -p /var/log/dias-logging/

sudo mkdir -p /etc/tpm_handlers/dias-logging/

sudo mkdir /usr/lib/python3/dist-packages/dias-logging

# Log file
sudo touch /var/log/dias-logging/info.log

# Permissions
sudo chown -R $USER:$USER /var/log/dias-logging/

sudo chown -R $USER:$USER /etc/tpm_handlers/dias-logging/

# Dependencies
pip3 install blist paho-mqtt

# Service setup
sudo cp  ../services/dias-logging-service/dias-logging.service /etc/systemd/system/dias-logging.service

sudo sed -i "/User=/c\User=$USER" /etc/systemd/system/dias-logging.service

sudo sed -i "/Group=/c\Group=$USER" /etc/systemd/system/dias-logging.service

cd ../../modules/dias-logging/src/bootstrap

cd ..

sudo cp log.py client_mqtt.py handlers.py  __init__.py  tpm_logger.py utils.py wrapper.py /usr/lib/python3/dist-packages/dias-logging
sudo sed -i "/handler =/c\handler = logging.FileHandler(\"/var/log/dias-logging/info.log\")" /usr/lib/python3/dist-packages/dias-logging/log.py
sudo cp config.ini /etc/dias-logging/

sudo systemctl enable dias-logging.service

sudo systemctl start dias-logging.service


