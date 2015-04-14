
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

