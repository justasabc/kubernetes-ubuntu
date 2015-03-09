#/bin/sh
registry=docker-registry:5000
local_images=$(docker images | grep -v $registry | grep -v TAG | awk '{print $1":"$2}')
for name in $local_images; do
	docker -H tcp://docker-registry:2375 rmi $registry/$name
done

