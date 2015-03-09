#/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import uuid

from docker_client import *

# opensim related
#HOST_NAME = "virgeo.pku.edu.cn"
#REGIONLOAD_WEB_URL_PREFIX = "http://virgeo.pku.edu.cn:880/region_load/"
HOST_NAME =  HOST_IP
REGIONLOAD_WEB_URL_PREFIX = "http://{0}:880/region_load/".format(HOST_NAME)
# base/vgeo/opensim/project/
# base/apache/var/www/region_load/
APACHE_LOCAL_DIR = os.getcwd()+"/../../../apache/var/www/region_load/"
INTERNAL_ADDRESS = "0.0.0.0"
ALLOW_ALTERNATE_PORTS = False
MAX_AGENTS = 100
MAX_PRIMS = 15000

GLOBAL_REGION_DATA = {
	"huyu":
		{"orig":(1000,1000), "startPort":9000, "wh":(4,7)},
	"xwd":
		{"orig":(1005,1000), "startPort":9050, "wh":(5,7)},
	"newregion":
		{"orig":(1010,1000), "startPort":9100, "wh":(10,10)}
	}
SIM_START_PORT = 8800
SIM_MAX_COUNT = 200

CLUSTER_DATA_DIR = "./cluster_data/"

class Region:
	"""
	region
	"""
	def __init__(self,name,uuid,loc_x,loc_y,internal_address,port,allow_alternate_ports,hostname,max_agents,max_prims):
		self.name = name
		self.uuid = uuid
		self.loc_x = loc_x
		self.loc_y = loc_y
		self.internal_address = internal_address
		self.port = port
		self.allow_alternate_ports = allow_alternate_ports
		self.hostname = hostname
		self.max_agents = max_agents
		self.max_prims = max_prims

	#====================================================================================
	# to ini
	#====================================================================================
	def __to_ini(self,region_name,region_uuid,loc_x,loc_y,internal_address,region_port,allow_alternate_ports,hostname,max_agents,max_prims):
		ini_format = "[{0}]\nRegionUUID = {1}\nLocation = {2},{3}\nInternalAddress = {4}\nInternalPort = {5}\nAllowAlternatePorts = {6}\nExternalHostName = {7}\nMaxAgents = {8}\nMaxPrims = {9}\n".format(region_name,region_uuid,loc_x,loc_y,internal_address,region_port,allow_alternate_ports,hostname,max_agents,max_prims)
		return ini_format

	#====================================================================================
	# to xml
	#====================================================================================
	def __to_xml(self,region_name,region_uuid,loc_x,loc_y,internal_address,region_port,allow_alternate_ports,hostname,max_agents,max_prims):
		xml_format = '  <Section Name="{0}" >\n	<Key Name ="RegionUUID" Value = "{1}" />\n	<Key Name ="Location" Value = "{2},{3}" />\n 	<Key Name ="InternalAddress" Value = "{4}" />\n 	<Key Name ="InternalPort" Value = "{5}" />\n 	<Key Name ="AllowAlternatePorts" Value = "{6}" />\n 	<Key Name ="ExternalHostName" Value = "{7}" />\n 	<Key Name ="MaxAgents" Value = "{8}" />\n 	<Key Name ="MaxPrims" Value = "{9}" />\n  </Section>\n'.format(region_name,region_uuid,loc_x,loc_y,internal_address,region_port,allow_alternate_ports,hostname,max_agents,max_prims)
		return xml_format

	def to_ini(self):
		return self.__to_ini(self.name,self.uuid,self.loc_x,self.loc_y,self.internal_address,self.port,self.allow_alternate_ports,self.hostname,self.max_agents,self.max_prims)

	def to_xml(self):
		return self.__to_xml(self.name,self.uuid,self.loc_x,self.loc_y,self.internal_address,self.port,self.allow_alternate_ports,self.hostname,self.max_agents,self.max_prims)

	def str(self):
		str_format = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}"
		return str_format.format(self.name,self.uuid,self.loc_x,self.loc_y,self.internal_address,self.port,self.allow_alternate_ports,self.hostname,self.max_agents,self.max_prims)

	def get_region_name(self):
		return self.name

	def get_region_uuid(self):
		return self.uuid

	def get_region_location_x(self):
		return self.loc_x

	def get_region_location_y(self):
		return self.loc_y

	def get_region_port(self):
		return self.port

	def get_allow_alternate_ports(self):
		return self.allow_alternate_ports

	def get_hostname(self):
		return self.hostname

	def get_max_agents(self):
		return self.max_agents

	def get_max_prims(self):
		return self.max_prims

