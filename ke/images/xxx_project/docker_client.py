#/usr/bin/python
# -*- coding:utf-8 -*-

# https://docs.docker.com/articles/basics/
# https://github.com/docker/docker-py
# https://pypi.python.org/packages/source/d/docker-py/
# http://docker-py.readthedocs.org/en/latest/

#===================================
# create 4 default users
# create user [first] [last] [passw] [RegionX] [RegionY] [Email]
# import oar/iar data
# command-script ./opensim_data/oar/script/load_oar_huyu.txt
# command-script ./opensim_data/oar/script/load_oar_xwd.txt

# command-script ./opensim_data/iar/script/load_iar.txt
# command-script ./opensim_data/test_user/load_iar.txt

#  docker exec -i -t robust ls /home/opensim80/bin/opensim_data/maptiles
#  ????????????
#===================================

import subprocess
import os
from docker import Client

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

def execute_external_command(command_str):
	p = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	value = ""
	for line in p.stdout.readlines():
		value = line.rstrip()
	return_code = p.wait()
	return value

def get_host_ip():
	command_str = "/sbin/ifconfig $ETH0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
	return execute_external_command(command_str)

def get_container_ip(container_name):
	command_str = "docker inspect -f '{{ .NetworkSettings.IPAddress }}' {0}".format(container_name)
	return execute_external_command(command_str)

HOST_IP = get_host_ip()
MYSQL_IP = get_container_ip('mysql')
DOCKER_SERVER_URL = 'unix://var/run/docker.sock'

class DockerClient:
	"""
	docker client for runing robust and opensim containers
	"""

	def __init__(self,base_url):
		self.client = Client(base_url)

	def info(self):
		return self.client.info()

	def version(self):
		return self.client.version()

	#==============================================================================
	# docker create/start/stop/restart/attach/pause/unpause/logs
	#==============================================================================
	def create_container(self,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command):
		container = self.client.create_container(detach=detach,stdin_open=stdin_open,tty=tty,hostname=hostname,name=name,working_dir=working_dir,cpu_shares=cpu_shares,mem_limit=mem_limit,ports=ports,volumes=volumes,environment=environment,image=image,command=command)
		return container

	def start_container(self,container,port_bindings,binds,links):
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

	#==============================================================================
	# docker execute command in container
	#==============================================================================
	def execute_container(self,container,cmd):
		return self.client.execute(container,cmd,detach=False,tty=True)

	#==============================================================================
	# docker remove container/image
	#==============================================================================
	def remove_container(self,container):
		return self.client.remove_container(container)

	def remove_image(self,image):
		return self.client.remove_image(image)

	#==============================================================================
	# docker list container/image
	#==============================================================================
	def list_all_containers(self):
		return self.client.containers(all=True)

	def list_running_containers(self):
		return self.client.containers(all=False)

	def list_images(self):
		return self.client.images()

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

	#==============================================================================
	# docker inspect container/image
	#==============================================================================
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

	def inspect_image(self,image):
		return self.client.inspect_image(image)

	def history_image(self,image):
		return self.client.history(image)

	#==============================================================================
	# docker commit/tag/build image
	#==============================================================================
	def commit_image(self,container,repository,tag,message,author):
		return self.client.commit(container=container,repository=repository,tag=tag,message=message,author=author)

	def tag_image(self,image,repository,tag):
		return self.client.tag(image=image,repository=repository,tag=tag)

	def build_image(self,dockerfile_folder,tag,rm):
		return self.client.build(path=dockerfile_folder,tag=tag,rm=rm)


