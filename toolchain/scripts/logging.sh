#!/bin/bash

# Create directories
sudo mkdir -p /var/log/dias-logging/

sudo mkdir -p /etc/dias-logging/bin/

sudo mkdir /usr/lib/python3/dist-packages/dias-logging

# Log files
sudo touch /var/log/dias-logging/tpm_logger.log

sudo touch /var/log/dias-logging/info.log

# Permissions
sudo chown -R $USER:$USER /var/log/dias-logging/

sudo chown -R $USER:$USER /etc/dias-logging/

# Dependencies
pip3 install blist paho-mqtt

# Service setup + Bootstrap
sudo cp  ../services/dias-logging-service/dias-logging.service /etc/systemd/system/dias-logging.service

sudo sed -i "/User=/c\User=$USER" /etc/systemd/system/dias-logging.service

sudo sed -i "/Group=/c\Group=$USER" /etc/systemd/system/dias-logging.service

cd ../../modules/dias-logging/src/bootstrap

python3 bootstrap_tpm.py --provision_generator --path /etc/dias-logging/bin --out_pub key.pub --out_priv key.priv

cd ..

sudo cp client_mqtt.py handlers.py  __init__.py  tpm_logger.py utils.py wrapper.py /usr/lib/python3/dist-packages/dias-logging

sudo cp config.ini /etc/dias-logging/

sudo systemctl enable dias-logging.service

sudo systemctl start dias-logging.service


