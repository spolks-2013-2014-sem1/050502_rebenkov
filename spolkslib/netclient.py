import socket
import sys


def __client_socket_create(isTcp=True):

    if isTcp:
        sock_type = socket.SOCK_STREAM
    else:
        sock_type = socket.SOCK_DGRAM

    s = socket.socket(socket.AF_INET, sock_type)
    return s


def __make_client(host, port, action, a_args, isTcp=True):

    try:
        client_socket = __client_socket_create(isTcp)
        if isTcp:
            client_socket.connect((host, port))

        action(client_socket, *a_args)

    except KeyboardInterrupt as e:
        print 'keyboard interrupt detected.\nterminate.'
    except socket.error as e:
        print 'socket error {0}'.format(e)
    except IOError as e:
        print 'can\'t open file.\nterminate'
    except Exception as e:
        print 'exception occured: {0}.\nterminate.'.format(e)
    finally:
        if client_socket != None:
            client_socket.close()

        sys.exit(0)


def run_tcp_client(host, port, action, a_args=()):

    return __make_client(host, port, action, a_args)


def run_udp_client(host, port, action, a_args=()):

    return __make_client(host, port, action, a_args, False)
