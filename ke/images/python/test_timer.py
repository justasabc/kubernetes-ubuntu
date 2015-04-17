from threading import Thread,Timer,Event

class MyClass(Thread):

	def __init__(self):
        	Thread.__init__(self)
		self.stopped = Event()

	def do_work(self):
		print "working..."

	def run(self):
        	while not self.stopped.wait(1):
			self.do_work()
			#self.stop()

	def start(self):
		print "start"
		Thread.start(self)

	def stop(self):
		self.stopped.set()

c = MyClass()
c.start()
