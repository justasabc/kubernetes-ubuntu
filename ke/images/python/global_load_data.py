"""
Class Hierarchy

G{classtree: GlobalLoadData} 

Package tree
G{packagetree: global_load_data} 

Import Graph
G{importgraph: global_load_data} 
"""

LOAD_LEVEL_NORMAL = 0
LOAD_LEVEL_EXPAND = 1
LOAD_LEVEL_SHRINK = 2

class GlobalLoadData:

	def __init__(self,global_load_data_dict):
		print "[GlobalLoadData] init ..."
		self.global_load_data_dict = global_load_data_dict
		print "[GlobalLoadData] OK"

	def get_load_lower(self,name):
		return self.global_load_data_dict[name]['lower']

	def get_load_upper(self,name):
		return self.global_load_data_dict[name]['upper']

	def cal_load_level(self,name,load):
		upper = self.get_load_upper(name)
		lower = self.get_load_lower(name)
		if load < lower:
			return LOAD_LEVEL_SHRINK
		elif load > upper:
			return LOAD_LEVEL_EXPAND
		else:
			return LOAD_LEVEL_NORMAL

class GlobalLoadDataTesting(GlobalLoadData):
	pass
