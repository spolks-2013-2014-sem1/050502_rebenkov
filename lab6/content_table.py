import sys
import os
from spolkslib import filework


class Connection(object):

    """class holding connection unit consisting
    of socket object, addres info, associated
    filename and file descriptor, and length of
    received data"""

    def __init__(self, socket, addr, fin=True):

        """initialize connection object
        filename generates randomly"""

        self.socket = socket
        self.addr = addr
        self.filename = filework.random_name()
        self.data_length = 0
        self.f = open(self.filename, 'wb')
        self.fin = fin

    def __del__(self):

        """destructor: called when number of
        pointers on object is equal to zero
        and closes socket and file descriptor"""

        if self.fin == True and self.socket:
            self.socket.close()
            self.f.close()

        elif self.fin == False:
            print "eof from {0} was not detected\nerase {1}".format(self.addr,
            self.filename)
            os.remove(self.filename)


class ConnTable(object):

    """connections table holds connection units
    described above"""

    def __init__(self):

        """inital table entry is empty"""

        self.table = []

    def add(self, socket, addr, fin=True):

        element = Connection(socket, addr, fin)
        self.table.append(element)

    def remove(self, socket):

        """removes connection from list and
        delete it"""

        conn = self.get(socket)
        del conn
        self.table = [el for el in self.table if el.socket != socket]

        return True

    def remove_addr(self, addr):

        conn = self.get_addr(addr)
        del conn
        self.table = [el for el in self.table if el.addr != addr]

        return True

    def get(self, socket):

        """return connection unit by socket"""

        for el in self.table:
            if socket == el.socket:
                return el
        else:
            return None

    def get_addr(self, addr):

        for el in self.table:
            if addr == el.addr:
                return el
        else:
            return None

    def values(self):

        """returns all sockets in table"""

        values = []
        for el in self.table:
            values.append(el.socket)

        return values

    def addrs(self):

        values = []
        for el in self.table:
            value.append(el.addr)

        return values
