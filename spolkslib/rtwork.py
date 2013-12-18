def __transmit(s, buffer, addr=None):

    try:
        buffer_size = len(buffer)

        if not addr:
            socket_send = s.send
        else:
            socket_send = lambda buf: s.sendto(buf, addr)

        bytes_sended = socket_send(buffer)
        while (bytes_sended < buffer_size):
            buffer = buffer[bytes_sended:]
            buffer_size = len(buffer)
            bytes_sended = socket_send(buffer)

        return True

    except Exception as e:
        print ("send buffer error %s" % e)
        return False


def __recieve(s, buf_size, isTcp=True):

    buffer, readed = '', 0
    try:
        while (True):
            if readed == buf_size:
                break
            if isTcp:
                chunk = s.recv(buf_size - readed)
            else:
                (chunk, addr) = s.recvfrom(buf_size - readed)
                buffer += chunk
                return buffer

            if not chunk:
                break

            readed += len(chunk)
            buffer += chunk

    except Exception as e:
        print ("recieve buffer error %s" % e)
    finally:
        if isTcp:
            return buffer
        else:
            return (buffer, addr)


def recieve(s, buf_size):

    return __recieve(s, buf_size)


def recieve_from(s, buf_size):

    return __recieve(s, buf_size, False)


def transmit(s, buffer):

    return __transmit(s, buffer)


def transmit_to(s, buffer, addr):

    return __transmit(s, buffer, addr)
