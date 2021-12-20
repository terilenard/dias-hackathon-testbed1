#!/bin/sh

# generate Python sources
protoc --python_out=python/comm_core --proto_path=. proto/*

# generate C sources
protoc-c --c_out=c/ --proto_path=. proto/*
