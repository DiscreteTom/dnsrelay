'''
provide class `Data`
'''

import yaml

class Data:
	'''
	store DNS data, provide `Data.find(url)` and `Data.add(name, ttl, cls, type, value)`
	'''
	def __init__(self, filename: str, debugLevel = 0):
		'''
		init instance with `filename`

		`debugLevel` should in `[0, 1, 2]`
		'''
		self.filename = filename
		self.debugLevel = debugLevel

		# load data from yaml file
		f = open(filename, encoding='utf-8')
		self.data = yaml.safe_load(f)
		f.close()
	
	def find(self, url: str) -> list:
		'''
		- if `url` is found, return its ip address
		- if `url` is '0.0.0.0', return '0.0.0.0'
		- if `url` is not found, return empty str
		'''
		#TODO: 
		if url in self.data :
			return self.data[url]
		else:
			return ['']


	def add(self, name: str, ttl: int, cls: str, type: str, value: str) -> None:
		'''
		add a record to data file
		'''
		#ODO: add record to self.data
		if name in self.data	:
			self.data[name].append(value)
		else	:
			self.data[name] = [value]
		# save current data to data file
		f = open(self.filename, 'w', encoding='utf-8')
		yaml.safe_dump(self.data, f)
		f.close()