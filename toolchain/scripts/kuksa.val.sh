#!/bin/bash

echo "Installing dependencies"

sudo apt install -y cmake python3-pip

sudo apt install -y libblkid-dev e2fslibs-dev libboost-all-dev libaudit-dev libssl-dev mosquitto libmosquitto-dev libglib2.0-dev build-essential

cd ../../modules/kuksa.val/kuksa-val-server

git submodule update --init --recursive

mkdir build

cd build

cmake ..

make

sudo mkdir /usr/bin/kuksa.val

cd src/

sudo cp kuksa-val-server /usr/bin/kuksa.val/

sudo mkdir /etc/kuksa.val

sudo chown -R $USER:$USER /etc/kuksa.val/

sudo cp config.ini CA.pem Client.key Client.pem jwt.key.pub Server.key Server.pem vss_release_2.2.json /etc/kuksa.val/

cd ../../../../../toolchain/services/kuksa.val-service

sudo cp kuksa.val.service /etc/systemd/system/

sudo sed -i "/User=/c\User=$USER" /etc/systemd/system/kuksa.val.service

sudo sed -i "/Group=/c\Group=$USER" /etc/systemd/system/kuksa.val.service

sudo systemctl enable kuksa.val.service

sudo systemctl start kuksa.val.service
