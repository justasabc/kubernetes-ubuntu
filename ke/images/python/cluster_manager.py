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
from controller import *
from service import *
from pod import *
from pod_manager import *

class ClusterManager:

	def __init__(self,global_region_data_dict):
		print "[ClusterManager] init ..." 

		# apache
		self.apache_controller = ApacheController()
		""" @type: L{ApacheController} """
		self.apache_service = ApacheService()
		""" @type: L{ApacheService} """
		# mysql
		self.mysql_controller = MysqlController()
		""" @type: L{MysqlController} """
		self.mysql_service = MysqlService()
		""" @type: L{MysqlService} """
		# robust
		self.robust_controller = RobustController()
		""" @type: L{RobustController} """
		robust_service = RobustService()
		""" @type: L{RobustService} """
		print "="*60
		# opensim 
		self.opensim_pod_manager = OpensimPodManager(global_region_data_dict)
		""" @type: L{OpensimPodManager} """

		print "="*60
		print "[ClusterManager] OK" 

	def get_apache_controller(self):
		return self.apache_controller

	def get_apache_service(self):
		return self.apache_service

	def get_mysql_controller(self):
		return self.mysql_controller

	def get_mysql_service(self):
		return self.mysql_service

	def get_robust_controller(self):
		return self.robust_controller

	def get_robust_service(self):
		return self.robust_service

	def get_opensim_pod_manager(self):
		return self.opensim_pod_manager

	def start(self):
		# 1) apache 
		self.apache_controller.start()
		self.apache_service.start()

		# 2) mysql
		self.mysql_controller.start()
		self.mysql_service.start()

		# 3) robust
		self.robust_controller.start()
		self.robust_service.start()

		# 4) opensim
		self.opensim_pod_manager.start()

	def stop(self):
		# 4) opensim
		self.opensim_pod_manager.stop()

		# 3) robust
		self.robust_controller.stop()
		self.robust_service.stop()

		# 2) mysql
		self.mysql_controller.stop()
		self.mysql_service.stop()

		# 1) apache 
		self.apache_controller.stop()
		self.apache_service.stop()

class ClusterManagerTesting(ClusterManager):
	pass

