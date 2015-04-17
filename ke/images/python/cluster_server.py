"""
Class Hierarchy

G{classtree: ClusterServer} 

Package tree
G{packagetree: cluster_server} 

Import Graph
G{importgraph: cluster_server} 

"""
from cluster_manager import ClusterManager
from cluster_monitor import ClusterMonitor
from cluster_proxy import ClusterProxy

class ClusterServer:

	def __init__(self,global_region_data_dict,global_load_data_dict):
		print "[ClusterServer] init ..."
		# cluster manager
		self.cluster_manager = ClusterManager(global_region_data_dict)
		""" @type: L{ClusterManager} """

		# proxy server
		simulator_manager = self.cluster_manager.get_pod_manager().get_simulator_manager()
		self.cluster_proxy = ClusterProxy(simulator_manager)
		""" @type: L{ClusterProxy} """

		# cluster monitor 
		controller_manager = self.cluster_manager.get_controller_manager()
		self.cluster_monitor = ClusterMonitor(controller_manager,global_load_data_dict)
		""" @type: L{ClusterMonitor} """
		print "[ClusterServer] OK" 

	def start(self):
	 	print "[ClusterServer] start..."
		self.cluster_manager.start()
		self.cluster_proxy.start()
		self.cluster_monitor.start()

	def stop(self):
	 	print "[ClusterServer] stop..."
		self.cluster_manager.stop()
		self.cluster_proxy.stop()
		self.cluster_monitor.stop()

class ClusterServerTesting(ClusterServer):
	pass
