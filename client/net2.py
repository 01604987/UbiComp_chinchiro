import socket
import errno
from select import select
from struct import pack, unpack


class Client:

    def __init__(self, ip, port) -> None:
        self.server_ip = ip
        self.server_tcp_port = port
        self.client_tcp = None
        self.client_udp = None

    def init_tcp(self):
        self.client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_tcp.setblocking(False)
    
    def init_udp(self):
        self.client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_udp.setblocking(False)
        try:
            self.client_udp.bind(('192.168.1.11', self.server_tcp_port + 1))
        except OSError as err:
            if err.errno == errno.EADDRINUSE:
                pass
            else:
                raise
    def deinit_tcp(self):
        if self.client_tcp:
            self.client_tcp.close()

    def deinit_udp(self):
        self.client_udp.close()

    def connect_tcp(self):
        if self.client_tcp:
            try:
                self.client_tcp.connect((self.server_ip, self.server_tcp_port))
            except OSError as err:
                if err.errno == errno.EINPROGRESS:
                    print("Awaiting connection", err)
                    pass
                else:
                    print(str(err))
                    raise

    def establish_tcp(self):
 
        try:
            # receive will raise OSError if server socket not open
            data = self.receive_tcp_data(1)
            if not data:
                return 0
            print(data)
            self.send_tcp_data(10)
            return 1
        except OSError as err:
            print("in socket rec", err)
            if err.errno == errno.ECONNRESET or err.errno == errno.ECONNABORTED:
                self.deinit_tcp()
                self.init_tcp()
                self.connect_tcp()
                return 0
            raise
            
              
    # data is number from 0 to 666    
    def send_tcp_data(self, data):
        try:
            self.client_tcp.sendall(data.to_bytes(2, 'big'))
            print('Sent: ', data)
        except OSError as e:
            print("Error sending TCP", e)
        
    # data is number from 0 to 666
    def receive_tcp_data(self, est = None):
        
        ready_to_read, _, _ = select([self.client_tcp], [], [], 1)

        if not ready_to_read and not est:
            return 0

        try:
            data = self.client_tcp.recv(2)
        except OSError as err:
            if err.args[0] == errno.EAGAIN:
                print(str(err))
                return 0
            else:
                print("Error receiving TCP", err)
                raise
        if data:
            data = int.from_bytes(data, 'big')
            print('Received: ', data)
        return data


    def send_udp_shake(self, max_val, axis):
        data = pack('>hB', max_val, axis)
        try:
            # sending 2 bytes for max_val and 1 byte for axis (smallest represntable data size)
            self.client_udp.sendto(data, (self.server_ip, self.server_tcp_port + 1))
        except OSError as e:
            print(e)
            raise
    
    def receive_udp_shake(self):
        try:
            data = self.client_udp.recv(3)
            if data:
                max_val, axis = unpack('>hB', data)
            
                return (max_val, axis)
            return None
        except OSError as err:
            if err.errno == errno.EAGAIN:
                return None
