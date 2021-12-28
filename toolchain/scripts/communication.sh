#!/bin/bash

sudo apt -y install protobuf-compiler protobuf-c-compiler

pip3 install pyzmq protobuf blist

python3 ../../modules/communication_protocol/generate.sh
