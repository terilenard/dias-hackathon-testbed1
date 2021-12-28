#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Invalid arguments"
    echo "Expected local_port remote_ip remote_port"
    exit
fi

sudo pip3 install setuptools

sudo add-apt-repository -y ppa:lely/ppa

sudo apt update

sudo apt install -y autoconf automake libtool make g++ python3-pip liblely-io-dev

cd ../../dependencies/lely-core

autoreconf -i

./configure --disable-cython

make

sudo make install

cd ../../toolchain/services/can2udp-service

sudo cp can2udp.service /usr/local/lib/systemd/system/can2udp.service

sudo sed -i "/User=/c\User=$USER" /usr/local/lib/systemd/system/can2udp.service

sudo sed -i "/Group=/c\Group=$USER" /usr/local/lib/systemd/system/can2udp.service

sudo sed -i "/ExecStart=/c\ExecStart=/usr/local/bin/can2udp -D -fp $1 vcan0 $2 $3" /usr/local/lib/systemd/system/can2udp.service

sudo systemctl enable can2udp.service

sudo systemctl start can2udp.service
