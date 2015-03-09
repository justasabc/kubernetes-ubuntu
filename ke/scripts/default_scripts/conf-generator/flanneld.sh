#!/bin/bash
FILENAME=$(basename $0)
BASE="${FILENAME%.*}"

cat <<EOF >../$BASE
FLANNELD_OPTS="--etcd-endpoints=http://etcd:4001 --etcd-prefix=/coreos.com/network --subnet-file=/run/flannel/subnet.env"
EOF

#FLANNELD_OPTS="--etcd-endpoints=http://etcd:4001 --etcd-prefix="/coreos.com/network" --subnet-file="/run/flannel/subnet.env"
