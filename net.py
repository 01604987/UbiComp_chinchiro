import socket
import errno

class Server:
    
    def __init__(self, ip, port) -> None:
        self.server_ip = ip
        self.server_port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.connected = False

    def init_tcp(self):
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the socket to non-blocking mode
        self.server_socket.setblocking(False)
        
        # Bind the socket to the address and port
        try:
            self.server_socket.bind((self.server_ip, self.server_port))
        except OSError as err:
            if err.errno == errno.EADDRINUSE:
                pass
            else: raise
        self.server_socket.listen(1)

    def deinit_tcp(self):
        self.connected = False
        self.client_socket.close()
        self.server_socket.close()
        

    def accept_conn(self):
        if self.server_socket:
            try:
                # will raise OSError if unsuccessful
                self.client_socket, self.client_address = self.server_socket.accept()
                # connection established data
                self.send_tcp_data(1)
                while not (data:= self.receive_tcp_data()):
                    pass
                print(data)
                if data == 1:
                    self.connected = True
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
            self.client_socket.sendall(data)
        except Exception as e:
            print("Error sending TCP", e)
            #self.deinit_tcp()
        
    # data is number from 0 to 666
    def receive_tcp_data(self):
        try:
            data = self.client_socket.recv(2)
        except OSError as err:
            if err.args[0] == errno.EAGAIN:
                return 0
            else:
                print("Error receiving TCP", err)
                raise
        if data:
            data = int.from_bytes(data, 'big')
        return data

class Client:

    def __init__(self, ip, port) -> None:
        self.server_ip = ip
        self.server_port = port
        self.client_socket = None
        self.connected = False

    def init_tcp(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setblocking(False)

    def deinit_tcp(self):
        self.connected = False
        self.client_socket.close()

    def connect_tcp(self):
        if self.client_socket:
            try:
                self.client_socket.connect((self.server_ip, self.server_port))
            except OSError as err:
                if err.errno == errno.EINPROGRESS:
                    print("Awaiting connection", err)
                    pass
                else:
                    print(str(err))
                    raise

    def establish_tcp(self):
        # connect tcp here ?
 
        try:
            self.send_tcp_data(1)
            while not (data:= self.receive_tcp_data()):
                pass
            print(data)
            if data == 1:
                self.connected = True
            return 1
        except OSError as err:
            print("in socket rec", err)
            if err.errno == errno.ECONNRESET:
                self.deinit_tcp()
                self.init_tcp()
                return 0
            

              
    # data is number from 0 to 666    
    def send_tcp_data(self, data):
        try:
            data = data.to_bytes(2, 'big')
            self.client_socket.sendall(data)
        except Exception as e:
            print("Error sending TCP", e)
            #self.deinit_tcp()
        
    # data is number from 0 to 666
    def receive_tcp_data(self):
        try:
            data = self.client_socket.recv(2)
        except OSError as err:
            if err.args[0] == errno.EAGAIN:
                return 0
            else:
                print("Error receiving TCP", err)
                raise
        if data:
            data = int.from_bytes(data, 'big')
        return data
