import socket
import select
import sys
import os

from spolkslib import rtwork, filework
from content_table import *

__TCP_BUF_SIZE = 65536
__UDP_BUF_SIZE = 32768


def __tcp_server_routine(server, verbosity=False):

    connTable = ConnTable()

    while True:
        open_connections = connTable.values()
        rtr, rtw, ie = select.select(open_connections + [server], [],
        open_connections)

        for s in rtr:
            if s == server:
                conn, addr = server.accept()
                print "connected by {0}".format(addr)
                connTable.add(conn, addr)
                continue

            receive_data = False
            conn = connTable.get(s)
            if verbosity and conn.socket in ie:
                receive_data = True
                urg = s.recv(__TCP_BUF_SIZE, socket.MSG_OOB)
                print "{0} from {1} bytes recieved".format(conn.data_length,
                conn.addr)

            if conn.socket in rtr or receive_data:
                receive_data = False
                data = rtwork.recieve(s, __TCP_BUF_SIZE)
                if not data:
                    print '{0} disconnected'.format(conn.addr)
                    connTable.remove(s)
                    conn.fin = True
                    del conn
                    continue

                conn.f.write(data)
            else:
                continue
            conn.data_length += len(data)

    return True


def __udp_server_routine(server):

    connTable = ConnTable()

    while True:
        rtr, rtw, ie = select.select([server], [], [])
        if server in rtr:
            data, client = rtwork.recieve_from(server, __UDP_BUF_SIZE)

            if not connTable.get_addr(client):
                print 'connected by {0}'.format(client)
                connTable.add(None, client, False)

            conn = connTable.get_addr(client)

            if data == "FIN":
                print '{0} disconnected'.format(conn.addr)
                conn.fin = True
                connTable.remove_addr(client)
                del conn
            else:
                conn.f.write(data)
                rtwork.transmit_to(server, "ACK", client)

    return True


tcp_server = __tcp_server_routine
tcp_server_urg = lambda s: __tcp_server_routine(s, True)
udp_server = __udp_server_routine
