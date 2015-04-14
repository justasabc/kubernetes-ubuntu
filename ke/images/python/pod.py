"""
Class Hierarchy

G{classtree: BasePod} 

Package tree
G{packagetree: pod} 

Import Graph
G{importgraph: pod} 

"""
#/usr/bin/python
# -*- coding:utf-8 -*-
from cluster_tool import KubernetesTool
from pod_param import PodParam

OPENSIM_NAME='opensim'
OPENSIM_IMAGE="docker-registry:5000/ubuntu:opensim"
OPENSIM_COMMAND = ["/bin/bash", "/home/opensim80/bin/ke/start_opensim_xxx.sh"]
OPENSIM_CPU = 1024
OPENSIM_MEMORY = 1000000000

class BasePod:

	def __init__(self,pod_id,config_path):
		self.pod_id = pod_id
		""" @type: C{string} """
		self.config_path = config_path
		""" @type: C{string} """

		self.pod_param = None
		""" @type: L{PodParam} """
		self.tool = KubernetesTool()
		""" @type: L{KubernetesTool} """

	def get_pod_id(self):
		return self.pod_id

	def get_config_path(self):
		return self.config_path

	def get_pod_param(self):
		return self.pod_param

	def get_tool(self):
		return self.tool

	def start(self):
		self.tool.create_pod(self.config_path)

	def stop(self):
		self.tool.delete_pod(self.pod_id)

class ApachePod(BasePod):

	def __init__(self):
		self.create_pod_param()

	def create_pod_param(self):
		pod_id = 'apache-pod'
		config_path = 'json/apache-pod.json'
		BasePod.__init__(self,pod_id,config_path)

	def start(self):
		print "[ApachePod] start..."
		BasePod.start(self)

class MysqlPod(BasePod):

	def __init__(self):
		self.create_pod_param()

	def create_pod_param(self):
		pod_id = 'mysql-pod'
		config_path = 'json/mysql-pod.json'
		BasePod.__init__(self,pod_id,config_path)

	def start(self):
		print "[MysqlPod] start..."
		BasePod.start(self)

class RobustPod(BasePod):

	def __init__(self):
		self.create_pod_param()

	def create_pod_param(self):
		pod_id = 'robust-pod'
		config_path = 'json/robust-pod.json'
		BasePod.__init__(self,pod_id,config_path)

	def start(self):
		print "[RobustPod] start..."
		BasePod.start(self)

class OpensimPod(BasePod):

	def __init__(self,simulator):
		print "[OpensimPod] init ..."
		self.simulator = simulator
		""" @type: L{Simulator} """
		self.create_pod_param(simulator)
		print "[OpensimPod] OK"

	def create_pod_param(self,simulator):
		sim_name = simulator.get_simulator_name()
		sim_port = simulator.get_simulator_port()
		region_port_list = simulator.get_region_port_list()

		pod_id = sim_name
		volumes = [  
			{"name":"opensim-ke", "source":{"hostDir":{"path":"/volumes/opensim_resources/ke"}}},
			{"name":"opensim-config", "source":{"hostDir":{"path":"/volumes/opensim_resources/config-include"}}},
			{"name":"opensim-data", "source":{"hostDir":{"path":"/volumes/opensim_resources/opensim_data"}}}
		]  
		volume_mounts = [  
			{"name":"opensim-ke", "mountPath":"/home/opensim80/bin/ke", "readOnly":False},  
			{"name":"opensim-config", "mountPath":"/home/opensim80/bin/config-include", "readOnly":False},  
			{"name":"opensim-data", "mountPath":"/home/opensim80/bin/opensim_data", "readOnly":False}
		]
		name = OPENSIM_NAME
		image = OPENSIM_IMAGE
		command = OPENSIM_COMMAND
		cpu = OPENSIM_CPU
		memory = OPENSIM_MEMORY
		env = [
			{"name": "SIM_NAME","value": sim_name},
			{"name": "SIM_PORT","value": sim_port},
			{"name": "INI_MASTER","value": "/home/opensim80/bin/ke/grid/conf/OpenSimDefaults.ini"},
			{"name": "INI_FILE","value": "/home/opensim80/bin/ke/grid/conf/OpenSim.ini"},
			{"name": "LOG_CONFIG","value": "/home/opensim80/bin/ke/grid/conf/OpenSim.exe.config"},
			{"name": "PID_FILE","value": "/home/opensim80/bin/ke/grid/instances/{0}.pid".format(sim_name)},
			{"name": "LOG_FILE","value": "/home/opensim80/bin/ke/grid/instances/{0}.log".format(sim_name)}
		]
		
		ports = [
			{"containerPort": 8801, "hostPort": 8801, "protocol": "TCP"},
			{"containerPort": 9000, "hostPort": 9000, "protocol": "UDP"},
			{"containerPort": 9001, "hostPort": 9001, "protocol": "UDP"},
			{"containerPort": 9002, "hostPort": 9002, "protocol": "UDP"},
			{"containerPort": 9003, "hostPort": 9003, "protocol": "UDP"}
		]
		#ports = []
		#ports.append({"containerPort": sim_port, "hostPort": sim_port, "protocol": "TCP"})
		#for region_port in region_port_list:
		#	ports.append({"containerPort": region_port, "hostPort": region_port, "protocol": "UDP"})
		labels =  {"name": "opensim-pod"}

		# create params
		pod_param = PodParam(pod_id,volumes,volume_mounts,name,image,command,cpu,memory,env,ports,labels)
		dict_data = pod_param.to_dict()
		config_path = "json/"+pod_id+".json"

		# init BasePod
		BasePod.__init__(self,pod_id,config_path)
		self.tool.save_json_to_file(dict_data,config_path)

	def start(self):
		print "[OpensimPod] start..."
		BasePod.start(self)

class PodTesting(ApachePod,MysqlPod,RobustPod,OpensimPod):
	pass
