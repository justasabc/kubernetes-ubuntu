#/usr/bin/python
# -*- coding:utf-8 -*-

from setting import *
from region_pool import RegionPool
from cluster import Cluster
from proxy import ProxyServer

def start_cluster():
	region_pool = RegionPool(GLOBAL_REGION_DATA)
	region_pool.init_region_pool()

	cluster = Cluster(region_pool)
	cluster.init_cluster()
	cluster.start()

def start_proxy():
	region_pool = RegionPool(GLOBAL_REGION_DATA)
	region_pool.init_region_pool()

	cluster = Cluster(region_pool)
	cluster.init_cluster()
	cluster.start()

	# start up proxy server
	simulator_list = cluster.get_simulator_list()
	proxy_server = ProxyServer(simulator_list)
	proxy_server.start()

def main():
	#start_cluster()
	start_proxy()

if __name__=="__main__":
	main()
