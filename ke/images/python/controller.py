"""
Class Hierarchy

G{classtree: BaseController} 

Package tree
G{packagetree: controller} 

Import Graph
G{importgraph: controller} 

"""
from cluster_tool import KubernetesTool
from controller_param import ControllerParam 

class BaseController:

	def __init__(self,controller_id,config_path):
		self.controller_id = controller_id
		""" @type: C{string} """
		self.config_path = config_path
		""" @type: C{string} """

		self.controller_param = None
		""" @type: L{ControllerParam} """
		self.tool = KubernetesTool()
		""" @type: L{KubernetesTool} """

	def get_controller_id(self):
		return self.controller_id

	def get_config_path(self):
		return self.config_path

	def get_controller_param(self):
		return self.controller_param

	def get_tool(self):
		return self.tool

	def start(self):
		self.tool.create_controller(self.config_path)

	def stop(self):
		self.tool.delete_controller(self.controller_id)

class ApacheController(BaseController):

	def __init__(self):
		print "[ApacheController] init ..."
		self.create_controller_param()
		print "[ApacheController] OK"

	def create_controller_param(self):
		controller_id = 'apache-controller'
		config_path = 'json/apache-controller.json'
		BaseController.__init__(self,controller_id,config_path)

	def start(self):
		print "[ApacheController] start..."
		BaseController.start(self)

class MysqlController(BaseController):

	def __init__(self):
		print "[MysqlController] init ..."
		self.create_controller_param()
		print "[MysqlController] OK"

	def create_controller_param(self):
		controller_id = 'mysql-controller'
		config_path = 'json/mysql-controller.json'
		BaseController.__init__(self,controller_id,config_path)

	def start(self):
		print "[MysqlController] start..."
		BaseController.start(self)

class RobustController(BaseController):

	def __init__(self):
		print "[RobustController] init ..."
		self.create_controller_param()
		print "[RobustController] OK"

	def create_controller_param(self):
		controller_id = 'robust-controller'
		config_path = 'json/robust-controller.json'
		BaseController.__init__(self,controller_id,config_path)

	def start(self):
		print "[RobustController] start..."
		BaseController.start(self)

class ControllerTesting(ApacheController,MysqlController,RobustController):
	pass
