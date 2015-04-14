from docker import Client

c = Client('tcp://master:2375')
print c.version()