class BaseContainer:

	def __init__(self,docker_base_url,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command,port_bindings,binds,links):
		# create docker client instance
		self.__docker_client_instance = DockerClient(docker_base_url)

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

	#==============================================================================
	# basic getter
	#==============================================================================
	def get_docker_base_url(self):
		return self.docker_base_url

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

	#==============================================================================
	# useful functions
	#==============================================================================
	def get_status(self):
		return self.__docker_client_instance.get_container_status(self.name)

	def get_id(self):
		return self.__docker_client_instance.get_container_id(self.name)

	def __create(self):
		print "[BaseContainer] creating container {0} ...".format(self.name)
		self.__docker_client_instance.create_container(detach=self.detach,stdin_open=self.stdin_open,tty=self.tty,hostname=self.hostname,name=self.name,working_dir=self.working_dir,cpu_shares=self.cpu_shares,mem_limit=self.mem_limit,ports=self.ports,volumes=self.volumes,environment=self.environment,image=self.image,command=self.command)

	def __start(self):
		print "[BaseContainer] starting container {0} ...".format(self.name)
		self.__docker_client_instance.start_container(container=self.name,port_bindings=self.port_bindings,binds=self.binds,links=self.links)
	def __stop(self):
		print "[BaseContainer] stopping container {0} ...".format(self.name)
		self.__docker_client_instance.stop_container(container=self.name)

	def start(self):
		# if not exist,then create it and start it
		status = self.get_status()
		if status == CS_NonExist:
			print "[BaseContainer] container {0} does't exist, so create it first...".format(self.name)
			self.__create()
			self.__start()
		elif status == CS_Running:
			print "[BaseContainer] container {0} has already been started!".format(self.name)
		elif status == CS_Stopped:
			self.__start()

	def stop(self):
		status = self.get_status()
		if status == CS_Running:
			self.__stop()
		elif status == CS_Stopped:
			print "[BaseContainer] container {0} has already been stopped!".format(self.name)

	def restart(self):
		status = self.get_status()
		if status == CS_Running:
			self.__stop()
			self.__start()
		elif status == CS_Stopped:
			print "[BaseContainer] container {0} has already been stopped! Start it first!".format(self.name)
		

class ApacheContainer(BaseContainer):

	def __init__(self,docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_container_name):
		self.init_apache_settings(docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_container_name)

	def init_apache_settings(self,docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_container_name):
		# set paths
		e_current_folder=os.getcwd()
		e_host_folder=e_current_folder+"/../../../apache/var/www"
		e_container_folder="/var/www"
		e_container_workdir="/home"

		# params for create/start container 
		detach = True
		stdin_open = True
		tty = False
		hostname = e_container_name
		name = e_container_name
		working_dir = e_container_workdir

		# port mapping
		ports = [(880,'tcp')] 
		port_bindings = {'880/tcp':(e_host_ip,880)}
		print ports
		print port_bindings

		# volume mapping
		volumes = [e_container_folder]
		binds = {e_host_folder:{'bind':e_container_folder,'ro':False}}

		# environment (list or dict)
		environment = {}

		# init base
		BaseContainer.__init__(self,docker_base_url,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command,port_bindings,binds,links)

class MysqlContainer(BaseContainer):

	def __init__(self,docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_container_name):
		self.init_mysql_settings(docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_container_name)

	def init_mysql_settings(self,docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_container_name):
		# set paths
		e_container_workdir="/home"

		# params for create/start container 
		detach = True
		stdin_open = False
		tty = False
		hostname = e_container_name
		name = e_container_name
		working_dir = e_container_workdir

		# port mapping
		ports = [(3306,'tcp')] 
		port_bindings = {'3306/tcp':(e_host_ip,33061)}
		print ports
		print port_bindings

		# volume mapping
		volumes = []
		binds = {}

		# environment (list or dict)
		environment = {}

		# init base
		BaseContainer.__init__(self,docker_base_url,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command,port_bindings,binds,links)

class VgeoContainer(BaseContainer):

	def __init__(self,docker_base_url,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command,port_bindings,binds,links,e_pid_file,e_log_file):
		self.pid_file = e_pid_file
		self.log_file = e_log_file
		BaseContainer.__init__(self,docker_base_url,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command,port_bindings,binds,links)

	def get_pid_file():
		return self.pid_file

	def get_log_file():
		return self.log_file

	def __remove_file(self,filepath):
		if os.path.exists(filepath):
			print "[VgeoContainer] removing {0}".format(filepath)

	def start(self):
		# remove pid/log file 
		self.__remove_file(self.pid_file)
		self.__remove_file(self.log_file)

		print "[VgeoContainer] start..."
		BaseContainer.start(self)

	def stop(self):
		print "[VgeoContainer] stop..."
		BaseContainer.stop(self)

		# remove pid/log file 
		self.__remove_file(self.pid_file)
		self.__remove_file(self.log_file)

	def restart(self):
		print "[VgeoContainer] restart..."
		BaseContainer.restart(self)

