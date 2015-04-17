# opensim pods
kubecfg delete pods/xwd
kubecfg delete pods/huyu

# robust
name=robust
kubecfg delete replicationControllers/$name-controller
pods_list=$(kubecfg list pods | grep $name-pod | awk '{print $1;}' )
for pod_id in $pods_list;do
	kubecfg delete pods/$pod_id
done
kubecfg delete services/robust-public-service
kubecfg delete services/robust-internal-service

# mysql
name=mysql
kubecfg delete replicationControllers/$name-controller
pods_list=$(kubecfg list pods | grep $name-pod | awk '{print $1;}' )
for pod_id in $pods_list;do
	kubecfg delete pods/$pod_id
done
kubecfg delete services/mysql-service

# apache
name=apache
kubecfg delete replicationControllers/$name-controller
pods_list=$(kubecfg list pods | grep $name-pod | awk '{print $1;}' )
for pod_id in $pods_list;do
	kubecfg delete pods/$pod_id
done
kubecfg delete services/apache-service
