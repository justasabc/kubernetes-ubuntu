"""
Class Hierarchy

G{classtree: ExecuteEngine} 

Package tree
G{packagetree: execute_engine} 

Import Graph
G{importgraph: execute_engine} 

"""
class ExecuteEngine:

	def __init__(self):
		self.command_list = []

	def add_command(self,cmd):
		self.command_list.append(cmd)

	def remove_command(self,cmd):
		self.command_list.remove(cmd)

	def start(self):
		# execute in order
		for cmd in self.command_list:
			cmd.start()

	def stop(self):
		# execute in reverse order
		for cmd in reversed(self.command_list):
			cmd.stop()
