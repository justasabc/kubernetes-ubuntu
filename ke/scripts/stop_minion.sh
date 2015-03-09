#/bin/sh

service flanneld stop
#service kubelet stop
#service kube-proxy stop
service docker stop

# remove docker0 and flannel0
ip link set dev flannel0 down
brctl delbr flannel0

# delete docker0
ip link set dev docker0 down
brctl delbr docker0
