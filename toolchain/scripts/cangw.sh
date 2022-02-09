#!/bin/bash

#if [ $# -lt 2 ]
#then
#    echo "Invalid arguments."
#    echo "Please give 2 CAN interfaces (e.g., can0, vcan0),
#    to set up a gateway"
#    exit 1
#fi

sudo apt install can-utils

sudo modprobe can-gw

cd ../toolchain/services/cangw-service

sudo cp cangw-in.service /etc/systemd/system/cangw-in.service

sudo cp cangw-out.service /etc/systemd/system/cangw-out.service

sudo sed -i "/User=/c\User=$USER" /etc/systemd/system/cangw-in.service

sudo sed -i "/Group=/c\Group=$USER" /etc/systemd/system/cangw-in.service

sudo sed -i "/User=/c\User=$USER" /etc/systemd/system/cangw-out.service

sudo sed -i "/Group=/c\Group=$USER" /etc/systemd/system/cangw-out.service

sudo systemctl enable cangw-in.service
sudo systemctl enable cangw-out.service

sudo systemctl start cangw-in.service
sudo systemctl start cangw-out.service