class RobustContainer(VgeoContainer):

	def __init__(self,docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_service_name):
		self.init_robust_settings(docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_service_name)

	def init_robust_settings(self,docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_service_name):
		# set paths
		# ke
		e_current_folder=os.getcwd()+"/resources/"
		e_host_folder=e_current_folder+"/ke"
		e_container_bin_folder="/home/opensim80/bin"
		e_container_folder=e_container_bin_folder+"/ke"
		e_container_workdir=e_container_bin_folder+"/ke"
		e_ini_file=e_container_folder+"/grid/conf/Robust.ini"
		e_log_config=e_container_folder+"/grid/conf/Robust.exe.config"
		e_pid_file=e_container_folder+"/grid/services/"+e_service_name+".pid"
		e_log_file=e_container_folder+"/grid/services/"+e_service_name+".log"
		pid_file=e_host_folder+"/grid/services/"+e_service_name+".pid"
		log_file=e_host_folder+"/grid/services/"+e_service_name+".log"

		# params for create/start container 
		detach = False
		stdin_open = True
		tty = True
		hostname = e_service_name
		name = e_service_name
		working_dir = e_container_workdir

		# port mapping
		ports,port_bindings = self.__get_robust_port_mapping(e_host_ip,[8002,8003],'tcp')
		print ports
		print port_bindings

		# volume mapping
		volumes = [e_container_folder]
		binds = {e_host_folder:{'bind':e_container_folder,'ro':False}}

		# environment (list or dict)
		environment = {'SERVICE_NAME':e_service_name,'INI_FILE':e_ini_file,'LOG_CONFIG':e_log_config,'PID_FILE':e_pid_file,'LOG_FILE':e_log_file,'HOST_IP':e_host_ip}
		# init vgeo (pid_file log_file)
		VgeoContainer.__init__(self,docker_base_url,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command,port_bindings,binds,links,pid_file,log_file)

	#==============================================================================
	# get port mapping for robust
	#==============================================================================
	def __get_robust_port_mapping(self,host_ip,service_port_list,service_port_protocol):
		# input: 
		#  >>> 192.168.1.2, [8002,8003], tcp
		# output: 
		# >>>  e_ports = [(8002,'tcp'),(8003,'tcp')]
		# >>>  e_port_bindings = {'8002/tcp':('192.168.1.2',8002),'8003/tcp':('192.168.1.2',8003)}
		e_ports = []
		e_port_bindings = {}
		# service port
		for port in service_port_list:
			pair = (port,service_port_protocol)
			e_ports.append(pair)
			key = "{0}/{1}".format(port,service_port_protocol)
			value = (host_ip,port)
			e_port_bindings[key] = value
		return e_ports,e_port_bindings

