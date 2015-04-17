
class ControllerParam:

	def __init__(self,name,replicas,replicas_selector,pod_template):
		self.name = name
		""" @type: C{string} """
		self.replicas = replicas
		""" @type: C{integer} """
		self.replicas_selector = replicas_selector
		""" @type: C{string} """
		self.pod_template = pod_template
		""" @type: L{PodParam} """

	def get_name(self):
		return self.name

	def get_replicas(self):
		return self.replicas

	def get_replicas_selector(self):
		return self.replicas_selector

	def get_pod_template(self):
		return self.pod_template

