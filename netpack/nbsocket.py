import sys, socket

class Nbsocket():
    ''' A wrapper for a non-blocking TCP socket. It requires that the first 5 bytes 
        contain the total size of the data being sent.
    '''
    HEADER_WIDTH = 5
    def __init__(self, **kwargs):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.HEADER_WIDTH = 5
    def connect(self, host, port):
        self.sock.connect((host,port))
        self.sock.setblocking(0)
    def socket(self):
        return self.sock
    def send(self, bytedata):
        return self.sock.send(bytedata)
    def recv1(self, buffersize, whatsleft):
        '''Call this function if your implementation sends the size of data in
            first 5 bytes'''
        temp = self.sock.recv(buffersize)
        datasize = int.from_bytes(temp[:5],byteorder=sys.byteorder)
        return (temp[5:], datasize - len(temp))
    def recv2(self, buffersize, whatsleft):
        '''Call this function after recv1 if there more data to be received '''
        temp = self.sock.recv(buffersize)
        return (temp, whatsleft - len(temp))
    def close(self):
        self.sock.close()

def encapdata(data=None, headerwidth=5, byteorder=sys.byteorder):
    '''adds the size of the data as a header with a width of headerwidth bytes'''
    header = (len(data)+headerwidth).to_bytes(headerwidth,byteorder)
    packet = b''.join([header,data])
    return packet