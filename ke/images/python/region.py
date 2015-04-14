"""
Class Hierarchy

G{classtree: Region} 

Package tree
G{packagetree: region} 

Import Graph
G{importgraph: region} 

"""

#/usr/bin/python
# -*- coding:utf-8 -*-

from setting import *

class Region:
	"""
	region fields
	"""
	def __init__(self,name,uuid,loc_x,loc_y,internal_address,port,allow_alternate_ports,external_hostname,max_agents,max_prims):
		#print "[Region] init region {0}".format(name)
		self.name = name
		self.uuid = uuid
		self.loc_x = loc_x
		self.loc_y = loc_y
		self.internal_address = internal_address
		self.port = port
		self.allow_alternate_ports = allow_alternate_ports
		self.external_hostname = external_hostname
		self.max_agents = max_agents
		self.max_prims = max_prims

	#====================================================================================
	# to ini
	#====================================================================================
	def __to_ini(self,region_name,region_uuid,loc_x,loc_y,internal_address,region_port,allow_alternate_ports,external_hostname,max_agents,max_prims):
		ini_format = "[{0}]\nRegionUUID = {1}\nLocation = {2},{3}\nInternalAddress = {4}\nInternalPort = {5}\nAllowAlternatePorts = {6}\nExternalHostName = {7}\nMaxAgents = {8}\nMaxPrims = {9}\n".format(region_name,region_uuid,loc_x,loc_y,internal_address,region_port,allow_alternate_ports,external_hostname,max_agents,max_prims)
		return ini_format

	#====================================================================================
	# to xml
	#====================================================================================
	def __to_xml(self,region_name,region_uuid,loc_x,loc_y,internal_address,region_port,allow_alternate_ports,external_hostname,max_agents,max_prims):
		xml_format = '  <Section Name="{0}" >\n	<Key Name ="RegionUUID" Value = "{1}" />\n	<Key Name ="Location" Value = "{2},{3}" />\n 	<Key Name ="InternalAddress" Value = "{4}" />\n 	<Key Name ="InternalPort" Value = "{5}" />\n 	<Key Name ="AllowAlternatePorts" Value = "{6}" />\n 	<Key Name ="ExternalHostName" Value = "{7}" />\n 	<Key Name ="MaxAgents" Value = "{8}" />\n 	<Key Name ="MaxPrims" Value = "{9}" />\n  </Section>\n'.format(region_name,region_uuid,loc_x,loc_y,internal_address,region_port,allow_alternate_ports,external_hostname,max_agents,max_prims)
		return xml_format

	def to_ini(self):
		return self.__to_ini(self.name,self.uuid,self.loc_x,self.loc_y,self.internal_address,self.port,self.allow_alternate_ports,self.external_hostname,self.max_agents,self.max_prims)

	def to_xml(self):
		return self.__to_xml(self.name,self.uuid,self.loc_x,self.loc_y,self.internal_address,self.port,self.allow_alternate_ports,self.external_hostname,self.max_agents,self.max_prims)

	def str(self):
		str_format = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}"
		return str_format.format(self.name,self.uuid,self.loc_x,self.loc_y,self.internal_address,self.port,self.allow_alternate_ports,self.external_hostname,self.max_agents,self.max_prims)

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

	def get_external_hostname(self):
		return self.external_hostname

	def get_max_agents(self):
		return self.max_agents

	def get_max_prims(self):
		return self.max_prims


class RegionTesting(Region):
	pass
