#/bin/sh

#=========================================================================================================
# http://blog.csdn.net/iloveyin/article/details/40542635
# https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-docker-registry-on-ubuntu-14-04
#=========================================================================================================

# Docker has an unusual mechanism for specifying which registry to push to. You have to tag an image with the private registry's locati on in order to push to it. Let's tag our image to our private registry:

# ****************************************************************
# tag before push
# push
#docker tag test-image docker-registry:5000/test-image
#docker push docker-registry:5000/test-image

# pull and test
# docker pull docker-registry:5000/test-image
# docker run --rm -i -t docker-registry:5000/test-image
# ****************************************************************

# auto upload local images to registry server

registry=docker-registry:5000
local_images=$(docker images | grep -v $registry | grep -v TAG | awk '{print $1":"$2}')
for name in $local_images; do
	echo "pushing $name to server..."
	docker -H tcp://docker-registry:2375 tag $name $registry/$name
	docker -H tcp://docker-registry:2375 push $registry/$name
done

