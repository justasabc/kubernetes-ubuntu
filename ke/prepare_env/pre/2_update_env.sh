#/bin/sh

# update hosts
hosts=/etc/hosts
exist=$(cat $hosts | grep master | wc -l)
if [ $exist -eq 1 ]
then
	echo "$hosts has been updated!"
else
	cat hosts >>$hosts
	echo "updating $hosts..."
fi

# update bashrc
bashrc=/root/.bashrc
exist=$(cat $bashrc | grep HOST_IP | wc -l)
if [ $exist -eq 1 ]
then
	echo "$bashrc has been updated!"
else
	cat bashrc >>$bashrc
	echo "updating $bashrc..."
fi

echo "====================================="
echo $ETH0
echo $HOST_IP
echo "====================================="
