#/bin/bash
# http://jensd.be/?p=343
#http://rlworkman.net/howtos/iptables/cn/iptables-tutorial-cn-1.1.19.html#TABLE.TABLES
#https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html
#http://www.karlrupp.net/en/computer/nat_tutorial
#http://www.fclose.com/816/port-forwarding-using-iptables/
#https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/4/html/Security_Guide/s1-firewall-ipt-fwd.html
#http://opensimulator.org/wiki/Network_Settings

# port forwarding
#dst_ip=$(kubecfg list services | grep apache-service | awk '{print $4;}')
protocol=tcp
src_port=880
dst_port=880
src_ip=192.168.1.194
dst_ip=192.168.1.201

iptables -t nat -A PREROUTING -p $protocol --dport $src_port -j DNAT --to-destination $dst_ip:$dst_port
iptables -t nat -A POSTROUTING -p $protocol -d $dst_ip --dport $dst_port -j SNAT --to-source $src_ip

#iptables -t nat -A PREROUTING -p tcp --dport 9999 -j DNAT --to-destination 192.168.202.105:80
#iptables -t nat -A POSTROUTING -p tcp -d 192.168.202.105 --dport 80 -j SNAT --to-source 192.168.202.103

iptables -t nat -L

# root@194: tcpdump tcp port 880
# client---194---201
# client-194;
# 194-201;
# 201-194;
# 194-client
