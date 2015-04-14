
class ProxyParam:

	def __init__(self,protocol,src_port,dst_port,src_ip,dst_ip):
		self.protocol = protocol
		""" @type: C{string} """
		self.src_port = src_port
		""" @type: C{integer} """
		self.dst_port = dst_port
		""" @type: C{integer} """
		self.src_ip = src_ip
		""" @type: C{string} """
		self.dst_ip = dst_ip
		""" @type: C{string} """
