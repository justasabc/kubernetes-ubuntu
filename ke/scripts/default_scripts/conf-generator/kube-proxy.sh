#!/bin/bash
FILENAME=$(basename $0)
BASE="${FILENAME%.*}"

KUBE_LOGTOSTDERR=true
KUBE_ETCD_SERVERS=http://etcd:4001

cat <<EOF >../$BASE
KUBE_PROXY_OPTS="--logtostderr=${KUBE_LOGTOSTDERR} \\
	--etcd_servers=${KUBE_ETCD_SERVERS}"
EOF

#KUBE_PROXY_OPTS="--etcd_servers=http://127.0.0.1:4001 \
#--logtostderr=true"
