#/usr/bin/python
# -*- coding:utf-8 -*-

import subprocess
import os

class BaseCommander:
	"""
	execute external commands
	"""
	def __init__(self,name):
		self.name = name

	def execute_external_command(self,command_str):
		print "[BaseCommander] {0}".format(command_str)
		p = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		value = ""
		for line in p.stdout.readlines():
			value += line
		return_code = p.wait()
		return value.rstrip()

class UtilityCommander(BaseCommander):
	"""
	utility commander
	"""

	def __init__(self):
		BaseCommander.__init__(self,"UtilityCommander")

	def get_host_ip(self):
		command_str = "/sbin/ifconfig $ETH0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
		return BaseCommander.execute_external_command(self,command_str)

	def get_container_ip(self,container_name):
		command_str = "docker inspect -f '{{ .NetworkSettings.IPAddress }}' {0}".format(container_name)
		return BaseCommander.execute_external_command(self,command_str)

	def copy_region_xml_to_minions(self,minions):
		# scp -r xml/* minion1:/volumes/var/www/region_load/
		for minion in minions:
			print "copying xml to {0}...".format(minion)
			command_str = "scp -r xml/* {0}:/volumes/var/www/region_load/".format(minion)
			BaseCommander.execute_external_command(self,command_str)

class KubernetesCommander(BaseCommander):
	"""
	kubernetes commander
	"""

	def __init__(self):
		BaseCommander.__init__(self,"KubernetesCommander")

	def __create(self,type_name,config_file):
		command_str = "kubecfg -c {0} create {1}".format(config_file,type_name)
		return BaseCommander.execute_external_command(self,command_str)

	def __list(self,type_name):
		command_str = "kubecfg list {0}".format(type_name)
		return BaseCommander.execute_external_command(self,command_str)

	def __delete(self,type_name,type_id):
		command_str = "kubecfg delete {0}/{1}".format(type_name,type_id)
		return BaseCommander.execute_external_command(self,command_str)

	#=====================================================================
	# create pod/service/replicationController/node/minion/event
	#=====================================================================
	def create_pod(self,config_file):
		type_name = "pods"
		return self.__create(type_name,config_file)

	def create_service(self,config_file):
		type_name = "services"
		return self.__create(type_name,config_file)

	def create_replication_controller(self,config_file):
		type_name = "replicationControllers"
		return self.__create(type_name,config_file)

	def create_node(self,config_file):
		type_name = "nodes"
		return self.__create(type_name,config_file)

	def create_minion(self,config_file):
		type_name = "minions"
		return self.__create(type_name,config_file)

	def create_event(self,config_file):
		type_name = "events"
		return self.__create(type_name,config_file)

	#=====================================================================
	# list pod/service/replicationController/node/minion/event
	#=====================================================================
	def list_pods(self):
		type_name = "pods"
		return self.__list(type_name)

	def list_services(self):
		type_name = "services"
		return self.__list(type_name)

	def list_replication_controller(self):
		type_name = "replicationControllers"
		return self.__list(type_name)

	def list_nodes(self):
		type_name = "nodes"
		return self.__list(type_name)

	def list_minions(self):
		type_name = "minions"
		return self.__list(type_name)

	def list_events(self):
		type_name = "events"
		return self.__list(type_name)

	#=====================================================================
	# delete pod/service/replicationController/node/minion/event
	#=====================================================================
	def delete_pod(self,type_id):
		type_name = "pods"
		return self.__delete(type_name,type_id)

	def delete_service(self,type_id):
		type_name = "services"
		return self.__delete(type_name,type_id)

	def delete_replication_controller(self,type_id):
		type_name = "replicationControllers"
		return self.__delete(type_name,type_id)

	def delete_node(self,type_id):
		type_name = "nodes"
		return self.__delete(type_name,type_id)

	def delete_minion(self,type_id):
		type_name = "minions"
		return self.__delete(type_name,type_id)

	def delete_event(self,type_id):
		type_name = "events"
		return self.__delete(type_name,type_id)

	#=====================================================================
	# get pod hostname
	#=====================================================================
	def get_pod_hostname(self,pod_id):
		command_str = "kubecfg list pods | grep "+pod_id+ " | awk '{print $3;}' | cut -f1 -d/"
		return BaseCommander.execute_external_command(self,command_str)

	def hostname_to_ip(self,hostname):
		command_str = "resolveip -s {0}".format(hostname)
		return BaseCommander.execute_external_command(self,command_str)

