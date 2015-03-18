#/usr/bin/python
# -*- coding:utf-8 -*-

from commander import UtilityCommander,KubernetesCommander,IptablesCommander

HOST_IP = UtilityCommander().get_host_ip()

class BaseProxy:
	"""
	base proxy: set up a network proxy between client and server(apache,robust,opensim)
	"""
	def __init__(self,protocol,src_port,dst_port,src_ip,dst_ip):
		self.protocol = protocol
		self.src_port = src_port
		self.dst_port = dst_port
		self.src_ip = src_ip
		self.dst_ip = dst_ip

	def get_protocol(self):
		return self.protocol 

	def get_src_port(self):
		return self.src_port

	def get_dst_port(self):
		return self.dst_port

	def get_src_ip(self):
		return self.src_ip 

	def get_dst_ip(self):
		return self.dst_ip

	def __setup_proxy(self,protocol,src_port,dst_port,src_ip,dst_ip):
		cmd = IptablesCommander()
		cmd.nat_add_rule_to_prerouting_chain(protocol,src_port,dst_port,src_ip,dst_ip)
		cmd.nat_add_rule_to_postrouting_chain(protocol,src_port,dst_port,src_ip,dst_ip)

	def setup(self):
		self.__setup_proxy(self.protocol,self.src_port,self.dst_port,self.src_ip,self.dst_ip)

class ApacheProxy(BaseProxy):
	"""
	apache proxy
	"""

	def __init__(self):
		self.__init_setting()

	def __init_setting(self):
		print "[ApacheProxy] init..."
		protocol = "tcp"
		src_port = 880
		dst_port = 880
		src_ip =  HOST_IP

		cmd = KubernetesCommander()
		pod_id = "apache"
		hostname = cmd.get_pod_hostname(pod_id)
		dst_ip = cmd.hostname_to_ip(hostname)

		BaseProxy.__init__(self,protocol,src_port,dst_port,src_ip,dst_ip)

	def setup(self):
		BaseProxy.setup(self)
		print "[ApacheProxy] setup"

class MysqlProxy(BaseProxy):
	"""
	mysql proxy
	"""

	def __init__(self):
		self.__init_setting()

	def __init_setting(self):
		print "[MysqlProxy] init..."
		protocol = "tcp"
		src_port = 3306
		dst_port = 3306
		src_ip =  HOST_IP

		cmd = KubernetesCommander()
		pod_id = "mysql"
		hostname = cmd.get_pod_hostname(pod_id)
		dst_ip = cmd.hostname_to_ip(hostname)

		BaseProxy.__init__(self,protocol,src_port,dst_port,src_ip,dst_ip)

	def setup(self):
		BaseProxy.setup(self)
		print "[MysqlProxy] setup"

class RobustProxy(BaseProxy):
	"""
	robust proxy
	"""

	def __init__(self):
		self.__init_setting()

	def __init_setting(self):
		print "[RobustProxy] init..."
		protocol = "tcp"
		src_port = 8002
		dst_port = 8002
		src_ip =  HOST_IP

		cmd = KubernetesCommander()
		pod_id = "robust"
		hostname = cmd.get_pod_hostname(pod_id)
		dst_ip = cmd.hostname_to_ip(hostname)

		BaseProxy.__init__(self,protocol,src_port,dst_port,src_ip,dst_ip)

	def setup(self):
		BaseProxy.setup(self)
		print "[RobustProxy] setup"

class SimulatorProxy(BaseProxy):
	"""
	simulator proxy
	"""

	def __init__(self,protocol,src_port,dst_port,src_ip,dst_ip):
		BaseProxy.__init__(self,protocol,src_port,dst_port,src_ip,dst_ip)

	def setup(self):
		BaseProxy.setup(self)

class RegionProxy(BaseProxy):
	"""
	region proxy
	"""

	def __init__(self,protocol,src_port,dst_port,src_ip,dst_ip):
		BaseProxy.__init__(self,protocol,src_port,dst_port,src_ip,dst_ip)

	def setup(self):
		BaseProxy.setup(self)

