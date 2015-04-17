"""
Class Hierarchy

G{classtree: PodManager} 

Package tree
G{packagetree: pod_manager} 

Import Graph
G{importgraph: pod_manager} 

"""

from pod import *
from simulator_manager import SimulatorManager

class PodManager:

	def __init__(self,global_region_data_dict):
		print "[PodManager] init ..." 
		self.simulator_manager = SimulatorManager(global_region_data_dict)
		""" @type: L{SimulatorManager} """

		self.pod_list = []
		""" @type: L{BasePod} """

		self.init_pod_manager()
		print "[PodManager] OK"

	def init_pod_manager(self):
		sim_list = self.simulator_manager.get_simulator_list()
		for sim in sim_list:
			# opensim pod
			pod = OpensimPod(sim)
			self.add_pod(pod)

	def get_simulator_manager(self):
		return self.simulator_manager

	def add_pod(self,pod):
		self.pod_list.append(pod)

	def remove_pod(self,pod):
		self.pod_list.remove(pod)

	def get_pod_list(self):
		return self.pod_list

	def get_pod_count(self):
		return len(self.pod_list)

	def start(self):
		for pod in self.pod_list:
			pod.start()

	def stop(self):
		for pod in self.pod_list:
			pod.stop()

class PodManagerTesting(PodManager):
	pass
