
class Cluster:
	"""
	a cluster has N simulators
	"""
	def __init__(self,region_pool):
		self.region_pool = region_pool
		self.filepath = CLUSTER_DATA_DIR+"cluster"

		# simulator list
		self.simulator_list = []

	def get_simulator_list(self):
		return self.simulator_list

	def get_simulator_count(self):
		return len(self.simulator_list)

	def add_simulator(self,sim):
		self.simulator_list.append(sim)

	def remove_simulator(self,sim):
		self.simulator_list.remove(sim)

	#====================================================================================
	# get region name list
	#====================================================================================
	def __get_region_name_list(self,region_group,global_region_data):
		#REGION_NAME_HUYU=["huyu"+str(x)+str(y) for x in range(4) for y in range(7)]
		wh = global_region_data[region_group]["wh"]
		xmax = wh[0]
		ymax = wh[1]
		region_name_list = ["{0}{1}{2}".format(region_group,x,y) for x in range(xmax) for y in range(ymax)]
		return region_name_list

	#====================================================================================
	# init cluster
	#====================================================================================
	def init_cluster(self):
		if os.path.exists(self.filepath):
			print "[Cluster] read cluster data from {0}...".format(self.filepath)
			self.__read_cluster_data(self.filepath)
		else:
			print "[Cluster] create default cluster for the first time..."
			self.__create_default_cluster()
			print "[Cluster] save cluster data to {0}...".format(self.filepath)
			self.__save_cluster_data(self.filepath)

	def __new_simulator_name(self):
		sim_count = len(self.simulator_list)
		if sim_count >= SIM_MAX_COUNT:
			print "[Warning] sim_count >={0}".format(SIM_MAX_COUNT)
			return "default"
		return "sim{0}".format(sim_count+1)

	def __new_simulator_port(self):
		sim_count = len(self.simulator_list)
		if sim_count >= SIM_MAX_COUNT:
			print "[Warning] sim_count >={0}".format(SIM_MAX_COUNT)
			return SIM_START_PORT
		return SIM_START_PORT+(sim_count+1)

	#====================================================================================
	# create default cluster
	#====================================================================================
	def __create_default_cluster(self):
		self.simulator_list = []
		region_pool = self.region_pool
		global_region_data = self.region_pool.get_global_region_data()
		
		# huyu
		region_group="huyu"
		sim_name = self.__new_simulator_name()
		sim_port = self.__new_simulator_port()
		region_name_list = self.__get_region_name_list(region_group,global_region_data)
		huyu_sim = Simulator(sim_name,sim_port,region_pool,region_name_list)
		# create xml file
		huyu_sim.create_simulator_xml_file()
		self.add_simulator(huyu_sim)

		# xwd
		region_group="xwd"
		sim_name = self.__new_simulator_name()
		sim_port = self.__new_simulator_port()
		region_name_list = self.__get_region_name_list(region_group,global_region_data)
		xwd_sim = Simulator(sim_name,sim_port,region_pool,region_name_list)
		# create xml file
		xwd_sim.create_simulator_xml_file()
		self.add_simulator(xwd_sim)

		# newregion
		region_group="newregion"
		sim_name = self.__new_simulator_name()
		sim_port = self.__new_simulator_port()
		#region_name_list = self.__get_region_name_list("newregion",global_region_data)
		region_name_list = self.__get_region_name_list(region_group,global_region_data)
		#region_name_list = ["newregion00","newregion01"]
		new_sim = Simulator(sim_name,sim_port,region_pool,region_name_list)
		# create xml file
		new_sim.create_simulator_xml_file()
		self.add_simulator(new_sim)

		print huyu_sim.get_region_port_list()
		print xwd_sim.get_region_port_list()
		print new_sim.get_region_port_list()

		# copy xml files to minions
		cmd = UtilityCommander()		
		cmd.copy_region_xml_to_minions(MINIONS)

	def __save_cluster_data(self,filepath):
		with open(filepath,'w') as f:
			for sim in self.simulator_list:
				line = sim.str()+"\n"
				f.write(line)

	def __read_cluster_data(self,filepath):
		for line in open(filepath,'r'):
			sim = self.__read_simulator(line)
			self.add_simulator(sim)

	#====================================================================================
	# read simulator from simulator string
	#====================================================================================
	def __read_simulator(self,simulator_str):
		parts = simulator_str.rstrip("\n").split(",")
		sim_name = parts[0]
		sim_port = int(parts[1])
		region_name_list = parts[2:]

		# create simulator
		sim = Simulator(sim_name,sim_port,self.region_pool,region_name_list)
		return sim

	def start(self):
		for sim in self.get_simulator_list():
			sim_pod = OpensimPod(sim)
			#sim_pod.start()

	def stop(self):
		for sim in self.get_simulator_list():
			sim_pod = OpensimPod(sim)
			sim_pod.stop()
