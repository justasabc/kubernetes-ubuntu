#/bin/sh
image=./my_image_tar/registry.tar
exist=$(docker images | grep ^registry | wc -l)
if [ $exist -eq 1 ]
then
        echo "$image has been uploaded!"
else
        echo "uploading $image..."
	docker -H tcp://docker-registry:2375 load < $image
	echo "upload success!"
fi


