import sys
import os
import select
import socket

from spolkslib import filework, rtwork

__TCP_BUF_SIZE = 65536
__UDP_BUF_SIZE = 32768


def __tcp_client_routine(conn, filename, verbosity=False):

    f = open(filename, 'rb')
    f_size = filework.get_fsize(f)
    __URG_PERIOD = int(f_size) / __TCP_BUF_SIZE / 10 * __TCP_BUF_SIZE
    bytes_sended = 0

    while True:
        if verbosity and bytes_sended % __URG_PERIOD == 0:
            conn.send('!', socket.MSG_OOB)
            print ("%s bytes sended" % bytes_sended)

        buffer = f.read(__TCP_BUF_SIZE)
        rtr, rtw, ie = select.select([], [conn], [], 10.0)

        if conn in rtw:
            success = rtwork.transmit(conn, buffer)
        else:
            break

        if bytes_sended == f_size or not success:
            break

        bytes_sended += len(buffer)

    conn.close()
    f.close()


def __udp_client_routine(client, filename, host, port):

    server = (host, port)
    f = open(filename, 'rb')
    f_size = filework.get_fsize(f)
    bytes_sended = 0

    while True:
        buffer = f.read(__UDP_BUF_SIZE)
        __resend_until_ack(client, buffer, server)

        if bytes_sended == f_size:
            rtwork.transmit_to(client, "FIN", server)
            break

        bytes_sended += len(buffer)

    client.close()
    f.close()


def __resend_until_ack(client, buffer, server):

    send_again = False
    while True:
        rtwork.transmit_to(client, buffer, server)
        while True:
            rtr, rtw, ie = select.select([client], [], [], 10.0)
            addr = None
            if client in rtr:
                ack, addr = rtwork.recieve_from(client, 3)

            if not addr:
                raise Exception("server is off-line")
            if addr == server:
                if ack == "ACK":
                    return True
                elif send_again:
                    raise Exception("server disconnected")
                else:
                    send_again = True
                    break


tcp_client = __tcp_client_routine
tcp_client_urg = lambda conn, filename: __tcp_client_routine(conn,
filename, True)
udp_client = __udp_client_routine
