#!/bin/bash

# tpm2-tss dependencies
sudo apt -y install autoconf-archive libcmocka0 libcmocka-dev procps iproute2 build-essential git pkg-config gcc libtool automake libssl-dev uthash-dev autoconf doxygen libjson-c-dev libini-config-dev libcurl4-openssl-dev acl

# tpm2-tools dependencies
sudo apt-get -y install pandoc autoconf automake libtool pkg-config gcc libssl-dev libcurl4-gnutls-dev python-yaml uuid-dev

# tpm2-abrmd
sudo apt -y install libglib2.0-dev

# User for abrmd
sudo useradd --system --user-group tss

# Compile tpm2-tss
cd ../../dependencies/tpm2-tss/

./bootstrap

./configure

make -j4

sudo make install

sudo ldconfig

# Compile tpm2-tools
cd ../tpm2-tools-4.3.2/

./bootstrap

./configure

make

sudo make install

# compile tpm2-abrmd
cd ../tpm2-abrmd

./bootstrap

./configure

make

sudo make install

sudo ldconfig

sudo pkill -HUP dbus-daemon

sudo cp dist/tpm2-abrmd.conf /etc/dbus-1/system.d/tpm2-abrmd.conf 

# Compile ibmtss

cd ../ibmtss/src

make

sudo make install

cd ../../../toolchain/services/ibmtss-service

sudo cp ibmtss.service /etc/systemd/system/ibmtss.service

cd ../tpm2-abrmd

sudo cp tpm2-abrmd.service /etc/systemd/system/tpm2-abrmd.service

sudo systemctl enable ibmtss.service

sudo systemctl enable tpm2-abrmd.service

sudo systemctl daemon-reload

sudo systemctl start ibmtss.service

sudo systemctl restart tpm2-abrmd.service
