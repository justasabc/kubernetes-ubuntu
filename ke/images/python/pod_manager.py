"""
Class Hierarchy

G{classtree: OpensimPodManager} 

Package tree
G{packagetree: pod_manager} 

Import Graph
G{importgraph: pod_manager} 

"""

from pod import OpensimPod
from simulator_manager import SimulatorManager

class OpensimPodManager:

	def __init__(self,global_region_data_dict):
		print "[OpensimPodManager] init ..." 
		self.simulator_manager = SimulatorManager(global_region_data_dict)
		""" @type: L{SimulatorManager} """

		self.opensim_pod_list = []
		""" @type: L{OpensimPod} """

		self.init_opensim_pod_manager()
		print "[OpensimPodManager] OK"

	def init_opensim_pod_manager(self):
		sim_list = self.simulator_manager.get_simulator_list()
		for sim in sim_list:
			pod = OpensimPod(sim)
			self.add_opensim_pod(pod)

	def get_simulator_manager(self):
		return self.simulator_manager

	def add_opensim_pod(self,pod):
		self.opensim_pod_list.append(pod)

	def remove_opensim_pod(self,pod):
		self.opensim_pod_list.remove(pod)

	def get_opensim_pod_list(self):
		return self.opensim_pod_list

	def get_opensim_pod_count(self):
		return len(self.opensim_pod_list)

	def start(self):
		for pod in self.opensim_pod_list:
			pod.start()

	def stop(self):
		for pod in self.opensim_pod_list:
			pod.stop()

class OpensimPodManagerTesting(OpensimPodManager):
	pass
