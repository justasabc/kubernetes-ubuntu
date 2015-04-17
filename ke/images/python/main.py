"""
Class Hierarchy

G{classtree: Main} 

Package tree
G{packagetree: main} 

Import Graph
G{importgraph: main} 

"""
#/usr/bin/python
# -*- coding:utf-8 -*-

from cluster_server import ClusterServer

GLOBAL_REGION_DATA_DICT = {
	"huyu": {"sim_port":8801, "region_orig":(1000,1000), "region_start_port":9000, "wh":(2,2)},
	"xwd" : {"sim_port":8802, "region_orig":(1005,1000), "region_start_port":9050, "wh":(2,2)}
	}

GLOBAL_LOAD_DATA_DICT = {
	"apache": {"lower":0.1,"upper":0.4},
	"mysql": {"lower":0.2,"upper":0.5},
	"robust": {"lower":0.4,"upper":0.7}
}

class Main:

	def __init__(self,global_region_data_dict,global_load_data_dict):
		self.server = ClusterServer(global_region_data_dict,global_load_data_dict)
		""" @type: L{ClusterServer} """

	def run(self):
		print "="*80
		print "[Main] Server is starting..."
		print "="*80
		self.server.start()

class MainTesting(Main):
	pass

def main_entry():
	g_main = Main(GLOBAL_REGION_DATA_DICT,GLOBAL_LOAD_DATA_DICT)
	g_main.run()

if __name__=="__main__":
	main_entry()
