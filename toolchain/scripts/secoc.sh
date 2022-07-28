#!/bin/bash
sudo apt install python3-pip

sudo pip3 install paho-mqtt j1939 pycryptodome cantools py_expression_eval serial websockets==8.1 kuksa_viss_client

# Source files
SOURCES=/usr/lib/python3/dist-packages/secoc/
sudo mkdir $SOURCES

# Logging files
sudo mkdir /var/log/dbcfeeder
sudo chown $USER:$USER /var/log/dbcfeeder

touch /var/log/dbcfeeder/info.log
touch /var/log/dbcfeeder/error.log

# Config files
sudo mkdir /etc/dbcfeeder/
sudo chown $USER:$USER /etc/dbcfeeder/

# Copy source files
cd ../../modules/secoc/kuksa_feeders

sudo cp client_mqtt.py dbcfeeder.py get_start_freshness.py j1939reader.py secoc_verification.py $SOURCES

# Copy dependencies from kuksa.val
cd ../../kuksa.val/kuksa-feeders/dbc2val/

sudo cp elm2canbridge.py dbc2vssmapper.py dbcreader.py $SOURCES
sudo cp -r transforms $SOURCES

sudo cp ../../kuksa_certificates/jwt/super-admin.json.token /etc/dbcfeeder/

cd ../../../../toolchain/services/dbcfeeder-service/

sudo cp dbc_feeder.ini /etc/dbcfeeder/

sudo chown $USER:$USER /etc/dbcfeeder/super-admin.json.token

sudo chown -R $USER:$USER /var/log/dbcfeeder /etc/dbcfeeder/ /usr/lib/python3/dist-packages/secoc/

sudo cp dbcfeeder.service /etc/systemd/system/

sudo cp dias_mapping.yml /etc/dbcfeeder/mapping.yml

sudo chown $USER:$USER /etc/dbcfeeder/mapping.yml

touch /etc/dbcfeeder/counter.txt

sudo sed -i "/User=/c\User=$USER" /etc/systemd/system/dbcfeeder.service

sudo sed -i "/Group=/c\Group=$USER" /etc/systemd/system/dbcfeeder.service

sudo systemctl enable dbcfeeder.service

sudo systemctl start dbcfeeder.service
