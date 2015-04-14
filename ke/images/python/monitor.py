#/usr/bin/python
# -*- coding:utf-8 -*-

class ContainerStats:
	"""
	container stats

	example:
	name	cpu_percentage	memory_usage/memory_limit memory_percentage network_rx/network_tx
	cadvisor            0.00%               12.02 MiB/31.39 GiB   0.04%               762 KiB/26.25 MiB
	"""

	def __init__(self,name,cpu_percentage,memory_usage,memory_limit,memory_percentage,network_rx,network_tx):
		self.name = name
		self.cpu_percentage = cpu_percentage
		self.memory_usage = memory_usage
		self.memory_limit = memory_limit
		self.memory_percentage = memory_percentage
		self.network_rx = network_rx
		self.network_tx = network_tx

	def set_name(self,name):
		self.name = name

	def set_cpu_percentage(self,cpu_percentage):
		self.cpu_percentage = cpu_percentage

	def set_memory_usage(self,memory_usage):
		self.memory_usage = memory_usage

	def set_memory_limit(self,memory_limit):
		self.memory_limit = memory_limit

	def set_memory_percentage(self,memory_percentage):
		self.memory_percentage = memory_percentage

	def set_network_rx(self,network_rx):
		self.network_rx = network_rx

	def set_network_tx(self,network_tx):
		self.network_tx = network_tx
		
	def get_name(self):
		return self.name

	def get_cpu_percentage(self):
		return cpu_percentage

	def get_memory_usage(self):
		return memory_usage

	def get_memory_limit(self):
		return mem_limit

	def get_memory_percentage(self):
		return memory_percentage

	def get_network_rx(self):
		return network_rx

	def get_network_tx(self):
		return network_tx

class Monitor:

	def __init__(self):
