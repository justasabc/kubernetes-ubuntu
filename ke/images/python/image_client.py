#Image client module
#Author: justasabc
#Created: 2015/3/31
#Copyright (C) 2015 justasabc
"""
Class Hierarchy

G{classtree: ImageClient} 

Import Graph
G{importgraph: ImageClient} 
"""

from docker import Client

class ImageClient:
	"""
	Image client class
	"""

	def __init__(self,base_url):
		"""
		Init image client instance
		"""
		self.client = Client(base_url)
		"""
		@type: L{docker.Client}
		"""

	def build_image(self,dockerfile_folder,tag,rm):
		return self.client.build(path=dockerfile_folder,tag=tag,rm=rm)

	def commit_image(self,container,repository,tag,message,author):
		return self.client.commit(container=container,repository=repository,tag=tag,message=message,author=author)

	def tag_image(self,image,repository,tag):
		return self.client.tag(image=image,repository=repository,tag=tag)

	def remove_image(self,image):
		return self.client.remove_image(image)

	def list_images(self):
		return self.client.images()

	def inspect_image(self,image):
		return self.client.inspect_image(image)

	def history_image(self,image):
		return self.client.history(image)

class ImageClientTesting(ImageClient):

	def __init__(self):
		DOCKER_SERVER_URL = 'unix://var/run/docker.sock'
		ImageClient.__init__(self,DOCKER_SERVER_URL)

	def run(self):
		print ImageClient.list_images(self)

def main():
	test = ImageClientTesting()
	test.run()

if __name__ == '__main__':
	main()
		
