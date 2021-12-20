#!/bin/sh

cd ./proto
# generate Python sources
protoc --python_out=../python --proto_path=. ./dias_protocol/*.proto

# generate C sources
protoc-c --c_out=../c/src --proto_path=. ./dias_protocol/*.proto
