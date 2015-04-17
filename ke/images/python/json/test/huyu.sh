#/bin/bash
name=huyu

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

ssh $minion tail -f "/volumes/opensim_resources/ke/grid/instances/$name.log"