class OpensimContainer(VgeoContainer):

	def __init__(self,docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_sim_name,e_sim_port,e_region_port_list,e_regionload_web_url):
		self.init_opensim_settings(docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_sim_name,e_sim_port,e_region_port_list,e_regionload_web_url)

	def init_opensim_settings(self,docker_base_url,image,cpu_shares,mem_limit,links,command,e_host_ip,e_sim_name,e_sim_port,e_region_port_list,e_regionload_web_url):
		# set paths
		# ke
		e_current_folder=os.getcwd()+"/resources/"
		e_host_folder=e_current_folder+"/ke"
		e_container_bin_folder="/home/opensim80/bin"
		e_container_folder=e_container_bin_folder+"/ke"
		e_container_workdir=e_container_bin_folder+"/ke"
		# config-include
		e_host_config_include = e_current_folder+"/config-include"
		e_container_config_include = e_container_bin_folder+"/config-include"
		# opensim_data (oar,iar,scripts)
		e_host_opensim_data = e_current_folder+"/opensim_data"
		e_container_opensim_data = e_container_bin_folder+"/opensim_data"
		# maptiles 
		e_host_maptiles = e_current_folder+"/opensim_data/maptiles"
		e_container_maptiles = e_container_bin_folder+"/opensim_data/maptiles"

		e_ini_master=e_container_folder+"/grid/conf/OpenSimDefaults.ini"
		e_ini_file=e_container_folder+"/grid/conf/OpenSim.ini"
		e_log_config=e_container_folder+"/grid/conf/OpenSim.exe.config"
		e_pid_file=e_container_folder+"/grid/instances/"+e_sim_name+".pid"
		e_log_file=e_container_folder+"/grid/instances/"+e_sim_name+".log"
		pid_file=e_host_folder+"/grid/instances/"+e_sim_name+".pid"
		log_file=e_host_folder+"/grid/instances/"+e_sim_name+".log"

		# params for create/start container 
		detach = False
		stdin_open = True
		tty = True
		hostname = e_sim_name
		name = e_sim_name
		working_dir = e_container_workdir

		# port mapping
		# sim_port(tcp) + region_port_list (udp)
		ports,port_bindings = self.__get_opensim_port_mapping(e_host_ip,e_sim_port,'tcp',e_region_port_list,'udp')
		print ports
		print port_bindings

		# volume mapping
		volumes = [e_container_folder,e_container_config_include,e_container_opensim_data,e_container_maptiles]
		binds = {e_host_folder:{'bind':e_container_folder,'ro':False}, e_host_config_include:{'bind':e_container_config_include,'ro':False}, e_host_opensim_data:{'bind':e_container_opensim_data,'ro':False},e_host_maptiles:{'bind':e_container_maptiles,'ro':False}}
		# environment (list or dict)
		environment = {'SIM_NAME':e_sim_name,'SIM_PORT':e_sim_port,'INI_MASTER':e_ini_master,'INI_FILE':e_ini_file,'LOG_CONFIG':e_log_config,'PID_FILE':e_pid_file,'LOG_FILE':e_log_file,'REGIONLOAD_WEB_URL':e_regionload_web_url}

		# init vgeo (pid_file log_file)
		VgeoContainer.__init__(self,docker_base_url,detach,stdin_open,tty,hostname,name,working_dir,cpu_shares,mem_limit,ports,volumes,environment,image,command,port_bindings,binds,links,pid_file,log_file)

	#==============================================================================
	# get port mapping for opensim
	#==============================================================================
	def __get_opensim_port_mapping(self,host_ip,sim_port,sim_port_protocol,region_port_list,region_port_protocol):
		# input: 
		#  >>> 192.168.1.2, 9000,tcp, [9001,9002],udp
		# output: 
		# >>>  e_ports = [(9000,'tcp'),(9001,'udp'),(9002,'udp')]
		# >>>  e_port_bindings = {'9000/tcp':('192.168.1.2',8002),'9001/udp':('192.168.1.2',9001),'9002/udp':('192.168.1.2',9002)}
		e_ports = []
		e_port_bindings = {}
		# sim port
		sim_pair = (sim_port,sim_port_protocol)
		e_ports.append(sim_pair)
		key = "{0}/{1}".format(sim_port,sim_port_protocol)
		value = (host_ip,sim_port)
		e_port_bindings[key] = value
		# region port
		for port in region_port_list:
			pair = (port,region_port_protocol)
			e_ports.append(pair)
			key = "{0}/{1}".format(port,region_port_protocol)
			value = (host_ip,port)
			e_port_bindings[key] = value
		return e_ports,e_port_bindings

def test_apache():
	apache = ApacheContainer(DOCKER_SERVER_URL,APACHE_BASE_IMAGE,CPU_SHARES,MEM_LIMIT,APACHE_LINKS,APACHE_COMMAND,HOST_IP,APACHE_CONTAINER_NAME)
	apache.start()
	print apache.get_status(),apache.get_id()

def test_mysql():
	mysql = MysqlContainer(DOCKER_SERVER_URL,MYSQL_BASE_IMAGE,CPU_SHARES,MEM_LIMIT,MYSQL_LINKS,MYSQL_COMMAND,HOST_IP,MYSQL_CONTAINER_NAME)
	mysql.start()
	print mysql.get_status(),mysql.get_id()

def test_robust():
	robust = RobustContainer(DOCKER_SERVER_URL,ROBUST_BASE_IMAGE,CPU_SHARES,MEM_LIMIT,ROBUST_LINKS,ROBUST_COMMAND,HOST_IP,ROBUST_CONTAINER_NAME)
	robust.start()
	#robust.stop()
	print robust.get_status(),robust.get_id()

def test_docker_client():
	client = DockerClient(DOCKER_SERVER_URL)
	print client.get_container_status('apache')
	print client.get_container_status('mysql')
	print client.get_container_status('robust')
	print client.get_container_status('huyu')
	print client.get_container_status('xwd')
	print client.get_container_status('mycontainer')
	print client.get_container_status('xxx')

def main():
	#test_apache()
	#test_mysql()
	test_robust()
	#test_docker_client()

if __name__=="__main__":
	main()
