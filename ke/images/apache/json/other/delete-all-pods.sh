#/bin/bash
pods_list=$(kubecfg list pods | awk '{print $1;}' | tail -n +3)
for pod_id in $pods_list;do
	kubecfg delete pods/$pod_id
done
