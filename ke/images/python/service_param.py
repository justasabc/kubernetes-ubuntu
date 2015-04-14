
class ServiceParam:

	def __init__(self,name,host_port,container_port,protocol,selector):
		self.name = name
		self.host_port = host_port
		self.container_port = container_port
		self.protocol = protocol
		self.selector = selector
