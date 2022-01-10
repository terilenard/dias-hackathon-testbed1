#!/bin/bash

cd ../services/vcan0-service

sudo cp vcan0.sh /bin/vcan0.sh

sudo chmod 744 /bin/vcan0.sh

sudo chown $USER:$USER /bin/vcan0.sh

sudo cp etc/modules-load.d/can.conf /etc/modules-load.d/

sudo cp etc/systemd/network/vcan0.netdev /etc/systemd/network/

sudo cp etc/systemd/network/80-vcan.network /etc/systemd/network/

sudo systemctl enable systemd-networkd

sudo systemctl restart systemd-networkd
