import socket
import errno


# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the socket to non-blocking mode
server_socket.setblocking(False)

# Bind the socket to the address and port
server_socket.bind(("192.168.1.10", 5000))


class Server:
    
    def __init__(self, ip, port) -> None:
        self.server_ip = ip
        self.server_port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None

    def init_tcp(self):
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the socket to non-blocking mode
        self.server_socket.setblocking(False)
        
        # Bind the socket to the address and port
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(1)

    def deinit_tcp(self):
        self.server_socket.close()
        

    def accept_conn(self):
        if self.server_socket:
            try:
                self.client_socket, self.client_address = self.server_socket.accept()
                return 1
            except OSError as err:
                if err.errno != errno.EAGAIN:
                    raise
                return 0
        else:
            print("No socket open")
        
        

class Client:

    def __init__(self, ip, port) -> None:
        self.server_ip = ip
        self.server_port = port
        self.server_socket = None

    def init_tcp(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(False)
        