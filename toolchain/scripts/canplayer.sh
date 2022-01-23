#!/bin/bash

sudo apt install can-utils

if [ $# -lt 1 ]
then
  echo "Invalid arguments".
  echo "Arg 1: CAN log file to be replayed."
  echo "Arg 2 (optional): the CAN interface from which the CAN log file was captured"
  exit 1
fi


sudo mkdir /bin/can-player
sudo chown $USER:$USER /bin/can-player

sudo mkdir /var/log/can-player
sudo chown $USER:$USER /var/log/can-player
cat $1 > /var/log/can-player/dias.log

cd ../services/canplayer-service

cp can-player.sh /bin/can-player/
sudo cp can-player.service /etc/systemd/system/can-player.service


cp can-player.sh /bin/can-player

sudo sed -i "/User=/c\User=$USER" /etc/systemd/system/can-player.service
sudo sed -i "/Group=/c\Group=$USER" /etc/systemd/system/can-player.service


if [ $# -eq 2 ]
then
  sudo sed -i "/ExecStart=/c\ExecStart=/bin/can-player/can-player.sh /var/log/can-player/dias.log $2" /etc/systemd/system/can-player.service
fi

sudo systemctl enable can-player.service
sudo systemctl start can-player.service

