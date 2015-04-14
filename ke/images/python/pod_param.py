
class PodParam:

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
