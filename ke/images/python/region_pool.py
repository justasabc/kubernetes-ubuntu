"""
Class Hierarchy

G{classtree: RegionPool} 

Package tree
G{packagetree: region_pool} 

Import Graph
G{importgraph: region_pool} 

"""

#/usr/bin/python
# -*- coding:utf-8 -*-
import uuid
import os 
from setting import *
from region import Region
from global_region_data import GlobalRegionData

class RegionPool:
	"""
	region pool
	"""
	def __init__(self,global_region_data_dict):
		print "[RegionPool] init ..."
		self.filepath = CLUSTER_DATA_DIR+"region_pool"
		""" @type: C{string} """
		self.global_region_data = GlobalRegionData(global_region_data_dict)
		""" @type: C{GlobalRegionData} """
		self.region_list = []
		""" @type: L{Region} """

		self.init_region_pool()
		print "[RegionPool] OK"

	def get_global_region_data(self):
		return self.global_region_data

	def get_region_list(self):
		return self.region_list

	#====================================================================================
	# init region pool
	#====================================================================================
	def init_region_pool(self):
		if os.path.exists(self.filepath):
			self.read_region_pool(self.filepath)
		else:
			self.create_region_pool()
			self.save_region_pool(self.filepath)

	def create_region_pool(self):
		print "[RegionPool] create region pool for the first time..."
		self.region_dict = []
		for region_group in self.global_region_data.get_region_group_list():
			#wh = global_region_data[region_group]["wh"]
			#xmax = wh[0]
			#ymax = wh[1]
			xmax = self.global_region_data.get_region_width(region_group)
			ymax = self.global_region_data.get_region_height(region_group)
			for x in range(xmax):
				for y  in range(ymax):
					# create a region
					region = self.create_region(region_group,x,y)
					self.region_list.append(region)

	def save_region_pool(self,filepath):
		print "[RegionPool] save region pool to {0}...".format(filepath)
		with open(filepath,'w') as f:
			for region in self.region_list:
				line = region.str()+"\n"
				f.write(line)

	def read_region_pool(self,filepath):
		print "[RegionPool] read region pool from {0}...".format(filepath)
		for line in open(filepath,'r'):
			region = self.read_region(line)
			self.region_list.append(region)		

	#====================================================================================
	# create new region 
	#====================================================================================
	def create_region(self,region_group,relative_location_x,relative_location_y):
		x = relative_location_x
		y = relative_location_y

		# fields
		region_name = "{0}{1}{2}".format(region_group,x,y)
		region_uuid = uuid.uuid1()

		# region absolute location
		#orig = global_region_data[region_group]["orig"]
		orig = self.global_region_data.get_region_orig(region_group)
		region_location_x = orig[0]+x
		region_location_y = orig[1]+y

		internal_address = INTERNAL_ADDRESS

		# region port
		#start_port = global_region_data[region_group]["start_port"]
		start_port = self.global_region_data.get_region_start_port(region_group)
		region_port = start_port+10*x+y

		allow_alternate_ports = ALLOW_ALTERNATE_PORTS
		external_hostname = EXTERNAL_HOSTNAME
		max_agents = MAX_AGENTS
		max_prims = MAX_PRIMS

		# create region config
		region = Region(region_name,region_uuid,region_location_x,region_location_y,internal_address,region_port,allow_alternate_ports,external_hostname,max_agents,max_prims)
		return region

	#====================================================================================
	# read region from region string
	#====================================================================================
	def read_region(self,region_str):
		parts = region_str.rstrip("\n").split(",")
		region_name = parts[0]
		region_uuid = parts[1]
		region_location_x = int(parts[2])
		region_location_y = int(parts[3])
		internal_address = parts[4]
		region_port = int(parts[5])
		allow_alternate_ports = bool(parts[6])
		external_hostname = parts[7]
		max_agents = int(parts[8])
		max_prims = int(parts[9])

		# create region config
		region = Region(region_name,region_uuid,region_location_x,region_location_y,internal_address,region_port,allow_alternate_ports,external_hostname,max_agents,max_prims)
		return region
		
	"""
	def __split_region_name(self,region_name):
		# huyu36  xwd46 newregion99
		len_rn = len(region_name)
		xy = region_name[-2:]
		region_group = region_name[:len_rn-2]
		x = int(xy[0])
		y = int(xy[1])
		return region_group,x,y
	"""

	#====================================================================================
	# get region from region pool by region name
	#====================================================================================
	def get_region(self,region_name):
		#print "[RegionPool] get {} from region pool...".format(region_name)
		for region in self.region_list:
			if region.get_region_name() == region_name :
				#print "[REGION POOL]{0} found.".format(region_name)
				return region
		print "[RegionPool] {0} does not exist.".format(region_name)
		return None

class RegionPoolTesting(RegionPool):
	pass
