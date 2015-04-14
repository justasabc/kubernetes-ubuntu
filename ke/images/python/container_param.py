
class ContainerParam:

	def __init__(self,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command,port_bindings,binds,links):
		self.detach = detach
		self.stdin_open = stdin_open
		self.tty = tty
		self.hostname = hostname
		self.name = name
		self.working_dir = working_dir
		self.cpu_shares = cpu_shares
		self.mem_limit = mem_limit
		self.ports = ports
		self.volumes = volumes
		self.environment = environment
		self.image = image
		self.command = command
		self.port_bindings = port_bindings
		self.binds = binds
		self.links = links

	def get_detach(self):
		return self.detach

	def get_stdin_open(self):
		return self.stdin_open

	def get_tty(self):
		return self.tty

	def get_hostname(self):
		return self.hostname

	def get_name(self):
		return self.name

	def get_working_dir(self):
		return self.working_dir

	def get_cpu_shares(self):
		return self.cpu_shares

	def get_mem_limit(self):
		return self.mem_limit

	def get_ports(self):
		return self.ports

	def get_volumes(self):
		return self.volumes

	def get_environment(self):
		return self.environment

	def get_image(self):
		return self.image

	def get_command(self):
		return self.command

	def get_port_bindings(self):
		return self.port_bindings

	def get_binds(self):
		return self.binds

	def get_links(self):
		return self.links

