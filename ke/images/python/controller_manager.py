"""
Class Hierarchy

G{classtree: ControllerManager} 

Package tree
G{packagetree: controller_manager} 

Import Graph
G{importgraph: controller_manager} 

"""

from controller import *

class ControllerManager:

	def __init__(self):
		print "[ControllerManager] init ..." 
		self.apache_controller = ApacheController()
		""" @type: L{ApacheController} """

		self.mysql_controller = MysqlController()
		""" @type: L{MysqlController} """

		self.robust_controller = RobustController()
		""" @type: L{RobustController} """
		print "[ControllerManager] OK"

	def get_apache_controller(self):
		return self.apache_controller

	def get_mysql_controller(self):
		return self.mysql_controller

	def get_robust_controller(self):
		return self.robust_controller

class ControllerManagerTesting(ControllerManager):
	pass
