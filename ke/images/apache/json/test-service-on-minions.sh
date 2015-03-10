#/bin/bash
name=apache
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

echo curl -L "http://$ip:$port/region_load/sim1.xml"
ssh $minion curl -L "http://$ip:$port/region_load/sim1.xml"
