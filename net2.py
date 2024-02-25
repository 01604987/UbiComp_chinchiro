import socket
import errno

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
            self.client_udp.bind(('192.168.1.99', self.server_tcp_port + 1))
        except OSError as err:
            if err.errno == errno.EADDRINUSE:
                pass
            else:
                raise
    def deinit_tcp(self):
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
            while not (data:= self.receive_tcp_data()):
                pass
            print(data)
            
            if data == 10:
                print('connected')
            self.send_tcp_data(10)
            return 1
        except OSError as err:
            #print("in socket rec", err)
            if err.errno == errno.ECONNRESET:
                self.deinit_tcp()
                self.init_tcp()
                return 0
            raise
            
              
    # data is number from 0 to 666    
    def send_tcp_data(self, data):
        try:
            data = data.to_bytes(2, 'big')
            self.client_tcp.sendall(data)
        except OSError as e:
            print("Error sending TCP", e)
            #self.deinit_tcp()
        
    # data is number from 0 to 666
    def receive_tcp_data(self):
        try:
            data = self.client_tcp.recv(2)
        except OSError as err:
            if err.args[0] == errno.EAGAIN:
                return 0
            else:
                print("Error receiving TCP", err)
                raise
        if data:
            data = int.from_bytes(data, 'big')
        return data

    def send_udp_data(self, data):
        return

    def receive_udp_data(self):
        try:
            data = self.client_udp.recv(2)
            return data
        except OSError as err:
            if err.errno == errno.EAGAIN:
                return None

    def send_udp_data(self, data):
        data = data.to_bytes(2, 'big')
        try:
            # Attempt to send data to the UDP socket
            self.client_udp.sendto(data, (self.server_ip, self.server_tcp_port + 1))
            
        except OSError as e:
            print(e)
            raise
