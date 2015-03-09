#!/bin/bash
#=======================================================
# https://coreos.com/docs/launching-containers/building/getting-started-with-docker/
# https://github.com/jacksoncage/apache-docker
#=======================================================
E_CURRENT_FOLDER=$(pwd)

CONTAINER='apache'
REGISTRY=docker-registry:5000
BASE_IMAGE=$REGISTRY/ubuntu:apache
HOST_IP=$(/sbin/ifconfig $ETH0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
PORT=880
#APACHE_HOST_FOLDER=$E_CURRENT_FOLDER/var/www/
APACHE_HOST_FOLDER=/volumes/var/www
APACHE_CONTAINER_FOLDER=/var/www
CMD='/bin/bash /home/start_apache.sh'

docker run -d -p $HOST_IP:$PORT:$PORT/tcp -h $CONTAINER --name $CONTAINER -v $APACHE_HOST_FOLDER:$APACHE_CONTAINER_FOLDER $BASE_IMAGE  $CMD
#docker run -d -p $HOST_IP:$PORT:$PORT/tcp -h $CONTAINER --name $CONTAINER $BASE_IMAGE 
