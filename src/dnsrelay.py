if __name__ == '__main__':
	import argparse
	from net import NetController

	# construct argument parser
	parser = argparse.ArgumentParser()
	optGroup = parser.add_mutually_exclusive_group()
	optGroup.add_argument('-d', action='store_const', const='1', dest='debugLevel', default=0, help='level-1 debug')
	optGroup.add_argument('-dd', action='store_const', const='2', dest='debugLevel', help='level-2 debug')
	parser.add_argument('dns-server-ipaddr', nargs = '?', default='10.3.9.5', help='dns server ip address, "10.3.9.5" by default')
	parser.add_argument('filename', nargs='?', default='dnsrelay.yml', help='dns file name, "dnsrelay.yml" by default')

	# parse args
	args = parser.parse_args()

	# start relay controller
	net = NetController(args['dns-server-ipaddr'], args['filename'], args['debugLevel'])
	net.start()