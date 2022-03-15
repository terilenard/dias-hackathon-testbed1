#!/bin/bash

if [ $# -lt 1 ]
then
    echo "Invalid arguments. Please specify the log file to be replayed."
    exit 1
fi

cmd="canplayer vcan0=vcan1 -I $1"

eval $cmd
