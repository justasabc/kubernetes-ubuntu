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
	"huyu": {"sim_port":8801, "region_orig":(1000,1000), "region_start_port":9000, "wh":(3,3)},
	"xwd" : {"sim_port":8802, "region_orig":(1005,1000), "region_start_port":9050, "wh":(3,3)}
	}


class Main:

	def __init__(self,global_region_data_dict):
		self.server = ClusterServer(global_region_data_dict)
		""" @type: L{ClusterServer} """

	def run(self):
		self.server.start()

class MainTesting(Main):
	pass

def main_entry():
	g_main = Main(GLOBAL_REGION_DATA_DICT)
	#start_proxy()

if __name__=="__main__":
	main_entry()
