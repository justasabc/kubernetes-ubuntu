#/bin/bash
kubecfg delete replicationControllers/robust-controller
pods_list=$(kubecfg list pods | grep robust | awk '{print $1;}' )
for pod_id in $pods_list;do
	kubecfg delete pods/$pod_id
done
#kubecfg delete services/robust-service
