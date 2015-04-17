"""
Class Hierarchy

G{classtree: LoadCalculator} 

Package tree
G{packagetree: load_calculator} 

Import Graph
G{importgraph: load_calculator} 

"""
from global_load_data import *

class LoadCalculator:

	def __init__(self,global_load_data_dict):
		print "[LoadCalculator] init ..."
		self.global_load_data = GlobalLoadData(global_load_data_dict)
		""" @type: L{GlobalLoadData} """
		print "[LoadCalculator] OK"

	def cal_cpu_load(self,stats_list,load_interval):
		count = len(stats_list)
		index = 0
		if count>load_interval:
			index = count - load_interval
		total_load = 0
		index = count-load_interval
		while index < count:
			stats = stats_list[index]
			total_load = total_load + stats.get_cpu_percentage()
			index = index + 1
		load = total_load / load_interval
		return load

	def cal_mem_load(self,stats_list,load_interval):
		count = len(stats_list)
		index = 0
		if count>load_interval:
			index = count - load_interval
		total_load = 0
		index = count-load_interval
		while index < count:
			stats = stats_list[index]
			total_load = total_load + stats.get_memory_percentage()
			index = index + 1
		load = total_load / load_interval
		return load

	def cal_weighted_load(self,cpu_load,mem_load,cpu_weight,mem_weight):
		return cpu_weight*cpu_load + mem_weight*mem_load

	def cal_load_level(self,name,weighted_load):
		return self.global_load_data.cal_load_level(name,weighted_load)

	def cal_load_level(self,name,stats_list,load_interval,cpu_weight,mem_weight):
		cpu_load = self.cal_cpu_load(stats_list,load_interval)
		mem_load = self.cal_mem_load(stats_list,load_interval)
		weighted_load = self.cal_weighted_load(cpu_load,mem_load,cpu_weight,mem_weight)
		load_level = self.cal_load_level(name,weighted_load)
		return load_level

class LoadCalculatorTesting(LoadCalculator):
	pass
