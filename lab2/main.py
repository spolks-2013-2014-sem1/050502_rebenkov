#!/usr/bin/python			#spolks lab2 main.py
#A simple time server. Provides local time. Use CTRL+C to stop

import socket				#import socket module
from time import localtime, strftime	#import time module

s = socket.socket()			#create a socket object
port = 12345				#reserve a (random) port for server
s.bind(('',port))			#bind to the port
#using s.bind(('',port)) syntax instead of s.bind((socket.gethostname(),port))
#in purpose to reach server app from Virtualbox host OS
s.listen(5)				#now wait for client connection
while True:
	c, addr = s.accept()		#establish connection with client
	print 'Got connection from', addr
	c.send("Local time: ")
	c.send(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
	c.send("\n")
	
	c.close()			#close the connection
