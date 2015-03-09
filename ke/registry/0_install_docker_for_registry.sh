#/bin/bash

# ===================================================
# http://www.zhihu.com/question/26718775
# http://stackoverflow.com/questions/26710153/remote-access-to-a-private-docker-registry
# ===================================================
# vim docker.conf
#DOCKER_OPTS="--insecure-registry docker-registry:5000 -H tcp://host-ip:2375 -H unix:///var/run/docker.sock"

# how to connect to docker-registry remotely?
# docker -H tcp://222.29.118.40:2375 images
# docker -H tcp://222.29.118.40:2375 run --rm -i -t 222.29.118.40:5000/test

apt-get -y install lxc-docker-1.3.2
FILENAME=docker
REGISTRY=docker-registry:5000
TCP_ADDR=tcp://docker-registry:2375
SOCK_ADDR=unix:///var/run/docker.sock

cat <<EOF >$FILENAME
DOCKER_OPTS="--insecure-registry $REGISTRY -H $TCP_ADDR -H $SOCK_ADDR "
EOF

cp $FILENAME /etc/default/docker
rm $FILENAME
service docker stop
service docker start
