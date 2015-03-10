#/bin/bash
minion=$(kubecfg list pods | grep opensim | awk '{print $3;}' | cut -f1 -d/)
echo $minion
test $minion && ssh $minion tail -f /volumes/opensim_resources/ke/grid/instances/sim1.log
