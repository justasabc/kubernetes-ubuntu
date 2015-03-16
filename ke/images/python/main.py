#/usr/bin/python
# -*- coding:utf-8 -*-

from setting import *
from region_pool import RegionPool
from cluster import Cluster

def test_cluster():
	region_pool = RegionPool(GLOBAL_REGION_DATA)
	region_pool.init_region_pool()

	cluster = Cluster("Virgeo OpenSimulator Cluster",region_pool)
	cluster.init_cluster()
	cluster.start()
	#cluster.stop()

def main():
	test_cluster()

if __name__=="__main__":
	main()
