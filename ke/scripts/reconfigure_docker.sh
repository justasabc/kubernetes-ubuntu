#!/bin/bash

# delete docker0
ip link set dev docker0 down
brctl delbr docker0

echo "========================================"
# source must occur with #/bin/bash
file=/run/flannel/subnet.env
source $file
echo $FLANNEL_SUBNET
echo $FLANNEL_MTU
HOSTNAME=$(cat /etc/hostname)
echo $HOSTNAME
echo "========================================"

echo DOCKER_OPTS=\"--insecure-registry docker-registry:5000 -H tcp://${HOSTNAME}:2375 -H unix:///var/run/docker.sock \
    --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU}\" > /etc/default/docker
service docker stop
service docker start
