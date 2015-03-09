#!/bin/bash

NAME=base
docker stop $NAME
docker rm $NAME
docker rmi ubuntu:$NAME

docker build -t "ubuntu:$NAME" .
