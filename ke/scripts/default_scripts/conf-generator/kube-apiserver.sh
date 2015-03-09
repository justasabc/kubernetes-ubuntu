#!/bin/bash
# https://coreos.com/docs/distributed-configuration/etcd-configuration/

FILENAME=$(basename $0)
BASE="${FILENAME%.*}"

KUBE_LOGTOSTDERR=true

KUBE_ETCD_SERVERS=http://etcd:4001
KUBE_API_ADDRESS=0.0.0.0
KUBE_API_PORT=8080
KUBE_SERVICE_ADDRESSES=10.10.0.0/16
echo $KUBE_SERVICE_ADDRESSES

cat <<EOF >../$BASE
KUBE_APISERVER_OPTS="--logtostderr=${KUBE_LOGTOSTDERR} \\
	--etcd_servers=${KUBE_ETCD_SERVERS} \\
	--address=${KUBE_API_ADDRESS} \\
	--port=${KUBE_API_PORT} \\
	--portal_net=${KUBE_SERVICE_ADDRESSES}"
EOF

#KUBE_APISERVER_OPTS="--address=127.0.0.1 \
#--port=8080 \
#--etcd_servers=http://127.0.0.1:4001 \
#--logtostderr=true \
#--portal_net=10.10.10.0/24"
