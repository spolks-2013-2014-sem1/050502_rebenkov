#!/usr/bin/python			#spolks lab3 main.py
#A simple client-server app for file transmit via TCP.

import sys				#import some modules
import socket
import argparse
import os

BUF_SIZE = 128			#randomly generated 2^n size buffer


def run_server(port, filename):
	
	if 0 <= port <= 65535:
		s = socket.socket()		#read docs.python.org
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('',port))
		s.listen(1)
		conn, addr = s.accept()
		print 'Got connection from', addr
	else: return 0
	
	f = open(filename, 'rb')
	filesize = os.stat(filename).st_size
	sentsize = 0
	perflag = 0
	
	while True:
		data = f.read(BUF_SIZE)
		sentsize += BUF_SIZE
		percent = int(float(sentsize)*100/float(filesize))
		print "{} Kb of {} Kb sent ({}%)".format(sentsize/1024, filesize/1024, percent)
		sys.stdout.write('\033M')
		if not data:
			sys.stdout.write('\033D')
			print 'Data has been transfered'
			break
		try:
			conn.send(data)
		except socket.error:
			print 'Transfer fail'
			sys.exit
		if (percent % 10 == 0) & (perflag != percent):
			perflag = percent
			sys.stdout.write('\033D')
			print 'Urgent flag sent at {}%'.format(percent)
			conn.send(b'{}'.format(percent/10), socket.MSG_OOB)
		if (percent == 100) & (perflag != percent):
			perflag = percent
			sys.stdout.write('\033D')
			print 'Urgent flag sent at {}%'.format(percent)
			conn.send(b'{!}', socket.MSG_OOB)
			
	f.close()				#please close your files
	conn.close()			#and connections
	s.close()				#CLOSE 'EM ALL!!!
	
	
def run_client(host, port):
	if 0 <= port <= 65535:
		s = socket.socket()		#didn't you read docs.python.org?
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
#		host = socket.gethostname() #it could be anywhere
		s.connect((host,port))
	else:
		print 'Port # must be in range 0-65535'
		return
	
	f = open('rcvd.file','wb')
	rcvdsize = 0
	s.settimeout(2)
	
	while True:
		try:
			data = s.recv(2, socket.MSG_OOB)
		except socket.error, value:
			data = None
		if (data == '!'):
			print '{} Kb (100%) received'.format(rcvdsize/1024)
		elif data:
			print '{} Kb ({}0%) received'.format(rcvdsize/1024, data)
		else:
			data = s.recv(BUF_SIZE)
			rcvdsize += BUF_SIZE
			f.write(data)
		if not data:
			break
			
			
	print 'Done!'
	f.close()
	s.close()
	 

def main():
	parser = argparse.ArgumentParser()
#	subparsers = parser.add_subparsers(help='Select mode')
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-s", "--server", help="Run as server", action="store_true")
	group.add_argument("-c", "--client", help="Run as client", action="store_true")
	parser.add_argument("-a", "--address", help="Destination host (client mode)", default="127.0.0.1")
	parser.add_argument("-p", "--port", type=int, help="Port to listen/connect to", default=12345)
	parser.add_argument("-f", "--file", help="File to send (server mode)", default="send.file")
	args = parser.parse_args()
	if args.server:
		print 'Server mode'
		run_server(args.port, args.file)
	if args.client:
		print 'Client mode'
		run_client(args.address, args.port)

if __name__ == '__main__':
        main()
