#!/bin/bash

cd ../services/cloudfeeder-service

sudo pip3 install -r requirements.txt

sudo mkdir /etc/cloudfeeder/
sudo chown $USER:$USER /etc/cloudfeeder

sudo mkdir /var/log/cloudfeeder
sudo chown $USER:$USER /var/log/cloudfeeder

touch /var/log/cloudfeeder/info.log
touch /var/log/cloudfeeder/error.log

SOURCES=/usr/lib/python3/dist-packages/cloudfeeder/
sudo mkdir $SOURCES
sudo chown $USER:$USER $SOURCES

sudo cp kuksa_val_config.json /etc/cloudfeeder
sudo cp -r kuksa_certificates/ /etc/cloudfeeder

#sudo cp saved_dict.json saved_queue.json saved_samp.json $SOURCES
#sudo chown $USER:$USER $SOURCES/saved_dict.json $SOURCES/saved_queue.json $SOURCES/saved_samp.json

sudo cp cloudfeeder.service /etc/systemd/system/

cd ../../../modules/secoc/cloud/

sudo cp cloudfeeder.py preprocessor_bosch.py $SOURCES
sudo chown $USER:$USER $SOURCES/cloudfeeder.py $SOURCES/preprocessor_bosch.py

sudo systemctl enable cloudfeeder.service
sudo systemctl start cloudfeeder.service
