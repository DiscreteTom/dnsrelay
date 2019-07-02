'''
provide class `NetController`
'''

from processor import Processor
from refdict import refdict

class NetController:
	def __init__(self, dnsFileName: str, debugLevel = 0):
		'''
		construct a net controller

		`debugLevel` should in `[0, 1, 2]`
		'''
		self.processor = Processor(self, dnsFileName, debugLevel)
		self.debugLevel = debugLevel

	def start(self) -> bool:
		'''
		start this net controller. it will start a UDP server

		return False if error occurs, else return True
		'''
		import socket
		address = ('', 53)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(address)

		while True:
			data = self.packageToDict(*s.recvfrom(2048))
			self.processor.parse(data)
		
		s.close()
		return True
	
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

	def dictToPackage(self, data: dict) -> (tuple, bytes):
		'''
		return `((ip: str, port: int), msg: bytes)`
		'''
		# construct address
		address = (data['address.ip'], data['address.port'])
		# construct msg header
		msg = address['data.id']
		t = 0b00000000 if data['data.qr'] else 0b10000000
		t |= data['data.opcode'] << 3
		if data['data.aa']:
			t |= 0b00000100 
		if data['data.tc']:
			t |= 0b00000010
		if data['data.rd']:
			t |= 0b00000001
		msg += bytes([t])
		t = 0b10000000 if data['data.ra'] else 0b00000000
		t |= data['data.rcode']
		msg += bytes([t])
		msg += bytes([data['data.qdcount'] >> 8])
		msg += bytes([data['data.qdcount'] & 0b0000000011111111])
		msg += bytes([data['data.ancount'] >> 8])
		msg += bytes([data['data.ancount'] & 0b0000000011111111])
		msg += bytes([data['data.arcount'] >> 8])
		msg += bytes([data['data.arcount'] & 0b0000000011111111])
		# construct question
		msg += bytes(data['data.question.qname'].encode('utf-8'))
		msg += bytes([0])
		msg += bytes([data['data.question.qtype'] >> 8])
		msg += bytes([data['data.question.qtype'] & 0b0000000011111111])
		msg += bytes([data['data.question.qclass'] >> 8])
		msg += bytes([data['data.question.qclass'] & 0b0000000011111111])
		# construct answers
		for i in range(data['data.ancount']):
			msg += resourceToBytes(data['data.answer'][i])
		# construct authorities
		for i in range(data['data.nscount']):
			msg += resourceToBytes(data['data.authority'][i])
		# construct additionals
		for i in range(data['data.arcount']):
			msg += resourceToBytes(data['data.additional'][i])
		return msg

	def packageToDict(self, rawData: bytes, address: tuple) -> dict:
		'''
		parse `rawData` and `address` to a dict and return
		'''
		# construct header and address
		data = refdict({
			'address': {
				'ip': address[0],
				'port': address[1]
			},
			'data': {
				'header': {
					'id': rawData[0:2],
					'qr': bool(rawData[2] & 0b10000000),
					'opcode': (rawData[2] & 0b01111111) >> 3,
					'aa': bool(rawData[2] & 0b00000100),
					'tc': bool(rawData[2] & 0b00000010),
					'rd': bool(rawData[2] & 0b00000001),
					'ra': bool(rawData[3] & 0b10000000),
					'rcode': rawData[3] & 0b00001111,
					'qdcount': rawData[4] << 8 + rawData[5],
					'ancount': rawData[6] << 8 + rawData[7],
					'nscount': rawData[8] << 8 + rawData[9],
					'arcount': rawData[10] << 8 + rawData[11]
				},
				'question': [],
				'answer': [],
				'authority': [],
				'additional': []
			}
		})
		# construct questions
		index = 12 # index of rawData
		for i in range(data['data.qdcount']):
			nameEnd = NetController.getNameEnd(rawData, index)
			question = {
				'qname': rawData[index:nameEnd].decode('utf-8'),
				'qtype': rawData[nameEnd + 1] << 8 + rawData[nameEnd + 2],
				'qclass': rawData[nameEnd +3] << 8 + rawData[nameEnd + 4]
			}
			index = nameEnd + 5
			data['data.question'].append(question)
		# construct answers
		for i in range(data['data.ancount']):
			index, answer = getResource(rawData, index)
			data['data.answer'].append(answer)
		# construct authorities
		for i in range(data['data.nscount']):
			index, answer = getResource(rawData, index)
			data['data.authority'].append(answer)
		# construct additionals
		for i in range(data['data.arcount']):
			index, answer = getResource(rawData, index)
			data['data.additional'].append(answer)
		return data

	@classmethod
	def resourceToBytes(cls, data: dict) -> bytes:
		result = data['name'].encode('utf-8') + bytes([0])
		result += bytes([data['type'] >> 8])
		result += bytes([data['type'] & 0b0000000011111111])
		result += bytes([data['class'] >> 8])
		result += bytes([data['class'] & 0b0000000011111111])
		result += bytes([data['ttl'] >> 24])
		result += bytes([data['ttl'] >> 16] & 0b0000000011111111)
		result += bytes([data['ttl'] >> 8] & 0b000000000000000011111111)
		result += bytes([data['ttl'] & 0b00000000000000000000000011111111])
		result += bytes([data['rdlength'] >> 8])
		result += bytes([data['rdlength'] & 0b0000000011111111])
		result += data['rdata']
		return result

	@classmethod
	def getNameEnd(cls, rawData: bytes, startIndex: int) -> int:
		'''
		return the tail index of the name
		'''
		while rawData[startIndex] != 0:
			startIndex += 1
		return startIndex

	@classmethod
	def getResource(cls, rawData: bytes, startIndex: int) -> (int, dict):
		'''
		return end index and resource
		'''
		# construct name
		result = {}
		if rawData[startIndex] & 0b11000000 == 0b11000000:
			# this is a compressed format name
			offset = (rawData[startIndex] & 0b00111111) << 8 + rawData[startIndex + 1]
			nameEnd = getNameEnd(rawData, offset)
			result['name'] = rawData[offset:nameEnd].decode('utf-8')
			startIndex = nameEnd + 1
		else:
			nameEnd = getNameEnd(rawData, startIndex)
			result['name'] = rawData[startIndex:nameEnd]
			startIndex = nameEnd + 1
		# construct others
		result['type'] = rawData[startIndex] << 8 + rawData[startIndex + 1]
		startIndex += 2
		result['class'] = rawData[startIndex] << 8 + rawData[startIndex + 1]
		startIndex += 2
		result['ttl'] = rawData[startIndex] << 24 + rawData[startIndex + 1] << 16 + rawData[startIndex + 2] << 8 + rawData[startIndex + 3]
		startIndex += 4
		result['rdlength'] = rawData[startIndex] << 8 + rawData[startIndex + 1]
		startIndex += 2
		result['rdata'] = rawData[startIndex:startIndex + result['rdlength']].decode('utf-8')
		startIndex += result['rdlength']
		return startIndex, result
