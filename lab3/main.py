#!/usr/bin/python			#spolks lab3 main.py
#A simple client-server app for file transmit via TCP.

import sys
import socket
import argparse

BUF_SIZE = 1024


def run_server(port, filename):
	
	if 0 <= port <= 65535:
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('',port))
		s.listen(1)
		conn, addr = s.accept()
		print 'Got connection from', addr
	else: return 0
	
	f = open(filename, 'rb')
	while True:
		data = f.read(BUF_SIZE)
		if not data:
			print 'Data has been transfered'
			break
		try:
			conn.send(data)
		except socket.error:
			print 'Transfer failed'
			sys.exit
	f.close()
	conn.close()
	
	
def run_client(host, port):
	if 0 <= port <= 65535:
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
#		host = socket.gethostname()
		s.connect((host,port))
	else:
		print 'Port # must be in range 0-65535'
		return
	
	f = open('rcvd.file','wb')
	
	while True:
		data = s.recv(BUF_SIZE)
		if not data:
			break
		f.write(data)
			
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