class RegionPool:
	"""
	region pool
	"""
	def __init__(self,global_region_data):
		self.filepath = CLUSTER_DATA_DIR+"region_pool"

		self.global_region_data = global_region_data
		self.region_list = []

	#====================================================================================
	# init region pool
	#====================================================================================
	def init_region_pool(self):
		if os.path.exists(self.filepath):
			print "[REGION POOL]read region pool from {0}...".format(self.filepath)
			self.__read_region_pool(self.filepath)
		else:
			print "[REGION POOL]create region pool for the first time..."
			self.__create_region_pool()
			print "[REGION POOL]save region pool to {0}...".format(self.filepath)
			self.__save_region_pool(self.filepath)

	def __create_region_pool(self):
		global_region_data = self.global_region_data
		self.region_dict = []
		for region_group in global_region_data:
			wh = global_region_data[region_group]["wh"]
			xmax = wh[0]
			ymax = wh[1]
			for x in range(xmax):
				for y  in range(ymax):
					# create a region
					region = self.__create_region(region_group,x,y,global_region_data)
					self.region_list.append(region)

	def __save_region_pool(self,filepath):
		with open(filepath,'w') as f:
			for region in self.region_list:
				line = region.str()+"\n"
				f.write(line)

	def __read_region_pool(self,filepath):
		for line in open(filepath,'r'):
			region = self.__read_region(line)
			self.region_list.append(region)		

	#====================================================================================
	# create region 
	#====================================================================================
	def __create_region(self,region_group,relative_location_x,relative_location_y,global_region_data):
		x = relative_location_x
		y = relative_location_y

		# fields
		region_name = "{0}{1}{2}".format(region_group,x,y)
		region_uuid = uuid.uuid1()

		# region absolute loc
		orig = global_region_data[region_group]["orig"]
		region_location_x = orig[0]+x
		region_location_y = orig[1]+y

		internal_address = INTERNAL_ADDRESS

		# region port
		start_port = global_region_data[region_group]["startPort"]
		region_port = start_port+10*x+y

		allow_alternate_ports = ALLOW_ALTERNATE_PORTS
		hostname = HOST_NAME
		max_agents = MAX_AGENTS
		max_prims = MAX_PRIMS

		# create region config
		region = Region(region_name,region_uuid,region_location_x,region_location_y,internal_address,region_port,allow_alternate_ports,hostname,max_agents,max_prims)
		return region

	#====================================================================================
	# read region from region string
	#====================================================================================
	def __read_region(self,region_str):
		parts = region_str.rstrip("\n").split(",")
		region_name = parts[0]
		region_uuid = parts[1]
		region_location_x = int(parts[2])
		region_location_y = int(parts[3])
		internal_address = parts[4]
		region_port = int(parts[5])
		allow_alternate_ports = bool(parts[6])
		hostname = parts[7]
		max_agents = int(parts[8])
		max_prims = int(parts[9])

		# create region config
		region = Region(region_name,region_uuid,region_location_x,region_location_y,internal_address,region_port,allow_alternate_ports,hostname,max_agents,max_prims)
		return region
		
	def __split_region_name(self,region_name):
		# huyu36  xwd46 newregion99
		len_rn = len(region_name)
		xy = region_name[-2:]
		region_group = region_name[:len_rn-2]
		x = int(xy[0])
		y = int(xy[1])
		return region_group,x,y

	#====================================================================================
	# get region from region pool
	#====================================================================================
	def get_region(self,region_name):
		"""
		get region from region pool by region name
		"""
		for region in self.region_list:
			if region.get_region_name() == region_name :
				print "[REGION POOL]{0} found.".format(region_name)
				return region
		print "[REGION POOL]{0} does not exist.".format(region_name)
		return None

class Simulator:
	"""
	a simulator hosts N regions
	create a simulator ini/xml file containing N region ini/xml section
	"""
	def __init__(self,sim_name,sim_port,region_pool,region_name_list):
		self.sim_name = sim_name
		self.sim_port = sim_port
		self.region_pool = region_pool

		# simulator region list
		self.region_list = []
		for region_name in region_name_list:
			self.add_region(region_name)

		# simulator ini
		self.simulator_ini_string = ""
		self.simulator_ini_filename = self.sim_name + ".ini"
		self.simulator_ini_filepath = APACHE_LOCAL_DIR + self.simulator_ini_filename

		# simulator xml
		self.simulator_xml_string = ""
		self.simulator_xml_filename = self.sim_name + ".xml"
		self.simulator_xml_filepath = APACHE_LOCAL_DIR + self.simulator_xml_filename

		# regionload_web_url
		# regionload_web_url="http://162.105.17.48/region_load/huyu.xml"
		self.regionload_web_url= REGIONLOAD_WEB_URL_PREFIX + self.simulator_xml_filename

	def str(self):
		# sim_name,sim_port,r1,r2,r3,r4...
		str_format = "{0},{1}".format(self.sim_name,self.sim_port)

		for region in self.region_list:
			region_name = region.get_region_name()
			str_format += ","+region_name
		return str_format

	#================================================================================
	# add region
	#================================================================================
	def add_region(self,region_name):
		region = self.region_pool.get_region(region_name)
		if region:
			self.region_list.append(region)

	#================================================================================
	# remove region
	#================================================================================
	def remove_region(self,region_name):
		region = self.region_pool.get_region(region_name)
		if region:
			self.region_list.remove(region)

	def get_simulator_name(self):
		return self.sim_name 

	def get_simulator_port(self):
		return self.sim_port 

	def get_region_list(self):
		return self.region_list

	def get_regionload_web_url(self):
		return self.regionload_web_url 

	#================================================================================
	# get region port list
	#================================================================================
	def get_region_port_list(self):
		"""
		get region port list by region list
		"""
		self.region_port_list = []
		for region in self.region_list:
			port = region.get_region_port()
			self.region_port_list.append(port)
		return self.region_port_list

	def __save_file(self,filename,content):
		with open(filename,"w") as f:
			f.write(content)
		print filename + " generated"

	#================================================================================
	# create ini file
	#================================================================================
	def create_simulator_ini_file(self):
		self.simulator_ini_string = ""
		for region in self.region_list:
			self.simulator_ini_string += region.to_ini()
		self.__save_file(self.simulator_ini_filepath,self.simulator_ini_string)

	#================================================================================
	# create xml file
	#================================================================================
	def create_simulator_xml_file(self):
		self.simulator_xml_string = ""
		# add xml header
		self.simulator_xml_string += "<Nini>\n"
		for region in self.region_list:
			self.simulator_xml_string += region.to_xml()
		# add xml tail
		self.simulator_xml_string += "</Nini>"
		self.__save_file(self.simulator_xml_filepath,self.simulator_xml_string)

