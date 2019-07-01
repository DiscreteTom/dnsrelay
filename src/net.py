'''
provide class `NetController`
'''

from processor import Processor

class NetController:
	def __init__(self, dnsFileName: str, debugLevel = 0):
		'''
		construct a net controller

		`debugLevel` should in `[0, 1, 2]`
		'''
		self.processor = Processor(self, dnsFileName, debugLevel)

	def start(self) -> bool:
		'''
		start this net controller. it will start a UDP server

		return False if error occurs, else return True
		'''
		# TODO: start a UDP server and listen

		while True:
			data = {} # TODO: read data from socket and parse data into a dict
			# if this package is a DNS request, parse it
			self.processor.parse(data)
			# TODO: if this package is a DNS reply from a DNS server, send it to the client
	
	def reply(self, data: dict) -> None:
		'''
		construct an UDP package and send it to the client
		'''
		# TODO
	
	def query(self, data: dict) -> None:
		'''
		contruct an UDP package and send it to DNS server
		'''
		# TODO