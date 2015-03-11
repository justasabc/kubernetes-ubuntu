#/bin/sh
service flanneld stop
#service kubelet stop
#service kube-proxy stop
#service docker stop

#=======================================================================================
# No need to remove flannel0 becasue stop flanneld will remove flanneld0 at the same time.
#=======================================================================================
#ip link set dev flannel0 down
#brctl delbr flannel0
