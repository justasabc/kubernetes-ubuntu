#!/bin/bash
E_CURRENT_FOLDER=$(pwd)

E_HOST_FOLDER=$E_CURRENT_FOLDER/ke

E_CONTAINER_BIN_FOLDER=/home/opensim80/bin
E_CONTAINER_FOLDER=$E_CONTAINER_BIN_FOLDER/ke
E_CONTAINER_WORKDIR=$E_CONTAINER_BIN_FOLDER/ke

E_SERVICE_NAME='robust'
E_INI_FILE=$E_CONTAINER_FOLDER/grid/conf/Robust.ini
E_LOG_CONFIG=$E_CONTAINER_FOLDER/grid/conf/Robust.exe.config
E_PID_FILE=$E_CONTAINER_FOLDER/grid/services/$E_SERVICE_NAME.pid
E_LOG_FILE=$E_CONTAINER_FOLDER/grid/services/$E_SERVICE_NAME.log

CONTAINER=$E_SERVICE_NAME
BASE_IMAGE='ubuntu:robust'
HOST_IP=$(/sbin/ifconfig $ETH0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
CMD='/home/opensim80/bin/ke/start_robust.sh'

#docker rm $CONTAINER
docker run --rm -i -t -h $CONTAINER --name $CONTAINER -w $E_CONTAINER_WORKDIR -p $HOST_IP:8002:8002/tcp -p $HOST_IP:8003:8003/tcp -v $E_HOST_FOLDER:$E_CONTAINER_FOLDER --link mysql:vgeomysql -e SERVICE_NAME=$E_SERVICE_NAME -e INI_FILE=$E_INI_FILE -e LOG_CONFIG=$E_LOG_CONFIG -e PID_FILE=$E_PID_FILE -e LOG_FILE=$E_LOG_FILE $BASE_IMAGE $CMD