class IptablesCommander(BaseCommander):
	"""
	iptables commander
	"""
	def __init__(self):
		BaseCommander.__init__(self,"BaseCommander")

	#==========================================================
	# nat flush PREROUTING/POSTROUTING/INPUT/OUTPUT chains
	#==========================================================
	def nat_flush_prerouting_chain(self):
		command_str = "iptables -t nat -F PREROUTING"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_flush_postrouting_chain(self):
		command_str = "iptables -t nat -F POSTROUTING"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_flush_input_chain(self):
		command_str = "iptables -t nat -F INPUT"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_flush_output_chain(self):
		command_str = "iptables -t nat -F OUTPUT"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_flush_all_chains(self):
		self.nat_flush_prerouting_chain()
		self.nat_flush_postrouting_chain()
		self.nat_flush_input_chain()
		self.nat_flush_output_chain()

	#==========================================================
	# nat list PREROUTING/POSTROUTING/INPUT/OUTPUT chains
	#==========================================================
	def nat_list_prerouting_chain(self,with_line_numbers=False):
		command_str = "iptables -t nat -L PREROUTING"
		if with_line_numbers:
			command_str += " --line-numbers"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_list_postrouting_chain(self,with_line_numbers=False):
		command_str = "iptables -t nat -L POSTROUTING"
		if with_line_numbers:
			command_str += " --line-numbers"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_list_input_chain(self,with_line_numbers=False):
		command_str = "iptables -t nat -L INPUT"
		if with_line_numbers:
			command_str += " --line-numbers"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_list_output_chain(self,with_line_numbers=False):
		command_str = "iptables -t nat -L OUTPUT"
		if with_line_numbers:
			command_str += " --line-numbers"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_list_all_chains(self):
		result = ""
		result += (self.nat_list_prerouting_chain() + "\n")
		result += (self.nat_list_postrouting_chain() + "\n")
		result += (self.nat_list_input_chain() + "\n")
		result += (self.nat_list_output_chain() + "\n")
		return result.rstrip()

	#==========================================================
	# nat add rules to PREROUTING/POSTROUTING/INPUT/OUTPUT chains
	#==========================================================
	def nat_add_rule_to_prerouting_chain(self,protocol,src_port,dst_port,src_ip,dst_ip):
		command_str = "iptables -t nat -A PREROUTING -p {0} --dport {1} -j DNAT --to-destination {2}:{3}".format(protocol,dst_port,dst_ip,dst_port)
		return BaseCommander.execute_external_command(self,command_str)

	def nat_add_rule_to_postrouting_chain(self,protocol,src_port,dst_port,src_ip,dst_ip):
		command_str = "iptables -t nat -A POSTROUTING -p {0} -d {1} --dport {2} -j SNAT --to-source {4}".format(protocol,dst_ip,dst_port,src_ip)
		return BaseCommander.execute_external_command(self,command_str)

	def nat_add_rule_to_input_chain(self,protocol,src_port,dst_port,src_ip,dst_ip):
		command_str = "ls"
		return BaseCommander.execute_external_command(self,command_str)

	def nat_add_rule_to_output_chain(self,protocol,src_port,dst_port,src_ip,dst_ip):
		command_str = "ls"
		return BaseCommander.execute_external_command(self,command_str)

	#==========================================================
	# nat delete rules to PREROUTING/POSTROUTING/INPUT/OUTPUT chains
	#==========================================================
	def nat_delete_rule_from_prerouting_chain(self,rule_number):
		command_str = "iptables -t nat -D PREROUTING {0}".format(rule_number)
		return BaseCommander.execute_external_command(self,command_str)

	def nat_delete_rule_from_postrouting_chain(self,rule_number):
		command_str = "iptables -t nat -D POSTROUTING {0}".format(rule_number)
		return BaseCommander.execute_external_command(self,command_str)

	def nat_delete_rule_from_input_chain(self,rule_number):
		command_str = "iptables -t nat -D INPUT {0}".format(rule_number)
		return BaseCommander.execute_external_command(self,command_str)

	def nat_delete_rule_from_output_chain(self,rule_number):
		command_str = "iptables -t nat -D OUTPUT {0}".format(rule_number)
		return BaseCommander.execute_external_command(self,command_str)

def test(): 
	cmd = IptablesCommander()
	cmd.nat_flush_prerouting_chain()
	print cmd.nat_list_all_chains()
	print "OK"
	cmd = UtilityCommander()
	print cmd.get_host_ip()
	print "OK"
	cmd = KubernetesCommander()
	hostname = cmd.get_pod_hostname("apache-pod")
	print cmd.hostname_to_ip(hostname)
	print "OK"

def main():
	test()

if __name__=="__main__":
	main()
