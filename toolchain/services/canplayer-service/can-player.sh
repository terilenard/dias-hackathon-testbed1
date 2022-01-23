#!/bin/bash

if [ $# -lt 1 ]
then
    echo "Invalid arguments. Please specify the log file to be replayed."
    exit 1
fi

cmd="canplayer -I $1"

if [ $# -eq 2 ]
then
  cmd="canplayer vcan0=$2 -I $1"
fi

while true
do
    eval $cmd
done
