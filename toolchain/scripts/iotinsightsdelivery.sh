#!/bin/bash

NODE_MODULES=/usr/lib/node-modules
TELEMETRY_DELIVERER=telemetry-deliverer
LOG_DELIVERER=log-deliverer
SRC_PATH=../../modules/bosch-iot-insights-delivery

curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -

sudo apt update

sudo apt install nodejs

sudo npm install --global yarn

# Directories

sudo mkdir $NODE_MODULES

sudo mkdir $NODE_MODULES/$TELEMETRY_DELIVERER

sudo mkdir $NODE_MODULES/$LOG_DELIVERER

sudo chown -R $USER:$USER $NODE_MODULES $NODE_MODULES/$TELEMETRY_DELIVERER $NODE_MODULES/$LOG_DELIVERER

cd $SRC_PATH

cp * $NODE_MODULES/$TELEMETRY_DELIVERER
cp * $NODE_MODULES/$LOG_DELIVERER

sed -i "/  topic: process.env.MQTT_TOPIC ?? 'telemetry',/c\  topic: process.env.MQTT_TOPIC ?? 'log_events'," $NODE_MODULES/$LOG_DELIVERER/index.js

cd ../../toolchain/services/delivery-service
sudo cp delivery.service /etc/systemd/system/$TELEMETRY_DELIVERER.service
sudo cp delivery.service /etc/systemd/system/$LOG_DELIVERER.service

sudo sed -i "/ExecStart=/c\ExecStart=yarn --cwd /usr/lib/node-modules/$TELEMETRY_DELIVERER/ start" /etc/systemd/system/$TELEMETRY_DELIVERER.service
sudo sed -i "/ExecStart=/c\ExecStart=yarn --cwd /usr/lib/node-modules/$LOG_DELIVERER/ start" /etc/systemd/system/$LOG_DELIVERER.service

cd $NODE_MODULES/$TELEMETRY_DELIVERER
yarn install

cd ../$LOG_DELIVERER
yarn install

sudo systemctl enable $TELEMETRY_DELIVERER.service
sudo systemctl enable $LOG_DELIVERER.service
