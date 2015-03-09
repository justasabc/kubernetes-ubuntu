#/bin/sh
#docker rmi docker-registry:5000/ubuntu:apache
#docker rmi docker-registry:5000/ubuntu:mysql
#docker rmi docker-registry:5000/ubuntu:robust
#docker rmi docker-registry:5000/ubuntu:opensim

echo "pulling images to local minion..."
docker pull docker-registry:5000/ubuntu:apache
docker pull docker-registry:5000/ubuntu:mysql
docker pull docker-registry:5000/ubuntu:robust
docker pull docker-registry:5000/ubuntu:opensim
