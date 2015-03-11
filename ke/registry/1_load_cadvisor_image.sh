#/bin/sh
name=cadvisor
image=./my_image_tar/cadvisor0.8.tar
exist=$(docker images | grep ^google/cadvisor | wc -l)

new_image=google/cadvisor:0.8.0
registry=docker-registry:5000

if [ $exist -eq 1 ]
then
        echo "$image has been uploaded!"
else
        echo "uploading $image..."
	docker -H tcp://docker-registry:2375 load < $image
	echo "upload success!"

	echo "pushing $name to server..."
	docker -H tcp://docker-registry:2375 tag $new_image $registry/$name
	docker -H tcp://docker-registry:2375 push $registry/$name
fi
