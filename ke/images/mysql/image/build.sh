#!/bin/bash
name=mysql
image=ubuntu:$name
registry=docker-registry:5000

docker stop $name
docker rm $name
docker rmi $image
docker rmi $registry/$image

docker build -t $image .

# push to registry
docker tag $image $registry/$image
docker push $registry/$image
