#/bin/bash
name=mysql
ip=$(kubecfg list services | grep $name-service | awk '{print $4;}')
port=$(kubecfg list services | grep $name-service | awk '{print $5;}')

minion=
# get minion
while [ -z $minion ]
do
	sleep 1
	minion=$(kubecfg list pods | grep $name | awk '{print $3;}' | cut -f1 -d/)
	echo $minion
done
echo "========================================================"

running=
while [ "$running" != "Running" ]
do
	sleep 1
	running=$(kubecfg list pods | grep $name | awk '{print $5;}' )
	echo $running
done
echo "========================================================"

echo "mysql -u adminuser -padminpass -P $port -h $ip"
