#!/bin/bash

cat /proc/sys/net/ipv4/ip_forward

#iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to 192.168.1.2:8080
#iptables -t filter -A FORWARD -p tcp -d 192.168.1.2 --dport 8080 -j ACCEPT

# list 
iptables -t nat -F INPUT
iptables -t nat -F OUTPUT

# http://opensimulator.org/wiki/Network_Settings
#EXTERNAL_IP=162.105.17.48
EXTERNAL_IP=192.168.1.194

# robust 8002/tcp
PORT=8002
INTERNAL_IP=192.168.1.202
iptables -t nat -A INPUT -p tcp -m tcp --sport $PORT --dst $EXTERNAL_IP -j ACCEPT
iptables -t nat -A OUTPUT --dst $EXTERNAL_IP -p tcp --dport $PORT:$PORT -j DNAT --to-destination $INTERNAL_IP

# opensim sim_port/tcp
PORT=8801
INTERNAL_IP=192.168.1.201
iptables -t nat -A INPUT -p tcp -m tcp --sport $PORT --dst $EXTERNAL_IP -j ACCEPT
iptables -t nat -A OUTPUT --dst $EXTERNAL_IP -p tcp --dport $PORT:$PORT -j DNAT --to-destination $INTERNAL_IP

# opensim regions_port/udp
INTERNAL_IP=192.168.1.201

PORT=9000
iptables -t nat -A INPUT -p udp -m udp --sport $PORT --dst $EXTERNAL_IP -j ACCEPT
iptables -t nat -A OUTPUT --dst $EXTERNAL_IP -p udp --dport $PORT:$PORT -j DNAT --to-destination $INTERNAL_IP
PORT=9001
iptables -t nat -A INPUT -p udp -m udp --sport $PORT --dst $EXTERNAL_IP -j ACCEPT
iptables -t nat -A OUTPUT --dst $EXTERNAL_IP -p udp --dport $PORT:$PORT -j DNAT --to-destination $INTERNAL_IP
PORT=9002
iptables -t nat -A INPUT -p udp -m udp --sport $PORT --dst $EXTERNAL_IP -j ACCEPT
iptables -t nat -A OUTPUT --dst $EXTERNAL_IP -p udp --dport $PORT:$PORT -j DNAT --to-destination $INTERNAL_IP
PORT=9003
iptables -t nat -A INPUT -p udp -m udp --sport $PORT --dst $EXTERNAL_IP -j ACCEPT
iptables -t nat -A OUTPUT --dst $EXTERNAL_IP -p udp --dport $PORT:$PORT -j DNAT --to-destination $INTERNAL_IP

# restart iptables
#service iptables restart

# list 
iptables -t nat -L INPUT
iptables -t nat -L OUTPUT
