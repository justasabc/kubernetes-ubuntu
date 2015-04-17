"""
Class Hierarchy

G{classtree: ClusterProxy} 

Package tree
G{packagetree: cluster_proxy} 

Import Graph
G{importgraph: cluster_proxy} 

"""
from proxy import *

class ClusterProxy:
	"""
	1 ApacheProxy + 1 MysqlProxy + 1 RobustProxy + N OpensimProxy
	"""

	def __init__(self,simulator_manager):
	 	print "[ClusterProxy] init..."
		self.simulator_manager = simulator_manager
		#""" @type: L{SimulatorManager} """

		self.apache_proxy = ApacheProxy()
		""" @type: L{ApacheProxy} """
		self.mysql_proxy = MysqlProxy()
		""" @type: L{MysqlProxy} """
		self.robust_proxy = RobustProxy()
		""" @type: L{RobustProxy} """
		self.opensim_proxy_list = []
		""" @type: L{OpensimProxy} """

		self.init_proxy_server()
	 	print "[ClusterProxy] OK"

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
		self.stop()

	 	print "[ClusterProxy] start..."
		self.apache_proxy.start()
		self.mysql_proxy.start()
		self.robust_proxy.start()
		for opensim_proxy in self.get_opensim_proxy_list():
			opensim_proxy.start()

	def stop(self):
	 	print "[ClusterProxy] stop..."
		self.apache_proxy.stop()
		#self.mysql_proxy.stop()
		#self.robust_proxy.stop()
		#for opensim_proxy in self.get_opensim_proxy_list():
		#	opensim_proxy.stop()

class ClusterProxyTesting(ClusterProxy):
	pass
