if __name__ == '__main__':
	import argparse
	from net import NetController

	# construct argument parser
	parser = argparse.ArgumentParser()
	optGroup = parser.add_mutually_exclusive_group()
	parser.set_defaults(**{'debugLevel': 0, 'filename': 'dnsrelay.yml', 'serverAddr': '10.3.9.5'})
	optGroup.add_argument('-d', action='store_true', dest='debugLevel', help='level-1 debug')
	optGroup.add_argument('-dd', action='store_true', dest='debugLeve2', help='level-2 debug')
	parser.add_argument('dns-server-ipaddr', nargs = '?', help='dns server ip address, "10.3.9.5" by default', dest='serverAddr')
	parser.add_argument('filename', nargs='?', help='dns file name, "dnsrelay.yml" by default')

	# parse args
	args = parser.parse_args()

	# start relay controller
	level = 0
	if args['debugLevel']:
		level=1
	if args['debugLevel2']:
		level = 2
	net = NetController(args['serverAddr'], args['filename'], level)
	net.start()