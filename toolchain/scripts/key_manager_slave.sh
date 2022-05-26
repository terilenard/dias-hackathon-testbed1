#!/bin/bash

SOURCE_PATH=/usr/lib/python3/dist-packages/dias-ltk-stk/
CONFIG_PATH=/etc/dias-ltk-stk/
LOG_PATH=/var/log/dias-ltk-stk/
SERVICE_NAME=key_manager_slave.service
BOOSTRAP_DIR=/etc/tpm_handlers/dias-ltk-stk/

# Directories
sudo mkdir -p $SOURCE_PATH
sudo chmod $USER:$USER $SOURCE_PATH

sudo mkdir -p $CONFIG_PATH
sudo chmod $USER:$USER $CONFIG_PATH

sudo mkdir -p $LOG_PATH
sudo chmod $USER:$USER $LOG_PATH

# Log file
touch $LOG_PATH/slave_kmngr.log

# Sources
cd ../../modules/dias-ltk-stk/src/

cp -r pytpm/ $SOURCE_PATH
cp -r master_core/ $SOURCE_PATH
cp -r utils/ $SOURCE_PATH
cp master_kmngr.py $SOURCE_PATH
 
cd -
# Bootstrapping directories

if [ ! -e $BOOSTRAP_DIR ]
then
    sudo mkdir -p $BOOSTRAP_DIR
    sudo chown $USER:$USER $BOOSTRAP_DIR
fi

if [ ! -e $BOOSTRAP_DIR/MASTER_TPMCTX/ASYMKEYCTX ]
then
    sudo mkdir -p $BOOSTRAP_DIR/MASTER_TPMCTX/ASYMKEYCTX
    sudo chown $USER:$USER $BOOSTRAP_DIR/MASTER_TPMCTX/ASYMKEYCTX
fi

if [ ! -e $BOOSTRAP_DIR/MASTER_TPMCTX/EXTKEYSTORE ]
then
    mkdir -p $BOOSTRAP_DIR/MASTER_TPMCTX/EXTKEYSTORE
    sudo chown $USER:$USER $BOOSTRAP_DIR/MASTER_TPMCTX/EXTKEYSTORE
fi

# Service configuration
cp ../../modules/dias-ltk-stk/config/slave_kmngr.ini $CONFIG_PATH

sudo cp ../services/dias-ltk-stk-service/$SERVICE_NAME /etc/systemd/system/

sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME
