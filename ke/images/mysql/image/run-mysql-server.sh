#!/bin/bash
SERVICE_NAME='mysql'
CONTAINER=$SERVICE_NAME
BASE_IMAGE='ubuntu:mysql'
HOST_IP=$(/sbin/ifconfig $ETH0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
CMD='/bin/bash /home/start_mysql.sh'

HOST_PORT=3306
# run 
docker stop $CONTAINER
docker rm $CONTAINER
docker run -d -p $HOST_IP:$HOST_PORT:3306/tcp --name $CONTAINER -h $CONTAINER $BASE_IMAGE $CMD
docker logs $CONTAINER
