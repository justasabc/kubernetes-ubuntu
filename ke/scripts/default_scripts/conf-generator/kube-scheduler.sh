#!/bin/bash
FILENAME=$(basename $0)
BASE="${FILENAME%.*}"

KUBE_LOGTOSTDERR=true
KUBE_MASTER=http://master:8080

cat <<EOF >../$BASE
KUBE_SCHEDULER_OPTS="--logtostderr=${KUBE_LOGTOSTDERR} \\
	--master=${KUBE_MASTER}"
EOF

#KUBE_SCHEDULER_OPTS="--logtostderr=true \
#--master=127.0.0.1:8080"
