#!/usr/bin/python			#spolks lab5 main.py
#A simple client-server app for file transmit via UDP

import sys				#import some modules
import socket
import argparse
import os

BUF_SIZE = 128			#randomly generated 2^n size buffer


def run_server(host, port, filename):
	
	if 0 <= port <= 65535:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#UDP
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#		s.bind(('',port))		#UDP
#		s.listen(1)
#		conn, addr = s.accept()
#		print 'Got connection from', addr
	else: return 0
	
	f = open(filename, 'rb')
	filesize = os.stat(filename).st_size
	sentsize = 0
	perflag = 0
	
	while True:
		data = f.read(BUF_SIZE)
		sentsize += BUF_SIZE
		percent = int(float(sentsize)*100/float(filesize))	#rings
		print "{} Kb of {} Kb sent ({}%)".format(sentsize/1024, filesize/1024, percent)
		sys.stdout.write('\033M')			#escape symbols rule
		if not data:
			sys.stdout.write('\033D')
			print 'Data has been transfered'
			s.sendto('TANSTAAFL', (host, port))
		#There ain't no such thing as a free lunch
			break
		try:
			s.sendto(data, (host, port))
		except socket.error:
			print 'Transfer fail'
			sys.exit

			
	f.close()				#please close your files
	s.close()				#CLOSE 'EM ALL!!!
	
	
def run_client(host, port):
	if 0 <= port <= 65535:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#UDP too
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
#		host = socket.gethostname() #it could be anywhere
		s.bind((host,port))
	else:
		print 'Port # must be in range 0-65535'
		return
	
	f = open('rcvd.file','wb')
	rcvdsize = 0
	s.settimeout(10)
	
	while True:
		
		data,addr = s.recvfrom(BUF_SIZE)
		if data == "TANSTAAFL":
			break
		rcvdsize += BUF_SIZE
		f.write(data)
		print '{} Kb received'.format(rcvdsize/1024)
		sys.stdout.write('\033M')

			
	sys.stdout.write('\033D')		
	print 'Done!'
	f.close()
	s.close()
	 

def main():
	parser = argparse.ArgumentParser()
#	subparsers = parser.add_subparsers(help='Select mode')
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-s", "--server", help="Run as server", action="store_true")
	group.add_argument("-c", "--client", help="Run as client", action="store_true")
#	parser.add_argument("-u", "--UDP", help="Run in UDP mode")	#it's too late for perfection
	parser.add_argument("-a", "--address", help="Destination host (client mode)", default="127.0.0.1")
	parser.add_argument("-p", "--port", type=int, help="Port to listen/connect to", default=12345)
	parser.add_argument("-f", "--file", help="File to send (server mode)", default="send.file")
	args = parser.parse_args()
	if args.server:
		print 'Server mode'
		run_server(args.address, args.port, args.file)
	if args.client:
		print 'Client mode'
		run_client(args.address, args.port)

if __name__ == '__main__':
        main()
