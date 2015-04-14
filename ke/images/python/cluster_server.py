"""
Class Hierarchy

G{classtree: ClusterServer} 

Package tree
G{packagetree: cluster_server} 

Import Graph
G{importgraph: cluster_server} 

"""
from cluster_manager import ClusterManager
from proxy_server import ProxyServer

class ClusterServer:

	def __init__(self,global_region_data_dict):
		# cluster manager
		self.cluster_manager = ClusterManager(global_region_data_dict)
		""" @type: L{ClusterManager} """

		# proxy server
		simulator_manager = self.cluster_manager.get_opensim_pod_manager().get_simulator_manager()
		self.proxy_server = ProxyServer(simulator_manager)
		""" @type: L{ProxyServer} """

		# monitor 

	def start(self):
	 	print "[ClusterServer] start..."
		self.cluster_manager.start()
		self.proxy_server.start()

	def stop(self):
	 	print "[ClusterServer] stop..."
		self.cluster_manager.stop()
		self.proxy_server.stop()

class ClusterServerTesting(ClusterServer):
	pass
