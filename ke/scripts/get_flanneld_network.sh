#/bin/sh
etcdctl --peers http://etcd:4001 get /coreos.com/network/config
etcdctl --peers http://etcd:4001 get /coreos.com/network/subnets
