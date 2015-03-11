#!/bin/sh
NAME=cadvisor
docker stop $NAME
docker rm $NAME
