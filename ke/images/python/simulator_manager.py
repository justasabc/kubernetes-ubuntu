"""
Class Hierarchy

G{classtree: SimulatorManager} 

Package tree
G{packagetree: simulator_manager} 

Import Graph
G{importgraph: simulator_manager} 

"""
from cluster_tool import KubernetesTool
from region_pool import RegionPool
from simulator import Simulator

# minions related
MINIONS=["minion1","minion2","minion3"]

class SimulatorManager:

	def __init__(self,global_region_data_dict):
		print "[SimulatorManager] init ..." 
		self.region_pool = RegionPool(global_region_data_dict)
		""" @type: L{RegionPool} """

		self.simulator_list = []
		""" @type: L{Simulator} """

		self.tool = KubernetesTool()		
		#""" @type: L{KubernetesTool} """

		self.init_simulator_manager()
		print "[SimulatorManager] OK"

	def init_simulator_manager(self):
		global_region_data = self.get_global_region_data()
		for region_group in global_region_data.get_region_group_list():
			sim_name = region_group
			sim_port = global_region_data.get_sim_port(region_group)
			region_name_list = global_region_data.get_region_name_list(region_group)
			print "*"*60
			sim = Simulator(sim_name,sim_port,region_name_list,self.region_pool)
			# create xml file
			sim.create_simulator_xml_file()
			print "*"*60

			self.add_simulator(sim)
			#print sim.get_region_port_list()

		# copy xml files to minions
		self.tool.copy_region_xml_to_minions(MINIONS)

	def get_region_pool(self):
		return self.region_pool

	def get_global_region_data(self):
		return self.region_pool.get_global_region_data()

	def add_simulator(self,sim):
		print "[SimulatorManager] add {0} to simulator_list".format(sim.get_simulator_name())
		self.simulator_list.append(sim)

	def remove_simulator(self,sim):
		self.simulator_list.remove(sim)

	def get_simulator_list(self):
		return self.simulator_list

	def get_simulator_count(self):
		return len(self.simulator_list)

class SimulatorManagerTesting(SimulatorManager):
	pass
