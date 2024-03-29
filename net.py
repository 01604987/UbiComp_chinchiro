import socket
import errno
from select import select
from micropython import const
from struct import pack, unpack

###################################################################
############### TCP CODES ################
##########################################

# 10 connection established
# 11 message ack
# 12 turn end
# 13 calculate result
# 14 game end
# 16 shake end
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
            self.client_tcp.sendall(data.to_bytes(2, 'big'))
            print('Sent: ', data)
        except Exception as e:
            print("Error sending TCP", e)
        
    # data is number from 0 to 666
    def receive_tcp_data(self):

        ready_to_read, _, _ = select([self.client_tcp], [], [], 1)

        if not ready_to_read:
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
            # Attempt to send data to the UDP socket
            self.server_udp.sendto(data, (self.client_tcp_address[0], self.server_tcp_port + 1))
            
        except OSError as e:
            print(e)
            raise

    
    def receive_udp_shake(self):
        try:
            data = self.server_udp.recv(3)
            if data:
                max_val, axis = unpack('>hB', data)
            
                return (max_val, axis)
            return None
        except OSError as err:
            if err.errno == errno.EAGAIN:
                return None

