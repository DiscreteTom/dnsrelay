from data import Data
from refdict import refdict
import threading
import multiprocessing # may be used in concurrency control

def dealName(name: bytes, rawData: bytes):
	'''
	获取正确的名称
	'''
	NameTail = name[-2:]
	if(NameTail[0] & 0b11000000 == 192):
		offset = (NameTail[0] - 192)*256 + NameTail[1]
		name = name[0: len(name)-2] + getTail(rawData, offset)
	
	return name
				

def getTail(rawData: bytes, offset: int):
	'''
	递归获得通过偏移量压缩的值
	'''
	tail = bytes()
	# 存在偏移量压缩方式，在原数据中寻找
	while rawData[offset] != 0 and (rawData[offset] & 0b11000000 != 192):
		tail += rawData[offset: offset+1]
		offset += 1

	if rawData[offset] != 0:
		# 原数据存在偏移量，递归寻找
		newOffset = (rawData[offset] - 192)*256 + rawData[offset + 1]
		tail += getTail(rawData, newOffset)
	return tail

def bytesNameToStr(name: bytes):
	'''
	字节域名转字符串
	'''
	newName = bytes(name)
	num = newName[0]
	newName = newName[1:]
	while num < len(newName)-1:
		newNum = newName[num] + 1
		newName = newName[0: num] + bytes(b'.') + newName[num + 1:]
		num += newNum
	return newName.decode('utf-8')

def bytesIpToStr(ip: bytes):
	'''
	字节ip名转字符串
	'''
	ipStr = str()
	for i in range(0, 3):
		ipStr += str(ip[i]) + '.'
	ipStr += str(ip[3])
	return ipStr

class Processor:
	def __init__(self, netController = None, filename: str = '', debugLevel = 0):
		# from net import NetController
		'''
		init a processor

		`filename` is the DNS data file

		`debugLevel` should in `[0, 1, 2]`
		'''
		self.debugLevel = debugLevel
		self.data = Data(filename, debugLevel)
		self.net = netController
		# 请求列表
		self.queryList = {}
		self.defaultIp = '127.0.0.1'
		

	def parse(self, data: dict):
		'''
		may be called many times simultaneously, need concurrency control
		'''
		# TODO: parse data and get result
		t1 = threading.Thread(target=self.doParse, args = (data,))
		t1.start()
		# self.doParse(data)


	def doParse(self, data: dict):
		newData = data.copy();
		if data['data']['header']['qr']:
			if self.queryList.get(data['data']['header']['id'], None) != None:
				self.parseNames(newData)
				data['address'] = self.queryList.pop(data['data']['header']['id'], {})
				self.net.reply(data)
				for i in range(0, newData['data']['header']['ancount']):
					if newData['data']['answer'][i]['type'] == 1 and len(newData['data']['answer'][i]['rdata']) == 4:
						self.data.add(bytesNameToStr(newData['data']['question'][0]['qname'][:-1]), 0, 0, 0, bytesIpToStr(newData['data']['answer'][i]['rdata']))
			return;
		else:
			# 回复给客户端的信息
			replyData = {
				'address': {
					'ip': data['address']['ip'],
					'port': data['address']['port'],
				},
				'data': {
					'header': {
						'id': data['data']['header']['id'],
						'qr': True,
						'opcode': data['data']['header']['opcode'],
						'aa': False,
						'tc': False,
						'rd': True,
						'ra': False,
						'rcode': 0,
						'qdcount': data['data']['header']['qdcount'],
						'ancount': 0,
						'nscount': 0,
						'arcount': 0
					},
					'question': newData['data']['question'],
					'answer': [],
					'authority': [],
					'additional': []
				},
				'rawData': data['rawData']
			}

			# 处理数据
			self.parseNames(newData)
			name = bytesNameToStr(newData['data']['question'][0]['qname'])[:-1]
			ipStr = self.data.find(name)											# 进行查询
			if ipStr[0] == '' or newData['data']['question'][0]['qtype'] != 1:		# 没有记录，向服务器查询
				self.queryList[data['data']['header']['id']] = data['address']
				self.net.query(data)
				return;
			elif ipStr[0] == '0.0.0.0':												# 无效域名
				replyData['data']['header']['rcode'] = 3
			else:																	# 有效域名
				for j in range(0, len(ipStr)):
					ip = bytes(bytearray(list(map(int, ipStr[j].split('.')))))
					replyData['data']['header']['ancount'] += 1
					replyData['data']['answer'].append({
						'name': newData['data']['question'][0]['qname'],
						'type': 1,
						'class': 1,
						'ttl': 86400,
						'rdlength': 4,
						'rdata': ip
					})
			self.net.reply(refdict(replyData))
		
	def parseNames(self, newData: dict):
		rawData = newData['rawData']
			
		#deal all the names
		for i in range(0, newData['data']['header']['qdcount']):
			qname = newData['data']['question'][i]['qname']
			qname = dealName(qname, rawData)
			newData['data']['question'][i]['qname'] = qname
				
		# build a array of counts and another of names
		packsLen = [newData['data']['header']['ancount'], newData['data']['header']['nscount'], newData['data']['header']['arcount']]
		packsName = ['answer','authority','additional']

		for k in range(0, 3):
			for i in range(0, packsLen[k]):
				kname = newData['data'][packsName[k]][i]['name']
				kname = dealName(kname, rawData)
				newData['data'][packsName[k]][i]['name'] = kname
