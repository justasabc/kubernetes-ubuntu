#/bin/sh
etcdctl --peers http://etcd:4001 set /coreos.com/network/config '{ "Network": "10.10.0.0/16" }' 
etcdctl --peers http://etcd:4001 get /coreos.com/network/config
