#/usr/bin/python
# -*- coding:utf-8 -*-

from setting import *
from io import JsonGenerator
from commander import KubernetesCommander

class Pod:

	def __init__(self,pod_id,volumes,volume_mounts,name,image,command,cpu,memory,env,ports,labels):
		self.pod_id = pod_id
		self.volumes = volumes
		self.volume_mounts = volume_mounts
		self.name = name
		self.image = image
		self.command = command
		self.cpu = cpu
		self.memory = memory
		self.env = env
		self.ports = ports
		self.labels = labels

	def __to_dict(self,pod_id,volumes,volume_mounts,name,image,command,cpu,memory,env,ports,labels):
		d = {}
		d["id"] = pod_id
		d["kind"] = "Pod"
		d["apiVersion"] = "v1beta1"

		desiredState = {}
		manifest = {}
		manifest["version"] = "v1beta1"
		manifest["id"] = pod_id
		manifest["volumes"] = volumes

		containers = []
		c = {}
		c["name"] = name
		c["image"] = image
		c["command"] = command
		c["volumeMounts"] = volume_mounts
		c["cpu"] = cpu
		c["memory"] = memory
		c["env"] = env
		c["ports"] = ports
		containers.append(c)

		manifest["containers"] = containers
		desiredState["manifest"] = manifest
		d["desiredState"] = desiredState

		d["labels"] = labels
		
		return d

	def to_dict(self):
		return self.__to_dict(self.pod_id,self.volumes,self.volume_mounts,self.name,self.image,self.command,self.cpu,self.memory,self.env,self.ports,self.labels)

	def get_pod_id(self):
		return self.pod_id

	def get_volumes(self):
		return self.volumes

	def get_volume_mounts(self):
		return self.volume_mounts

	def get_name(self,name):
		return self.name

	def get_image(self,image):
		return self.image

	def get_command(self,command):
		return self.command

	def get_cpu(self,cpu):
		return self.cpu

	def get_memory(self,meory):
		return self.memory

	def get_env(self,env):
		return self.env

	def get_ports(self):
		return self.ports

	def get_labels(self):
		return self.labels

class Service:
	pass

class ReplicationController:
	pass

class OpensimPod(Pod):
	# a pod hosts N containers

	def __init__(self,simulator):
		self.simulator = simulator
		self.__init_setting(simulator)

	def __init_setting(self,simulator):
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
		cpu = CPU
		memory = MEMORY
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
		ports = []
		ports.append({"containerPort": sim_port, "hostPort": sim_port, "protocol": "TCP"})
		for region_port in region_port_list:
			ports.append({"containerPort": region_port, "hostPort": region_port, "protocol": "UDP"})
		labels =  {"name": "opensim-pod"}
		# init base
		Pod.__init__(self,pod_id,volumes,volume_mounts,name,image,command,cpu,memory,env,ports,labels)

		# fields
		self.dict_data = Pod.to_dict(self)
		self.file_path = "{0}{1}{2}".format(JSON_FOLDER,Pod.get_pod_id(self),".json")

		# generate json
		g = JsonGenerator("generator")
		g.generate(self.dict_data,self.file_path)

	def get_dict_data(self):
		return self.dict_data

	def get_json_file_path(self):
		return self.file_path

	def start(self):
		cmd = KubernetesCommander()
		cmd.create_pod(self.get_json_file_path())

	def status(self):
		cmd = KubernetesCommander()
		cmd.list_pods()

	def stop(self):
		cmd = KubernetesCommander()
		cmd.delete_pod(Pod.get_pod_id(self))

def test(): 
	pass

def main():
	test()

if __name__=="__main__":
	main()
