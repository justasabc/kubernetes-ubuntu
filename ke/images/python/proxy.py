#/usr/bin/python
# -*- coding:utf-8 -*-

from commander import UtilityCommander,KubernetesCommander,IptablesCommander

HOST_IP = UtilityCommander().get_host_ip()

class BaseProxy:
	"""
	set up a network proxy between client and server(apache,robust,opensim)
	"""
	def __init__(self,protocol,src_port,dst_port,src_ip,dst_ip):
		self.protocol = protocol
		self.src_port = src_port
		self.dst_port = dst_port
		self.src_ip = src_ip
		self.dst_ip = dst_ip

	def get_protocol(self):
		return self.protocol 

	def get_src_port(self):
		return self.src_port

	def get_dst_port(self):
		return self.dst_port

	def get_src_ip(self):
		return self.src_ip 

	def get_dst_ip(self):
		return self.dst_ip

	def __setup_proxy(self,protocol,src_port,dst_port,src_ip,dst_ip):
		cmd = IptablesCommander()
		cmd.nat_add_rule_to_prerouting_chain(protocol,src_port,dst_port,src_ip,dst_ip)
		cmd.nat_add_rule_to_postrouting_chain(protocol,src_port,dst_port,src_ip,dst_ip)

	def setup(self):
		self.__setup_proxy(self.protocol,self.src_port,self.dst_port,self.src_ip,self.dst_ip)


class ApacheProxy(BaseProxy):

	def __init__(self):
		self.__init_setting()

	def __init_setting(self):
		protocol = "tcp"
		src_port = 880
		dst_port = 880
		src_ip =  HOST_IP

		cmd = KubernetesCommander()
		pod_id = "apache-pod"
		hostname = cmd.get_pod_hostname(pod_id)
		dst_ip = cmd.hostname_to_ip(hostname)

		BaseProxy.__init__(self,protocol,src_port,dst_port,src_ip,dst_ip)

