import socket
import errno
from micropython import const

###################################################################
############### TCP CODES ################
##########################################

# 10 connection established
# 11 next try
# 12 turn end
# 13 game end
# 1 hit score
# 2 hit score
# 3 hit score
# 4 hit score
# 5 hit score
# 6 hit score
# 123 hit score
# 111 hit score
# 222 hit score
# 333 hit score
# 444 hit score
# 555 hit score
# 666 hit score


class Server:
    
    def __init__(self, ip, port) -> None:
        self.server_ip = const(ip)
        self.server_tcp_port = const(port)
        self.server_tcp = None
        self.server_udp = None
        self.client_tcp = None
        self.client_tcp_address = None
        self.connected_tcp = False

    def init_tcp(self):
        # Create a TCP/IP socket
        self.server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the socket to non-blocking mode
        self.server_tcp.setblocking(False)
        
        # Bind the socket to the address and port
        try:
            self.server_tcp.bind((self.server_ip, self.server_tcp_port))
        except OSError as err:
            if err.errno == errno.EADDRINUSE:
                pass
            else: raise
        self.server_tcp.listen(1)

    def init_udp(self):
        self.server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_udp.setblocking(False)
        try:
            self.server_udp.bind((self.server_ip, self.server_tcp_port + 1))
        except OSError as err:
            if err.errno == errno.EADDRINUSE:
                pass
            else:
                raise
    
    def deinit_udp(self):
        if self.server_udp:
            self.server_udp.close()
    
    def deinit_tcp(self):
        self.connected_tcp = False
        if self.client_tcp:
            self.client_tcp.close()
        self.client_tcp_address = None

        if self.server_tcp:
            self.server_tcp.close()
            

    def accept_conn(self):
        if self.server_tcp:
            try:
                # will raise OSError if unsuccessful
                self.client_tcp, self.client_tcp_address = self.server_tcp.accept()
                # connection established data
                self.send_tcp_data(10)
                while not (data:= self.receive_tcp_data()):
                    pass
                print(data)
                if data == 10:
                    self.connected_tcp = True
                return 1
            except OSError as err:
                if err.errno != errno.EAGAIN:
                    raise
                return 0
        else:
            print("No socket open")
          
    # data is number from 0 to 666    
    def send_tcp_data(self, data):
        try:
            data = data.to_bytes(2, 'big')
            self.client_tcp.sendall(data)
        except Exception as e:
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
        data = data.to_bytes(2, 'big')
        try:
            # Attempt to send data to the UDP socket
            self.server_udp.sendto(data, (self.client_tcp_address[0], self.server_tcp_port + 1))
            
        except OSError as e:
            print(e)
            raise

    def receive_udp_data(self):
        try:
            data = self.server_udp.recv(2)
            return data
        except OSError as err:
            if err.errno == errno.EAGAIN:
                return None

