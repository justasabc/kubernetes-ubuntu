#/usr/bin/python
# -*- coding:utf-8 -*-
import json

class JsonGenerator:
	"""
	generate json file from dict data
	"""
	def __init__(self,name):
		self.name = name

	def generate(self,dict_data,file_path):
		with open(file_path, 'w') as fp:
    			json.dump(dict_data, fp, indent=4, separators=(',',':'),sort_keys=True)
		print "[JsonGenerator] generate {0}".format(file_path)

