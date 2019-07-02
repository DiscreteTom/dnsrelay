if __name__ == '__main__':
	import argparse
	from net import NetController

	# construct argument parser
	parser = argparse.ArgumentParser()
	optGroup = parser.add_mutually_exclusive_group()
	parser.set_defaults({'debugLevel': 0, 'filename': 'dnsrelay.yml'})
	optGroup.add_argument('-d', action='store_const', const='1', dest='debugLevel', help='level-1 debug')
	optGroup.add_argument('-dd', action='store_const', const='2', dest='debugLevel', help='level-2 debug')
	parser.add_argument('dns-server-ipaddr', nargs = '?', help='dns server ip address')
	parser.add_argument('filename', nargs='?', help='dns file name, "dnsrelay.yml" by default')

	# parse args
	args = parser.parse_args()

	# start relay controller
	net = NetController(args['filename'], args['debugLevel'])
	net.start()