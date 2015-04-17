"""
Class Hierarchy

G{classtree: ClusterManager} 

Package tree
G{packagetree: cluster_manager} 

Import Graph
G{importgraph: cluster_manager} 

"""
#/usr/bin/python
# -*- coding:utf-8 -*-
from pod_manager import *
from service_manager import *
from controller_manager import *
from execute_engine import *

class ClusterManager:

	def __init__(self,global_region_data_dict):
		print "[ClusterManager] init ..." 
		# service
		self.service_manager = ServiceManager()
		""" @type: L{ServiceManager} """

		# robust
		self.controller_manager = ControllerManager()
		""" @type: L{RobustController} """

		print "="*60
		# pod
		self.pod_manager = PodManager(global_region_data_dict)
		""" @type: L{PodManager} """
		print "="*60

		self.execute_engine = ExecuteEngine()
		""" @type: L{ExecuteEngine} """
		self.init_execute_engine()
		print "[ClusterManager] OK" 

	def init_execute_engine(self):
		print "[ClusterManager] init execute engine..."

		# 1) apache controller
		self.execute_engine.add_command(self.controller_manager.get_apache_controller())
		# 2) apache service
		self.execute_engine.add_command(self.service_manager.get_apache_service())
		# 3) mysql controller
		self.execute_engine.add_command(self.controller_manager.get_mysql_controller())
		# 4) mysql service
		self.execute_engine.add_command(self.service_manager.get_mysql_service())
		# 5) robust controller
		self.execute_engine.add_command(self.controller_manager.get_robust_controller())
		# 6) robust public service
		self.execute_engine.add_command(self.service_manager.get_robust_public_service())
		# 7) robust private service
		self.execute_engine.add_command(self.service_manager.get_robust_private_service())

		# 8) opensim pod
		self.execute_engine.add_command(self.pod_manager)

	def get_execute_engine(self):
		return self.execute_engine

	def get_service_manager(self):
		return self.service_manager

	def get_controller_manager(self):
		return self.controller_manager

	def get_pod_manager(self):
		return self.pod_manager

	def start(self):
		self.execute_engine.start()

	def stop(self):
		self.execute_engine.stop()

class ClusterManagerTesting(ClusterManager):
	pass
