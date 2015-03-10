#/bin/bash
kubecfg delete replicationControllers/opensim-controller
pods_list=$(kubecfg list pods | grep opensim | awk '{print $1;}' )
for pod_id in $pods_list;do
	kubecfg delete pods/$pod_id
done
