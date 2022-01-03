#!/bin/bash

FW_PATH=../../modules/dias-firewall/
DEB_DIR_PATH=../../toolchain/services/diasfw-service/DIASFirewall_1.0-1/
sudo apt install python3-pip g++ libexpat-dev libconfig-dev can-utils

sudo pip3 install setuptools wheel tqdm twine

cd $FW_PATH

source build.sh core

cp /usr/lib/libfwcore.so $DEB_DIR_PATH/usr/lib/

cp Build/* $DEB_DIR_PATH/usr/local/bin/diasfw/

cp diasfw.cfg $DEB_DIR_PATH/etc/diasfw/diasfw.cfg

cp FWRules.xml $DEB_DIR_PATH/etc/diasfw/FWRules.xml

cp Utils/config.py $DEB_DIR_PATH/etc/diasfw/config.py

cp Utils/pyc_logger.py $DEB_DIR_PATH/usr/lib/python3/dist-packages/pycan/
cp Utils/pycan_msg.py $DEB_DIR_PATH/usr/lib/python3/dist-packages/pycan/
cp Utils/pycan_com.py $DEB_DIR_PATH/usr/lib/python3/dist-packages/pycan/

cp Utils/pycan_rec.py $DEB_DIR_PATH/usr/local/bin/diasfw/
cp Utils/pyclient_mqtt.py $DEB_DIR_PATH/usr/local/bin/diasfw/

cd $DEB_DIR_PATH/..

sudo dpkg -b ./DIASFirewall_1.0-1 ./DIASFirewall_1.0-1_amd64.deb

sudo dpkg -i ./DIASFirewall_1.0-1_amd64.deb