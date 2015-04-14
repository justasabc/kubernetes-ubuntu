"""
Class Hierarchy

G{classtree: BaseProxy} 

Package tree
G{packagetree: proxy} 

Import Graph
G{importgraph: proxy} 

"""
#/usr/bin/python
# -*- coding:utf-8 -*-

#from simulator import Simulator
from proxy_param import ProxyParam
from cluster_tool import UtilityTool,IptablesTool,KubernetesTool
g_utility_tool = UtilityTool()
HOST_IP = g_utility_tool.get_host_ip()
g_kubernetes_tool = KubernetesTool()

class BaseProxy:
	"""
	base proxy: set up a network proxy between client and server(apache,robust,opensim)
	"""
	def __init__(self,proxy_param):
		self.proxy_param = proxy_param
		""" @type: L{ProxyParam} """

		self.tool = IptablesTool()
		""" @type: L{IptablesTool} """

	def get_protocol(self):
		return self.proxy_param.protocol 

	def get_src_port(self):
		return self.proxy_param.src_port

	def get_dst_port(self):
		return self.proxy_param.dst_port

	def get_src_ip(self):
		return self.proxy_param.src_ip 

	def get_dst_ip(self):
		return self.proxy_param.dst_ip

	def get_tool(self):
		return self.iptables_tool

	def __start_proxy(self,proxy_param):
		protocol = proxy_param.protocol
		src_port = proxy_param.src_port
		dst_port = proxy_param.dst_port
		src_ip   = proxy_param.src_ip
		dst_ip   = proxy_param.dst_ip
		self.tool.nat_add_rule_to_prerouting_chain(protocol,src_port,dst_port,src_ip,dst_ip)
		self.tool.nat_add_rule_to_postrouting_chain(protocol,src_port,dst_port,src_ip,dst_ip)

	def start(self):
		self.__start_proxy(self.proxy_param)

class ApacheProxy(BaseProxy):
	"""
	apache proxy
	"""

	def __init__(self):
		print "[ApacheProxy] init..."
		self.create_proxy_param()
		print "[ApacheProxy] OK."

	def create_proxy_param(self):
		protocol = "tcp"
		src_port = 880
		dst_port = 880
		src_ip =  HOST_IP

		pod_id = "apache-pod"
		dst_ip = g_kubernetes_tool.get_pod_ip(pod_id)
		proxy_param = ProxyParam(protocol,src_port,dst_port,src_ip,dst_ip)
		BaseProxy.__init__(self,proxy_param)

	def start(self):
		print "[ApacheProxy] start..."
		BaseProxy.start(self)

class MysqlProxy(BaseProxy):
	"""
	mysql proxy
	"""

	def __init__(self):
		print "[MysqlProxy] init..."
		self.create_proxy_param()
		print "[MysqlProxy] OK."

	def create_proxy_param(self):
		protocol = "tcp"
		src_port = 3306
		dst_port = 3306
		src_ip =  HOST_IP

		pod_id = "mysql-pod"
		dst_ip = g_kubernetes_tool.get_pod_ip(pod_id)
		proxy_param = ProxyParam(protocol,src_port,dst_port,src_ip,dst_ip)
		BaseProxy.__init__(self,proxy_param)

	def start(self):
		print "[MysqlProxy] start..."
		BaseProxy.start(self)

class RobustProxy(BaseProxy):
	"""
	robust proxy
	"""

	def __init__(self):
		print "[RobustProxy] init..."
		self.create_proxy_param()
		print "[RobustProxy] OK."

	def create_proxy_param(self):
		protocol = "tcp"
		src_port = 8002
		dst_port = 8002
		src_ip =  HOST_IP

		pod_id = "robust-pod"
		dst_ip = g_kubernetes_tool.get_pod_ip(pod_id)
		proxy_param = ProxyParam(protocol,src_port,dst_port,src_ip,dst_ip)
		BaseProxy.__init__(self,proxy_param)

	def start(self):
		print "[RobustProxy] start..."
		BaseProxy.start(self)

class SimulatorProxy(BaseProxy):
	"""
	simulator proxy
	"""
	def __init__(self,proxy_param):
		BaseProxy.__init__(self,proxy_param)

	def start(self):
		print "[SimulatorProxy] start..."
		BaseProxy.start(self)

class RegionProxy(BaseProxy):
	"""
	region proxy
	"""
	def __init__(self,proxy_param):
		BaseProxy.__init__(self,proxy_param)

	def start(self):
		#print "[RegionProxy] start..."
		BaseProxy.start(self)

class OpensimProxy:
	"""
	opensim proxy:  1 simulator proxy + N region proxy
	"""

	def __init__(self,simulator):
		print "[OpensimProxy] init..."
		self.simulator = simulator
		""" @type: L{Simulator} """
		self.simulator_proxy = None
		""" @type: L{SimulatorProxy} """
		self.region_proxy_list = []
		""" @type: L{RegionProxy} """

		self.create_proxy_param(simulator)
		print "[OpensimProxy] OK"

	def create_proxy_param(self,simulator):
		sim_name = simulator.get_simulator_name()
		sim_port = simulator.get_simulator_port()
		region_port_list = simulator.get_region_port_list()

		src_ip =  HOST_IP
		pod_id = sim_name
		dst_ip = g_kubernetes_tool.get_pod_ip(pod_id)

		# create simulator proxy
		src_port = dst_port = sim_port
		simulator_proxy = self.create_simulator_proxy("tcp",src_port,dst_port,src_ip,dst_ip)
		self.set_simulator_proxy(simulator_proxy)

		# create N region proxy
		for region_port in region_port_list:
			src_port = dst_port = region_port
			region_proxy = self.create_region_proxy("udp",src_port,dst_port,src_ip,dst_ip)
			self.add_region_proxy(region_proxy)

	def start(self):
		print "[OpensimProxy] start..."
		self.simulator_proxy.start()
		for region_proxy in self.get_region_proxy_list():
			region_proxy.start()

	def set_simulator_proxy(self,simulator_proxy):
		self.simulator_proxy = simulator_proxy

	def get_simulator_proxy(self):
		return self.simulator_proxy

	def add_region_proxy(self,region_proxy):
		self.region_proxy_list.append(region_proxy)

	def get_region_proxy_list(self):
		return self.region_proxy_list

	def create_simulator_proxy(self,protocol,src_port,dst_port,src_ip,dst_ip):
		proxy_param = ProxyParam(protocol,src_port,dst_port,src_ip,dst_ip)
		simulator_proxy = SimulatorProxy(proxy_param)
		return simulator_proxy

	def create_region_proxy(self,protocol,src_port,dst_port,src_ip,dst_ip):
		proxy_param = ProxyParam(protocol,src_port,dst_port,src_ip,dst_ip)
		region_proxy = RegionProxy(proxy_param)
		return region_proxy

class ProxyTesting(ApacheProxy,MysqlProxy,RobustProxy,OpensimProxy):
	pass
