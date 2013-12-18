import socket
import select
import sys
import os
import time
import threading

from threading import Lock, Thread
from spolkslib import rtwork, filework

__TCP_BUF_SIZE = 65536
__UDP_BUF_SIZE = 32768 + 32


def __tcp_server_thread(conn, addr, verbosity):

    data_length = 0
    print "connected by", addr
    filename = filework.random_name()
    f = open(filename, 'wb')

    while True:
        rtr, rtw, ie = select.select([conn], [], [conn], 10.0)
        if conn in ie and verbosity == True:
            urg = conn.recv(__TCP_BUF_SIZE, socket.MSG_OOB)
            data = rtwork.recieve(conn, __TCP_BUF_SIZE)
            f.write(data)
            print "{0} bytes recieved from {1}".format(data_length, addr)

        elif conn in rtr:
            data = rtwork.recieve(conn, __TCP_BUF_SIZE)
            if not data:
                break
            f.write(data)
        else:
            break

        data_length += len(data)

    f.close()
    conn.close()
    print '{0} disconnected'.format(addr)

    return True


def __tcp_server_routine(server, verbosity=False):

    conn, addr = server.accept()
    t = Thread(target=__tcp_server_thread, args=(conn, addr, verbosity))
    t.daemon = True
    t.start()

    return True


class Connection(object):

    def __init__(self, addr, packets):

        print "connected by {0}".format(addr)
        self.addr = addr
        self.packets = packets
        self.filename = filework.random_name()
        self.f = open(self.filename, 'wb')
        self.mutex = Lock()

    def __del__(self):

        if self.packets > 0:
            print "{0} aborted connection\nerase {1}.".format(self.addr,
            self.filename)
            os.remove(self.filename)
        else:
            self.f.close()


__filename_addr = {}
except_trap = True


def __udp_server_thread(server):

    global __filename_addr
    mutex = Lock()
    while except_trap:
        mutex.acquire()
        try:
            rtr, rtw, ie = select.select([server], [], [])
            if server in rtr:
                data, client = rtwork.recieve_from(server, __UDP_BUF_SIZE)

            if not client in __filename_addr:
                packets = int(data[:16])
                __filename_addr[client] = Connection(client, packets)

            conn = __filename_addr[client]
            seek = int(data[16:32])
            data = data[32:]

        finally:
            mutex.release()

        conn.mutex.acquire()
        try:

            conn.f.seek(seek, 0)
            conn.f.write(data)
            conn.packets -= 1
            rtwork.transmit_to(server, "ACK", client)

        finally:
            conn.mutex.release()

        if conn.packets == 0:
            print "{0} disconnected.".format(client)
            del __filename_addr[client]
            del conn


def __udp_server_routine(server, count=7):

    global except_trap
    try:
        for i in range(0, count):
            t = Thread(target=__udp_server_thread, args=(server,))
            t.daemon = True
            t.start()
        while threading.active_count() > 0:
            time.sleep(0.1)
    except KeyboardInterrupt as e:
        except_trap = False
        raise e


tcp_server = __tcp_server_routine
tcp_server_urg = lambda s: __tcp_server_routine(s, True)
udp_server = __udp_server_routine
