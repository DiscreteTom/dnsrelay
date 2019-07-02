from data import Data
import multiprocessing # may be used in concurrency control

class Processor:
	def __init__(self, netController, filename: str, debugLevel = 0):
		'''
		init a processor

		`filename` is the DNS data file

		`debugLevel` should in `[0, 1, 2]`
		'''
		self.data = Data(filename, debugLevel)
		self.net = netController

	def parse(self, data: dict) -> None:
		'''
		may be called many times simultaneously, need concurrency control
		'''
		# TODO: parse data and get result
		result = {}
		# reply 
		