#/bin/sh
# https://github.com/crosbymichael/dockerui
NAME=dockerui
IMAGE=docker-registry:5000/dockerui:latest

#docker pull dockerui/dockerui
#docker tag dockerui/dockerui $IMAGE
#docker push $IMAGE


# we user host port 882 
HOST_PORT=882
CONTAINER_PORT=9000

docker stop $NAME
docker rm $NAME
docker run -d --name=$NAME -p $HOST_PORT:$CONTAINER_PORT -v /var/run/docker.sock:/var/run/docker.sock $IMAGE
