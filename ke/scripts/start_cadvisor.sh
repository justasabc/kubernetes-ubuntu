#/bin/sh
NAME=cadvisor
IMAGE=docker-registry:5000/cadvisor:latest
# we user host port 881 becauser 8080 has been used by kubernetes apiserver.
HOST_PORT=881
CONTAINER_PORT=8080

docker stop $NAME
docker rm $NAME
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=$HOST_PORT:$CONTAINER_PORT \
  --detach=true \
  --name=cadvisor \
  $IMAGE
