#/bin/sh

NAME=docker-registry
docker stop $NAME
docker rm $NAME
