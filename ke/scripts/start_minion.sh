#/bin/bash
# clear iptables
iptables -t filter -F
iptables -t nat -F

service flanneld start
#service kubelet start
#service kube-proxy start
#service docker start
