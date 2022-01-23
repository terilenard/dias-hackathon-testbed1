#!/bin/bash

if [ $# -lt 2 ]
then
    echo "Invalid arguments."
    echo "Please give 2 CAN interfaces (e.g., can0, vcan0),
    to set up a gateway"
    exit 1
fi

sudo apt install can-utils

sudo modprobe can-gw

sudo cangw -A -s $1 -d $2 -e

sudo cangw -A -d $1 -s $2 -e 
