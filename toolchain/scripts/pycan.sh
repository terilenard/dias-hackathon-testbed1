#!/bin/bash

PYCAN_PATH=../../modules/pycan/
SERVICE_PATH=../../toolchain/services/pycan-service/

cd $PYCAN_PATH

sudo mkdir -p /usr/lib/python3/dist-packages/pycan/
sudo mkdir -p /etc/pycan/

sudo cp pycan.py /usr/lib/python3/dist-packages/pycan/pycan.py
sudo cp pycan.cfg /etc/pycan/pycan.cfg

sudo cp $SERVICE_PATH/pycan.service /lib/systemd/system/pycan.service

sudo sed -i "/User=/c\User=$USER" /lib/systemd/system/pycan.service

sudo systemctl enable pycan
sudo systemctl start pycan
