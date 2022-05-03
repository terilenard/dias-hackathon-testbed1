#!/bin/bash

if [ $# -lt 4 ]
then
  echo "Invalid arguments".
  echo "Arg 1: Cloudfeeder username."
  echo "Arg 2: Cloudfeeder password"
  echo "Arg 3: Logger username."
  echo "Arg 4: Logger password"
  echo "Arg 5: Mixcan username"
  echo "Arg 6: Mixcan password"
  exit 1
fi

sudo apt install mosquitto

sudo sed -i "/After=/c\After=After=kuksa.val.service\nRequires=kuksa.val.service\nBefore=cloudfeeder.service" /usr/lib/systemd/system/mosquitto.service

sudo touch /etc/mosquitto/passwords
sudo echo "$1:$2" >> /etc/mosquitto/passwords
sudo echo "$3:$4" >> /etc/mosquitto/passwords
sudo echo "$5:$6" >> /etc/mosquitto/passwords

sudo mosquitto_passwd -U /etc/mosquitto/passwords

sudo echo -e "\npassword_file /etc/mosquitto/passwords " >> /etc/mosquitto/mosquitto.conf

sudo systemctl daemon-reload

sudo systemctl restart mosquitto
