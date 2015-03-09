#!/bin/bash
FILENAME=$(basename $0)
BASE="${FILENAME%.*}"

KUBE_LOGTOSTDERR=true
KUBE_ETCD_SERVERS=http://etcd:4001
# update minion address here
#MINION_ADDRESS=$HOST_IP
MINION_ADDRESS=0.0.0.0
# update here
MINION_HOSTNAME=$(cat /etc/hostname)
MINION_PORT=10250

cat <<EOF >../$BASE
KUBELET_OPTS="--logtostderr=${KUBE_LOGTOSTDERR} \\
	--etcd_servers=${KUBE_ETCD_SERVERS} \\
	--address=${MINION_ADDRESS} \\
	--port=${MINION_PORT} \\
	--hostname_override=${MINION_HOSTNAME}"
EOF

#KUBELET_OPTS="--address=127.0.0.1 \
#--port=10250 \
#--hostname_override=127.0.0.1 \
#--etcd_servers=http://127.0.0.1:4001 \
#--logtostderr=true"
