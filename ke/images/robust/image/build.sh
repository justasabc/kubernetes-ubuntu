#!/bin/bash
name=robust
image=ubuntu:$name
registry=docker-registry:5000

#docker stop $name
#docker rm $name
docker rmi $image
docker rmi $registry/$image

docker build -t $image .

# push to registry
docker tag $image $registry/$image
docker push $registry/$image

### add opensim images
new_image=ubuntu:opensim
docker tag $image $new_image
docker tag $new_image $registry/$new_image
docker push $registry/$new_image
