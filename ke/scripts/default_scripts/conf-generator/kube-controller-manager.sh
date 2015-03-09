#!/bin/bash
FILENAME=$(basename $0)
BASE="${FILENAME%.*}"

KUBE_LOGTOSTDERR=true
KUBE_MASTER=http://master:8080

# add minion address here
MINION_ADDRESSES=minion1,minion2,minion3,minion4
#MINION_ADDRESSES=192.168.1.201,192.168.1.202,192.168.1.203

cat <<EOF >../$BASE
KUBE_CONTROLLER_MANAGER_OPTS="--logtostderr=${KUBE_LOGTOSTDERR} \\
	--machines=${MINION_ADDRESSES} \\
	--master=${KUBE_MASTER}"
EOF

#KUBE_CONTROLLER_MANAGER_OPTS="--master=127.0.0.1:8080 \
#--machines=127.0.0.1 \
#--logtostderr=true"
