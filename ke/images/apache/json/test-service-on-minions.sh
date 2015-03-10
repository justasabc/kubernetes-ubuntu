#/bin/bash
ip_port=$(kubecfg list services | grep apache-service | awk '{print $4":"$5;}')
minion=$(kubecfg list pods | grep apache | awk '{print $3;}' | cut -f1 -d/)
echo $minion
test $minion && ssh $minion curl -L "http://$ip_port/region_load/sim1.xml"
