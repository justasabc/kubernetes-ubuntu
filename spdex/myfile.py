# -*- coding:utf-8 -*-
__author__ = "kezunlin"
import requests
import os
from setting import *

# https://github.com/justasabc/python_tutorials/blob/master/project/download/getimages.py
#IMAGE_CHUNK_SIZE = 20*1024

class MyFile:

	def ensure_dir(self,d):
		if not os.path.exists(d):
			print "Making dir {0}...".format(d)
			os.makedirs(d)
	
	def download_image(self,url,filepath,overwrite=False):
		# ./charts/jc/20150501/20150501001_home.jpg
		# ./charts/m14/15067/15067001_home.jpg
		root_dir = os.path.dirname(filepath)
		self.ensure_dir(root_dir)
		exist = os.path.exists(filepath)
		if (exist and overwrite) or not exist :
	    		r = requests.get(url,stream=True)
			if r.status_code == 200:
    				with open(filepath, 'wb') as f:
					print "Saving {0}...".format(filepath)
        				for chunk in r.iter_content(IMAGE_CHUNK_SIZE):
            					f.write(chunk)