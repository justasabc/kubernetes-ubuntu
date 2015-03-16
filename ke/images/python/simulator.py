#/usr/bin/python
# -*- coding:utf-8 -*-

from setting import *

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

