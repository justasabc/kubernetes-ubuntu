
"""
Class Hierarchy

G{classtree: ContainerClient} 

Import Graph
G{importgraph: container_client} 

"""

#/usr/bin/python
# -*- coding:utf-8 -*-

from docker import Client
from image_client import ImageClient
from container_param import ContainerParam

# docker related
APACHE_CONTAINER_NAME='apache'
MYSQL_CONTAINER_NAME='mysql'
ROBUST_CONTAINER_NAME='robust'
OPENSIM_CONTAINER_NAME='opensim'

APACHE_BASE_IMAGE='ubuntu:apache'
MYSQL_BASE_IMAGE='ubuntu:mysql'
ROBUST_BASE_IMAGE='ubuntu:robust'
OPENSIM_BASE_IMAGE='ubuntu:opensim'

CPU_SHARES=1
MEM_LIMIT='1g'
APACHE_LINKS = {}
MYSQL_LINKS = {}
ROBUST_LINKS = {'mysql':'vgeomysql'}
OPENSIM_LINKS = {'mysql':'vgeomysql','robust':'vgeorobust'}

APACHE_COMMAND = '/bin/bash ./start_apache.sh'
MYSQL_COMMAND = '/bin/bash ./start_mysql.sh'
ROBUST_COMMAND = '/bin/bash ./start_robust.sh'
OPENSIM_COMMAND = '/bin/bash ./start_opensim_xxx.sh'

# container status
CS_Running = 'running'
#CS_Paused = 'paused'
CS_Stopped = 'stopped'
#CS_Crashed = 'crashed'
CS_NonExist = 'nonexist'
CS_Unknown = 'unknown'

#cmd=UtilityCommander()
#HOST_IP = cmd.get_host_ip()
#MYSQL_IP = cmd.get_container_ip('mysql')
#DOCKER_SERVER_URL = 'unix://var/run/docker.sock'
DOCKER_SERVER_URL = 'tcp://master:2375'

class ContainerClient:
	"""
	Container client class
	"""

	def __init__(self,base_url):
		self.client = Client(base_url)
		""" @type: L{docker.Client} """
		self.image_client = ImageClient(base_url)
		""" @type: L{ImageClient} """

	def info(self):
		return self.client.info()

	def version(self):
		return self.client.version()

	#==============================================================================
	# docker create/start/stop/restart/attach/pause/unpause/logs
	#==============================================================================
	def create_container(self,container_param):
		detach = container_param.detach
		stdin_open = container_param.stdin_open
		tty = container_param.tty
		hostname = container_param.hostname
		name = container_param.name
		working_dir = container_param.working_dir
		cpu_shares = container_param.cpu_shares
		mem_limit = container_param.mem_limit
		ports = container_param.ports
		volumes = container_param.volumes
		environment = container_param.environment
		image = container_param.image
		command = container_param.command

		# create container
		container = self.client.create_container(detach=detach,stdin_open=stdin_open,tty=tty,hostname=hostname,name=name,working_dir=working_dir,cpu_shares=cpu_shares,mem_limit=mem_limit,ports=ports,volumes=volumes,environment=environment,image=image,command=command)
		return container

	def start_container(self,container_param):
		container = container_param.name
		port_bindings = container_param.port_bindings
		binds = container_param.binds
		links = container_param.links

		return self.client.start(container=container,port_bindings=port_bindings,binds=binds,links=links)

	def stop_container(self,container):
		return self.client.stop(container)

	def restart_container(self,container):
		return self.client.restart(container)

	def attach_container(self,container):
		return self.client.attach(container)

	def pause_container(self,container):
		return self.client.pasue(container)

	def unpause_container(self,container):
		return self.client.unpause(container)

	def logs_container(self,container):
		return self.client.logs(container)

	def execute_container(self,container,cmd):
		return self.client.execute(container,cmd,detach=False,tty=True)

	def remove_container(self,container):
		return self.client.remove_container(container)

	def list_all_containers(self):
		return self.client.containers(all=True)

	def list_running_containers(self):
		return self.client.containers(all=False)

	#==============================================================================
	# docker get container status
	#==============================================================================
	def get_container_status(self,container):
		for c in self.client.containers(all=True):
			names_list = c['Names']
			name = "/"+container
			exist = name in names_list
			if exist:
				status = c['Status']
				if status[:2]=='Up':
					return CS_Running
				else:
					return CS_Stopped
				#elif status[:10]=='Exited (0)':
					#return CS_Stopped
				#else:
				#	return CS_Crashed
		return CS_NonExist

	#==============================================================================
	# docker get container id
	#==============================================================================
	def get_container_id(self,container):
		for c in self.client.containers(all=True):
			names_list = c['Names']
			name = "/"+container
			exist = name in names_list
			if exist:
				return c['Id']
		return None

	def inspect_container(self,container):
		return self.client.inspect_container(container)

	def diff_container(self,container):
		return self.client.diff(container)

	def copy_from_container(self,container,filepath):
		return self.client.copy(container=container,resource=filepath)

	def port_container(self,container,private_port):
		return self.client.port(container=container,private_port=private_port)

	def top_container(self,container):
		return self.client.top(container)

	def stats_controller(self,container):
		return self.client.stats(container)

