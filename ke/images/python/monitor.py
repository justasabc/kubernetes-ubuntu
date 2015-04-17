"""
Class Hierarchy

G{classtree: BaseMonitor} 

Package tree
G{packagetree: monitor} 

Import Graph
G{importgraph: monitor} 

"""
#/usr/bin/python
# -*- coding:utf-8 -*-
"""
# http://rancher.com/comparing-monitoring-options-for-docker-deployments/
 1) HTTP GET
echo -e "GET /containers/[CONTAINER_NAME]/stats HTTP/1.0\r\n" | nc -U /var/run/docker.sock
 2) docker stats
docker stats [CONTAINER_NAME]
"""

from stats import *
from threading import Thread,Timer,Event

LOAD_INTERVAL = 15*60
WEIGHT = (0.6,0.4)
CPU_WEIGHT = 0.6
MEM_WEIGHT = 0.4
CHECK_INTERVAL = 10

LOAD_LEVEL_NORMAL = 0
LOAD_LEVEL_EXPAND = 1
LOAD_LEVEL_SHRINK = 2

class BaseMonitor(Thread):

	def __init__(self,name,base_controller,load_calculator,check_interval=CHECK_INTERVAL):
        	Thread.__init__(self)
		self.stopped = Event()
		""" @type: L{Event} """

		self.name = name
		""" @type: C{string} """
		self.stats_list = []
		""" @type: L{Stats} """

		self.base_controller = base_controller
		""" @type: L{BaseController} """
		self.load_calculator = load_calculator
		""" @type: L{LoadCalculator} """

		self.check_interval =  check_interval
		""" @type: C{integer} """

	def start(self):
		Thread.start(self)

	def stop(self):
		self.stopped.set()

	def run(self):
        	while not self.stopped.wait(self.check_interval):
			self.check_load_level()

	def check_load_level(self):
		print "[BaseMonitor] {0} load level is OK...".format(self.name)
		return 
		# connect stats for name
		# cal load level
		self.stats_list = self.base_controller.get_tool().stats_container(self.name)
		load_level = self.load_calculator.cal_load_level(self.name,self.stats_list,LOAD_INTERVAL,CPU_WEIGHT,MEM_WEIGHT)
		if load_level == LOAD_LEVEL_EXPAND:
			self.expand()
		elif load_level == LOAD_LEVEL_SHRINK:
			self.shrink()

	def expand(self):
		old_replicas = self.base_controller.get_controller_param().get_replicas()
		new_replicas = old_replicas + 1
		self.base_controller.expand(new_replicas)

	def shrink(self):
		old_replicas = self.base_controller.get_controller_param().get_replicas()
		new_replicas = old_replicas - 1
		if new_replicas >= 1:
			self.base_controller.shrink(new_replicas)

class ApacheMonitor(BaseMonitor):
	
	def __init__(self,apache_controller,load_calculator):
		print "[ApacheMonitor] init ..." 
		BaseMonitor.__init__(self,'apache',apache_controller,load_calculator)
		print "[ApacheMonitor] OK" 

	def start(self):
		print "[ApacheMonitor] start ..." 
		BaseMonitor.start(self)

class MysqlMonitor(BaseMonitor):
	
	def __init__(self,mysql_controller,load_calculator):
		print "[MysqlMonitor] init ..." 
		BaseMonitor.__init__(self,'mysql',mysql_controller,load_calculator)
		print "[MysqlMonitor] OK" 

	def start(self):
		print "[MysqlMonitor] start ..." 
		BaseMonitor.start(self)

class RobustMonitor(BaseMonitor):
	
	def __init__(self,robust_controller,load_calculator):
		print "[RobustMonitor] init ..." 
		BaseMonitor.__init__(self,'robust',robust_controller,load_calculator) 
		print "[RobustMonitor] OK" 

	def start(self):
		print "[RobustMonitor] start ..." 
		BaseMonitor.start(self)

class MonitorTesting(ApacheMonitor,MysqlMonitor,RobustMonitor):
	pass
