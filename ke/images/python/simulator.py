"""
Class Hierarchy

G{classtree: Simulator} 

Package tree
G{packagetree: simulator} 

Import Graph
G{importgraph: simulator} 

"""
#/usr/bin/python
# -*- coding:utf-8 -*-
from region_pool import RegionPool

class Simulator:
	"""
	a simulator hosts N regions
	create a simulator ini/xml file containing N region ini/xml section
	"""
	def __init__(self,sim_name,sim_port,region_name_list,region_pool):
		print "[Simulator] init {0}...".format(sim_name)
		self.sim_name = sim_name
		""" @type: C{string} """
		self.sim_port = sim_port
		""" @type: C{integer} """
		self.region_name_list = region_name_list
		""" @type: C{list} """
		self.region_pool = region_pool
		""" @type: L{RegionPool} """

		# simulator region list
		self.region_list = []
		""" @type: L{Region} """
		print "[Simulator] get region(s) from pool & add region(s) to simulator"
		for region_name in region_name_list:
			self.add_region(region_name)

		# simulator ini
		self.simulator_ini_filename = self.sim_name + ".ini"
		""" @type: C{string} """
		self.simulator_ini_filepath = "./ini/"+ self.simulator_ini_filename
		""" @type: C{string} """

		# simulator xml
		self.simulator_xml_filename = self.sim_name + ".xml"
		""" @type: C{string} """
		self.simulator_xml_filepath = "./xml/" + self.simulator_xml_filename
		""" @type: C{string} """
		print "[Simulator] {0} OK".format(sim_name)

	def str(self):
		# sim_name,sim_port,r1,r2,r3,r4...
		str_format = "{0},{1}".format(self.sim_name,self.sim_port)

		for region in self.region_list:
			region_name = region.get_region_name()
			str_format += ","+region_name
		return str_format

	def add_region(self,region_name):
		region = self.region_pool.get_region(region_name)
		if region:
			self.region_list.append(region)

	def remove_region(self,region_name):
		region = self.region_pool.get_region(region_name)
		if region:
			self.region_list.remove(region)

	def get_simulator_name(self):
		return self.sim_name 

	def get_simulator_port(self):
		return self.sim_port 

	def get_region_name_list(self):
		return self.region_name_list

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

	def save_file(self,filename,content):
		with open(filename,"w") as f:
			f.write(content)
		print "[Simulator] write {0} to file".format(filename)

	#================================================================================
	# create ini file
	#================================================================================
	def create_simulator_ini_file(self):
		self.simulator_ini_string = ""
		for region in self.region_list:
			self.simulator_ini_string += region.to_ini()
		self.save_file(self.simulator_ini_filepath,self.simulator_ini_string)

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
		self.save_file(self.simulator_xml_filepath,self.simulator_xml_string)


class SimulatorTesting(Simulator):
	pass
