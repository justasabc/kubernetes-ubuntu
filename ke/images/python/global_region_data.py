"""
Class Hierarchy

G{classtree: GlobalRegionData} 

Package tree
G{packagetree: global_region_data} 

Import Graph
G{importgraph: global_region_data} 

"""
class GlobalRegionData:

	def __init__(self,global_region_data_dict):
		print "[GlobalRegionData] init..."
		self.global_region_data_dict = global_region_data_dict
		print "[GlobalRegionData] OK."

	def get_region_group_list(self):
		return self.global_region_data_dict.keys()

	def get_sim_port(self,region_group):
		return self.global_region_data_dict[region_group]['sim_port']

	def get_region_orig(self,region_group):
		return self.global_region_data_dict[region_group]['region_orig']

	def get_region_start_port(self,region_group):
		return self.global_region_data_dict[region_group]['region_start_port']

	def get_region_width_height(self,region_group):
		return self.global_region_data_dict[region_group]['wh']

	def get_region_width(self,region_group):
		return self.global_region_data_dict[region_group]['wh'][0]

	def get_region_height(self,region_group):
		return self.global_region_data_dict[region_group]['wh'][1]

	def get_region_name_list(self,region_group):
		#REGION_NAME_HUYU=["huyu"+str(x)+str(y) for x in range(4) for y in range(7)]
		xmax = self.get_region_width(region_group)
		ymax = self.get_region_height(region_group)
		region_name_list = ["{0}{1}{2}".format(region_group,x,y) for x in range(xmax) for y in range(ymax)]
		return region_name_list

class GlobalRegionDataTesting(GlobalRegionData):
	pass
