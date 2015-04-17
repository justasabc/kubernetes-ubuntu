"""
Class Hierarchy

G{classtree: ServiceManager} 

Package tree
G{packagetree: service_manager} 

Import Graph
G{importgraph: service_manager} 

"""

from service import *

class ServiceManager:

	def __init__(self):
		print "[ServiceManager] init ..." 
		self.apache_service = ApacheService()
		""" @type: L{ApacheService} """

		self.mysql_service = MysqlService()
		""" @type: L{MysqlService} """

		self.robust_public_service = RobustPublicService()
		""" @type: L{RobustPublicService} """

		self.robust_private_service = RobustPrivateService()
		""" @type: L{RobustPrivateService} """
		print "[ServiceManager] OK"

	def get_apache_service(self):
		return self.apache_service

	def get_mysql_service(self):
		return self.mysql_service

	def get_robust_public_service(self):
		return self.robust_public_service

	def get_robust_private_service(self):
		return self.robust_private_service

class ServiceManagerTesting(ServiceManager):
	pass
