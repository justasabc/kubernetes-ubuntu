#/bin/bash
#==============================================================
# proxying client packets to proper servers(apache,robust,opensim)
#==============================================================

# port forwarding

# clear old rules
iptables -t nat -F PREROUTING
iptables -t nat -F POSTROUTING 

# add new rules
src_ip=192.168.1.194

# 1) apache
protocol=tcp
src_port=880
dst_port=880
pod_name=apache-pod
minion=$(kubecfg list pods | grep $pod_name | awk '{print $3;}' | cut -f1 -d/)
if [ "$minion" != "" ];then
	echo "======================================"
	dst_ip=$(resolveip -s $minion)
	iptables -t nat -A PREROUTING -p $protocol --dport $src_port -j DNAT --to-destination $dst_ip:$dst_port
	iptables -t nat -A POSTROUTING -p $protocol -d $dst_ip --dport $dst_port -j SNAT --to-source $src_ip
fi

# 2) robust
protocol=tcp
src_port=8002
dst_port=8002
pod_name=robust-pod
minion=$(kubecfg list pods | grep $pod_name | awk '{print $3;}' | cut -f1 -d/)
if [ "$minion" != "" ];then
	dst_ip=$(resolveip -s $minion)
	iptables -t nat -A PREROUTING -p $protocol --dport $src_port -j DNAT --to-destination $dst_ip:$dst_port
	iptables -t nat -A POSTROUTING -p $protocol -d $dst_ip --dport $dst_port -j SNAT --to-source $src_ip
fi

# 3) opensim sim port
protocol=tcp
src_port=8801
dst_port=8801
pod_name=sim1-pod
minion=$(kubecfg list pods | grep $pod_name | awk '{print $3;}' | cut -f1 -d/)
if [ "$minion" != "" ];then
	dst_ip=$(resolveip -s $minion)
	iptables -t nat -A PREROUTING -p $protocol --dport $src_port -j DNAT --to-destination $dst_ip:$dst_port
	iptables -t nat -A POSTROUTING -p $protocol -d $dst_ip --dport $dst_port -j SNAT --to-source $src_ip
fi

# 4) opensim region ports
region_ports=(9000 9001 9002 9003)
protocol=udp
if [ "$minion" != "" ];then
	for port in "${region_ports[@]}";do
		src_port=$port
		dst_port=$port
		iptables -t nat -A PREROUTING -p $protocol --dport $src_port -j DNAT --to-destination $dst_ip:$dst_port
		iptables -t nat -A POSTROUTING -p $protocol -d $dst_ip --dport $dst_port -j SNAT --to-source $src_ip
	done
fi

iptables -t nat -L
