#/bin/sh

# add minion here
minions=(minion1 minion2 minion3)
kube_root=/root/kubernetes-ubuntu
path=/volumes/opensim_resources

for m in "${minions[@]}" ;do
	echo "===================================="
	echo "copying files to $m..."
	#scp start_robust.sh $m:$path
	#scp start_opensim_xxx.sh $m:$path
	#scp -r grid $m:$path
	scp -r ../ke $m:$path
done