class BaseContainer(ContainerClient):
	"""
	base container
	"""

	def __init__(self,docker_base_url,container_param):
		ContainerClient.__init__(self,docker_base_url)
		self.container_param = container_param
      		""" @type: L{ContainerParam}"""

	#==============================================================================
	# basic getter
	#==============================================================================
	def get_docker_base_url(self):
		return self.docker_base_url

	def get_container_param(self):
		return self.container_param

	#==============================================================================
	# useful functions
	#==============================================================================
	def get_status(self):
		return ContainerClient.get_container_status(self,self.container_param.name)

	def get_id(self):
		return ContainerClient.get_container_id(self,self.container_param.name)

	#==============================================================================
	# start/stop/restart
	#==============================================================================
	def start(self):
		# if not exist,then create it and start it
		status = self.get_status()
		if status == CS_NonExist:
			print "[BaseContainer] container {0} does't exist, so create it first...".format(self.name)
			ContainerClient.create_container(self,self.container_param)
			ContainerClient.start_container(self,self.container_param)
		elif status == CS_Running:
			print "[BaseContainer] container {0} has already been started!".format(self.name)
		elif status == CS_Stopped:
			ContainerClient.start_container(self,self.container_param)

	def stop(self):
		status = self.get_status()
		if status == CS_Running:
			ContainerClient.stop_container(self,self.container_param.name)
		elif status == CS_Stopped:
			print "[BaseContainer] container {0} has already been stopped!".format(self.name)

	def restart(self):
		status = self.get_status()
		if status == CS_Running:
			ContainerClient.stop_container(self,self.container_param.name)
			ContainerClient.start_container(self,self.container_param)
		elif status == CS_Stopped:
			print "[BaseContainer] container {0} has already been stopped! Start it first!".format(self.name)
		

class ApacheContainer(BaseContainer):

	def __init__(self,docker_base_url):
		container_param = self.create_apache_container_param()
		BaseContainer.__init__(self,docker_base_url,container_param)

	def create_apache_container_param(self):
		pass

class MysqlContainer(BaseContainer):

	def __init__(self,docker_base_url):
		container_param = self.create_mysql_container_param()
		BaseContainer.__init__(self,docker_base_url,container_param)

	def create_mysql_container_param(self):
		pass

class VgeoContainer(BaseContainer):

	def __init__(self,docker_base_url,container_param):
		BaseContainer.__init__(self,docker_base_url,container_param)

class RobustContainer(VgeoContainer):

	def __init__(self,docker_base_url):
		container_param = self.create_robust_container_param()
		VgeoContainer.__init__(self,docker_base_url,container_param)

	def create_robust_container_param(self):
		pass

class OpensimContainer(VgeoContainer):

	def __init__(self,docker_base_url):
		container_param = self.create_opensim_container_param()
		VgeoContainer.__init__(self,docker_base_url,container_param)

	def create_opensim_container_param(self):
		pass

class ContainerTesting(ApacheContainer,MysqlContainer,RobustContainer,OpensimContainer):
	pass

def test_docker_client():
	client = ContainerClient(DOCKER_SERVER_URL)
	print client.get_container_status('apache')
	print client.get_container_status('mysql')
	print client.get_container_status('robust')
	print client.get_container_status('huyu')
	print client.get_container_status('xwd')
	print client.get_container_status('mycontainer')
	print client.get_container_status('xxx')

def format_percentage(a,b):
	return "{0:.2f}%".format(float(a)/b * 100)

def test_stats():
	client = DockerClient(DOCKER_SERVER_URL)
	stats_obj = client.stats_controller("docker-registry")
	counter = 0
	for stat in stats_obj:
		d = json.loads(stat)
		total_usage = d['cpu_stats']['cpu_usage']['total_usage']
		usage_in_usermode = d['cpu_stats']['cpu_usage']['usage_in_usermode']
		usage_in_kernelmode = d['cpu_stats']['cpu_usage']['usage_in_kernelmode']

		system_cpu_usage = d['cpu_stats']['system_cpu_usage']
		#cpu_percentage = format_percentage(total_usage,system_cpu_usage)
		cpu_percentage = format_percentage(u,system_cpu_usage)

		memory_usage = d['memory_stats']['usage']
		memory_limit = d['memory_stats']['limit']
		memory_percentage = format_percentage(memory_usage,memory_limit)
		network_rx = d['network']['rx_bytes']
		network_tx = d['network']['tx_bytes']
		print cpu_percentage,memory_percentage
		counter += 1
		if counter>=100:
			break
	print "="*110

def main():
	#test_apache()
	#test_mysql()
	#test_robust()
	#test_docker_client()
	test_stats()

if __name__=="__main__":
	main()
