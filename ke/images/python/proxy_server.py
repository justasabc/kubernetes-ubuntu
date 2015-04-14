"""
Class Hierarchy

G{classtree: ProxyServer} 

Package tree
G{packagetree: proxy_server} 

Import Graph
G{importgraph: proxy_server} 

"""
from proxy import *
from cluster_tool import IptablesTool

class ProxyServer:
	"""
	1 ApacheProxy + 1 MysqlProxy + 1 RobustProxy + N OpensimProxy
	"""

	def __init__(self,simulator_manager):
	 	print "[ProxyServer] init..."
		self.simulator_manager = simulator_manager
		#""" @type: L{SimulatorManager} """

		self.tool = IptablesTool()
		#""" @type: L{IptablesTool} """

		self.apache_proxy = ApacheProxy()
		""" @type: L{ApacheProxy} """
		self.mysql_proxy = MysqlProxy()
		""" @type: L{MysqlProxy} """
		self.robust_proxy = RobustProxy()
		""" @type: L{RobustProxy} """
		self.opensim_proxy_list = []
		""" @type: L{OpensimProxy} """

		self.init_proxy_server()
	 	print "[ProxyServer] OK"

	def init_proxy_server(self):
		for sim in self.simulator_manager.get_simulator_list():
			opensim_proxy = OpensimProxy(sim)
			self.add_opensim_proxy(opensim_proxy)

	def get_apache_proxy(self):
		return self.apache_proxy

	def get_mysql_proxy(self):
		return self.mysql_proxy

	def get_robust_proxy(self):
		return self.robust_proxy

	def add_opensim_proxy(self,opensim_proxy):
		self.opensim_proxy_list.append(opensim_proxy)

	def get_opensim_proxy_list(self):
		return self.opensim_proxy_list

	def start(self):
	 	print "[ProxyServer] start..."
		self.apache_proxy.start()
		self.mysql_proxy.start()
		self.robust_proxy.start()
		for opensim_proxy in self.get_opensim_proxy_list():
			opensim_proxy.start()

	def stop(self):
	 	print "[ProxyServer] stop..."
		self.tool.nat_flush_all_chains()
		print self.tool.nat_list_all_chains()

class ProxyServerTesting(ProxyServer):
	pass