class OpensimProxy:
	"""
	opensim proxy:  1 simulator proxy + N region proxy
	"""

	def __init__(self,simulator):
		self.simulator = simulator
		self.simulator_proxy = None
		self.region_proxy_list = []
		self.__init_setting(simulator)

	def set_simulator_proxy(self,simulator_proxy):
		self.simulator_proxy = simulator_proxy

	def get_simulator_proxy(self):
		return self.simulator_proxy

	def append_region_proxy(self,region_proxy):
		self.region_proxy_list.append(region_proxy)

	def get_region_proxy_list(self):
		return self.region_proxy_list

	def __create_simulator_proxy(self,protocol,src_port,dst_port,src_ip,dst_ip):
		simulator_proxy = SimulatorProxy(protocol,src_port,dst_port,src_ip,dst_ip)
		return simulator_proxy

	def __create_region_proxy(self,protocol,src_port,dst_port,src_ip,dst_ip):
		region_proxy = RegionProxy(protocol,src_port,dst_port,src_ip,dst_ip)
		return region_proxy

	def __init_setting(self,simulator):
		sim_name = simulator.get_simulator_name()
		sim_port = simulator.get_simulator_port()
		region_port_list = simulator.get_region_port_list()
		print "[OpensimProxy] {0} init...".format(sim_name)

		src_ip =  HOST_IP
		cmd = KubernetesCommander()
		pod_id = sim_name
		hostname = cmd.get_pod_hostname(pod_id)
		dst_ip = cmd.hostname_to_ip(hostname)

		# create simulator proxy
		src_port = dst_port = sim_port
		simulator_proxy = self.__create_simulator_proxy("tcp",src_port,dst_port,src_ip,dst_ip)
		self.set_simulator_proxy(simulator_proxy)

		# create N region proxy
		for region_port in region_port_list:
			src_port = dst_port = region_port
			region_proxy = self.__create_region_proxy("udp",src_port,dst_port,src_ip,dst_ip)
			self.append_region_proxy(region_proxy)

	def setup(self):
		self.simulator_proxy.setup()
		for region_proxy in self.get_region_proxy_list():
			region_proxy.setup()
		sim_name = self.simulator.get_simulator_name()
		print "[OpensimProxy] {0} setup".format(sim_name)

class NetworkProxy:
	"""
	1 ApacheProxy + 1 MysqlProxy + 1 RobustProxy + N OpensimProxy
	"""

	def __init__(self,apache_proxy,mysql_proxy,robust_proxy,opensim_proxy_list):
		self.apache_proxy = apache_proxy
		self.mysql_proxy = mysql_proxy
		self.robust_proxy = robust_proxy
		self.opensim_proxy_list = opensim_proxy_list

	def set_apache_proxy(self,apache_proxy):
		self.apache_proxy = apache_proxy

	def get_apache_proxy(self):
		return self.apache_proxy

	def set_mysql_proxy(self,mysql_proxy):
		self.mysql_proxy = mysql_proxy

	def get_mysql_proxy(self):
		return self.mysql_proxy

	def set_robust_proxy(self,robust_proxy):
		self.robust_proxy = robust_proxy

	def get_robust_proxy(self):
		return self.robust_proxy

	def set_opensim_proxy_list(self,opensim_proxy_list):
		self.opensim_proxy_list = opensim_proxy_list

	def get_opensim_proxy_list(self):
		return self.opensim_proxy_list

	def setup(self):
		self.apache_proxy.setup()
		self.mysql_proxy.setup()
		self.robust_proxy.setup()
		for opensim_proxy in self.get_opensim_proxy_list():
			opensim_proxy.setup()

class ProxyServer(NetworkProxy):
	"""
	proxy server
	"""
	def __init__(self,simulator_list):
		self.__init_setting(simulator_list)

	def __create_apache_proxy(self):
		return ApacheProxy()

	def __create_mysql_proxy(self):
		return MysqlProxy()

	def __create_robust_proxy(self):
		return RobustProxy()

	def __create_opensim_proxy(self,simulator):
		return OpensimProxy(simulator)

	def __init_setting(self,simulator_list):
		apache_proxy = self.__create_apache_proxy()
		mysql_proxy = self.__create_mysql_proxy()
		robust_proxy = self.__create_robust_proxy()
		opensim_proxy_list = []
		for simulator in simulator_list:
			opensim_proxy = self.__create_opensim_proxy(simulator)
			opensim_proxy_list.append(opensim_proxy)
		# init 
		NetworkProxy.__init__(self,apache_proxy,mysql_proxy,robust_proxy,opensim_proxy_list)

	def __clear_chains(self):
		print "[ProxyServer] clear chains..."
		cmd = IptablesCommander()
		cmd.nat_flush_all_chains()

	def __list_chains(self):
		print "*"*110
		print "[ProxyServer] list chains..."
		cmd = IptablesCommander()
		print cmd.nat_list_all_chains()
		print "*"*110

	def start(self):
		print "[ProxyServer] is starting..."
		self.__clear_chains()
		NetworkProxy.setup(self)
		#self.__list_chains()
		print "[ProxyServer] started..."

	def stop(self):
		print "[ProxyServer] is stopping..."
		self.__clear_chains()
		print "[ProxyServer] stopped..."

def test():
	ap = ApacheProxy()
	ap.setup()
	mp = MysqlProxy()
	mp.setup()
	rp = RobustProxy()
	rp.setup()

def main():
	test()

if __name__=="__main__":
	main()
