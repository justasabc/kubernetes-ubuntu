#!/bin/bash
FILENAME=$(basename $0)
BASE="${FILENAME%.*}"

ETCD_NAME=$BASE
# no http:// prefix
ETCD_PEER_ADDR=etcd:7001
ETCD_ADDR=etcd:4001
ETCD_PEER_BIND_ADDR=etcd:7001
ETCD_BIND_ADDR=etcd:4001

# etcdctl --peers http://$ETCD_BIND_ADDR get mykey
# etcdctl --peers http://etcd:4001 get mykey

# clear etcd data store
ETCD_DATA_DIR=/opt/$BASE
test -d $ETCD_DATA_DIR && rm -rf $ETCD_DATA_DIR
! test -d $ETCD_DATA_DIR && mkdir -p $ETCD_DATA_DIR

cat <<EOF >../$BASE
ETCD_OPTS="--name=$ETCD_NAME \\
	--peer-addr=$ETCD_PEER_ADDR \\
	--addr=$ETCD_ADDR \\
	--peer-bind-addr=$ETCD_PEER_BIND_ADDR \\
	--bind-addr=$ETCD_BIND_ADDR \\
	--data-dir=$ETCD_DATA_DIR"
EOF

#ETCD_OPTS="--name=etcd \
#--addr=127.0.0.1:4001 \
#--bind-addr=0.0.0.0 \
#--peer-addr=127.0.0.1:7001 \
#--peer-bind-addr=0.0.0.0 \
#--data-dir=/opt/etcd"
