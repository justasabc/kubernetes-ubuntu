#/bin/sh
etcdctl --peers http://etcd:4001 get /coreos.com/network/config
