"""
Class Hierarchy

G{classtree: ClusterMonitor} 

Package tree
G{packagetree: cluster_monitor} 

Import Graph
G{importgraph: cluster_monitor} 

"""
from monitor import *
from load_calculator import *

class ClusterMonitor:

	def __init__(self,controller_manager,global_load_data_dict):
		print "[ClusterMonitor] init ..."
		self.controller_manager = controller_manager
		#""" @type: L{ControllerManager} """

		self.load_calculator = LoadCalculator(global_load_data_dict)
		#""" @type: L{LoadCalculator} """

		self.apache_monitor = ApacheMonitor(self.controller_manager.get_apache_controller(),self.load_calculator)
		""" @type: L{ApacheMonitor} """
		self.mysql_monitor = MysqlMonitor(self.controller_manager.get_mysql_controller(),self.load_calculator)
		""" @type: L{MysqlMonitor} """
		self.robust_monitor = RobustMonitor(self.controller_manager.get_robust_controller(),self.load_calculator)
		""" @type: L{RobustMonitor} """

		print "[ClusterMonitor] OK"

	def get_apache_monitor(self):
		return self.apache_monitor

	def get_mysql_monitor(self):
		return self.mysql_monitor

	def get_robust_monitor(self):
		return self.robust_monitor

	def start(self):
		print "[ClusterMonitor] start ..."
		self.apache_monitor.start()
		self.mysql_monitor.start()
		self.robust_monitor.start()

	def stop(self):
		print "[ClusterMonitor] start ..."
		self.apache_monitor.stop()
		self.mysql_monitor.stop()
		self.robust_monitor.stop()

class ClusterMonitorTesting(ClusterMonitor):
	pass
