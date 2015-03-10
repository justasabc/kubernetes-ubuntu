#!/bin/bash
SIM_NAME='opensim'
SIM_PORT=8800

CONTAINER=$SIM_NAME
BASE_IMAGE='ubuntu:opensim'
HOST_IP=$(/sbin/ifconfig $ETH0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
CMD='/bin/bash /home/opensim80/bin/ke/start_opensim_xxx.sh'

docker rm  $CONTAINER
docker run -i -t -h $CONTAINER -p $HOST_IP:8800:8800/tcp -p $HOST_IP:9001:9001/udp -p $HOST_IP:9002:9002/udp --link mysql:vgeomysql --link robust:vgeorobust --name $CONTAINER $BASE_IMAGE $CMD