class SimulatorCluster:
	"""
	a cluster has N simulators
	"""
	def __init__(self,cluster_name,region_pool):
		self.filepath = CLUSTER_DATA_DIR+"cluster"

		self.cluster_name = cluster_name
		self.region_pool = region_pool

		# simulator list
		self.simulator_list = []

	def get_cluster_name(self):
		return self.cluster_name

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
			print "[CLUSTER]read cluster data from {0}...".format(self.filepath)
			self.__read_cluster_data(self.filepath)
		else:
			print "[CLUSTER]create default cluster for the first time..."
			self.__create_default_cluster()
			print "[CLUSTER]save cluster data to {0}...".format(self.filepath)
			#self.__save_cluster_data(self.filepath)

	def __new_simulator_name(self):
		sim_count = len(self.simulator_list)
		if sim_count >= SIM_MAX_COUNT:
			print "[Warning] sim_count >={0}".format(SIM_MAX_COUNT)
			return "default"
		return "sim_{0}".format(sim_count)

	def __new_simulator_port(self):
		sim_count = len(self.simulator_list)
		if sim_count >= SIM_MAX_COUNT:
			print "[Warning] sim_count >={0}".format(SIM_MAX_COUNT)
			return SIM_START_PORT
		return SIM_START_PORT+sim_count
	#====================================================================================
	# create default cluster
	#====================================================================================
	def __create_default_cluster(self):
		self.simulator_list = []
		region_pool = self.region_pool
		global_region_data = self.region_pool.global_region_data
		
		# huyu
		sim_name = self.__new_simulator_name()
		sim_port = self.__new_simulator_port()
		region_name_list = self.__get_region_name_list("huyu",global_region_data)
		huyu_sim = Simulator(sim_name,sim_port,region_pool,region_name_list)
		# create xml file
		huyu_sim.create_simulator_xml_file()
		self.add_simulator(huyu_sim)

		# xwd
		sim_name = self.__new_simulator_name()
		sim_port = self.__new_simulator_port()
		region_name_list = self.__get_region_name_list("xwd",global_region_data)
		xwd_sim = Simulator(sim_name,sim_port,region_pool,region_name_list)
		# create xml file
		xwd_sim.create_simulator_xml_file()
		self.add_simulator(xwd_sim)

		# newregion
		sim_name = self.__new_simulator_name()
		sim_port = self.__new_simulator_port()
		#region_name_list = self.__get_region_name_list("newregion",global_region_data)
		region_name_list = ["newregion00","newregion01"]
		new_sim = Simulator(sim_name,sim_port,region_pool,region_name_list)
		# create xml file
		new_sim.create_simulator_xml_file()
		self.add_simulator(new_sim)

		print huyu_sim.get_region_port_list()
		print xwd_sim.get_region_port_list()

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
			sim_name = sim.get_simulator_name()
			sim_port = sim.get_simulator_port()
			region_port_list = sim.get_region_port_list()
			regionload_web_url = sim.get_regionload_web_url()
			# run N opensim container
			sim_container = OpensimContainer(DOCKER_SERVER_URL,OPENSIM_BASE_IMAGE,CPU_SHARES,MEM_LIMIT,OPENSIM_LINKS,OPENSIM_COMMAND,HOST_IP,sim_name,sim_port,region_port_list,regionload_web_url)
			sim_container.start()

def test_cluster():
	region_pool = RegionPool(GLOBAL_REGION_DATA)
	region_pool.init_region_pool()

	cluster = SimulatorCluster("Virgeo OpenSimulator Cluster",region_pool)
	cluster.init_cluster()
	cluster.start()

def main():
	test_cluster()

if __name__=="__main__":
	main()
