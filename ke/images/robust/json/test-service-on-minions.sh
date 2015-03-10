#/bin/bash
minion=$(kubecfg list pods | grep robust | awk '{print $3;}' | cut -f1 -d/)
echo $minion
test $minion && ssh $minion tail -f /volumes/opensim_resources/ke/grid/services/robust.log
