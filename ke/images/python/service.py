"""
Class Hierarchy

G{classtree: BaseService} 

Package tree
G{packagetree: service} 

Import Graph
G{importgraph: service} 

"""

from cluster_tool import KubernetesTool
from service_param import ServiceParam

class BaseService:

	def __init__(self,service_id,config_path):
		self.service_id = service_id
		""" @type: C{string} """
		self.config_path = config_path
		""" @type: C{string} """

		self.service_param = None
		""" @type: L{ServiceParam} """
		self.tool = KubernetesTool()
		""" @type: L{KubernetesTool} """

	def get_service_id(self):
		return self.service_id

	def get_config_path(self):
		return self.config_path

	def get_service_param(self):
		return self.service_param

	def get_tool(self):
		return self.tool

	def start(self):
		self.tool.create_service(self.config_path)

	def stop(self):
		self.tool.delete_service(self.service_id)

class ApacheService(BaseService):

	def __init__(self):
		print "[ApacheService] init ..."
		self.create_service_param()
		print "[ApacheService] OK"

	def create_service_param(self):
		service_id = 'apache-service'
		config_path = 'json/apache-service.json'
		BaseService.__init__(self,service_id,config_path)

	def start(self):
		print "[ApacheService] start..."
		BaseService.start(self)

class MysqlService(BaseService):

	def __init__(self):
		print "[MysqlService] init ..."
		self.create_service_param()
		print "[MysqlService] OK"

	def create_service_param(self):
		service_id = 'mysql-service'
		config_path = 'json/mysql-service.json'
		BaseService.__init__(self,service_id,config_path)

	def start(self):
		print "[MysqlService] start..."
		BaseService.start(self)

class RobustPublicService(BaseService):

	def __init__(self):
		print "[RobustPublicService] init ..."
		self.create_service_param()
		print "[RobustPublicService] OK"

	def create_service_param(self):
		service_id = 'robust-public-service'
		config_path = 'json/robust-public-service.json'
		BaseService.__init__(self,service_id,config_path)

	def start(self):
		print "[RobustPublicService] start..."
		BaseService.start(self)

class RobustPrivateService(BaseService):

	def __init__(self):
		print "[RobustPrivateService] init ..."
		self.create_service_param()
		print "[RobustPrivateService] OK"

	def create_service_param(self):
		service_id = 'robust-internal-service'
		config_path = 'json/robust-internal-service.json'
		BaseService.__init__(self,service_id,config_path)

	def start(self):
		print "[RobustPrivateService] start..."
		BaseService.start(self)

class ServiceTesting(ApacheService,MysqlService,RobustPublicService,RobustPrivateService):
	pass
