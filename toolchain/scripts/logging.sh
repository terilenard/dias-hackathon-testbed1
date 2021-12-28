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
pip3 install pyzmq blist

# Service setup + Bootstrap
sudo cp  ../services/tpm-logger-service/tpm-logger.service /usr/local/lib/systemd/system/tpm-logger.service

sudo sed -i "/User=/c\User=$USER" /usr/local/lib/systemd/system/tpm-logger.service

sudo sed -i "/Group=/c\Group=$USER" /usr/local/lib/systemd/system/tpm-logger.service

cd ../../modules/dias-logging/src/bootstrap

python3 bootstrap_tpm.py --provision_generator --path /etc/dias-logging/bin --out_pub key.pub --out_priv key.priv 1&>/dev/null

cd ..

sudo cp handlers.py  __init__.py  tpm_logger.py utils.py wrapper.py /usr/lib/python3/dist-packages/dias-logging

sudo cp config.ini /etc/dias-logging/

sudo systemctl enable tpm-logger.service

sudo systemctl start tpm-logger.service


