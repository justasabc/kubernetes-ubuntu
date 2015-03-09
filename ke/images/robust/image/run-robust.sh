#!/bin/bash
SERVICE_NAME='robust'
CONTAINER=$SERVICE_NAME
BASE_IMAGE='ubuntu:robust'
HOST_IP=$(/sbin/ifconfig $ETH0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
CMD='/bin/bash /home/opensim80/bin/ke/robust start main'

# run 
docker rm $CONTAINER
docker run -i -t -h $CONTAINER -p $HOST_IP:8002:8002/tcp -p $HOST_IP:8003:8003/tcp --link mysql:vgeomysql --name $CONTAINER $BASE_IMAGE  $CMD

