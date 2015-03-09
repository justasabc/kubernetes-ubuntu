#/bin/bash
kubecfg delete replicationControllers/apache-controller
pods_list=$(kubecfg list pods | grep apache | awk '{print $1;}' )
for pod_id in $pods_list;do
	kubecfg delete pods/$pod_id
done
#kubecfg delete services/apache-service
