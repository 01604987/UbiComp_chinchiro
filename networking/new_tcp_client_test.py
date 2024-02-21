import socket

import network
from time import sleep
import errno
import select

ssid = ""
password = ""

# Define server IP and port
SERVER_IP = "192.168.1.10"
SERVER_PORT = 5002

# Function to connect to WiFi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print(wlan.ifconfig())

connect_to_wifi()

import socket
from time import sleep
import select

IP = '192.168.1.10'
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setblocking(False)

def conn(tcp_socket, IP):
    try:
        tcp_socket.connect((IP, 5002))
    except OSError as err:
        if err.errno == errno.EINPROGRESS:
            print("Awaiting connection", err)
            pass
        else:
            print(str(err))
            raise
        
def rec():
    try:
        resp = tcp_socket.recv(2)
        print(resp)
        if resp:
            return
    except OSError as err:
        if err.args[0] == errno.EAGAIN:
            print("again")
            pass
        else:
            tcp_socket.close()
            print("Error receiving TCP", err)
            return
        
def receive_tcp_data(tcp_socket):
        try:
            data = tcp_socket.recv(2)
        except OSError as err:
            if err.args[0] == errno.EAGAIN:
                return 0
            else:
                print("Error receiving TCP", err)
                
                raise
        if data:
            data = int.from_bytes(data, 'big')
        print(data)
        return data


def send_tcp_data(tcp_socket, data):
    try:
        data = data.to_bytes(2, 'big')
        tcp_socket.sendall(data)
    except Exception as e:
        print("Error sending TCP", e)

#time.sleep(2)

while True:
    conn(tcp_socket, IP)
        
    time.sleep(1)
    
    try:
        resp = receive_tcp_data(tcp_socket)
        send_tcp_data(tcp_socket,1)
        break
    except OSError as err:
        print("in socket rec", err)
        if err.errno == errno.ECONNRESET:
            tcp_socket.close()
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.setblocking(False)
            continue
        
        
    time.sleep(1)



num = 6
try:
    data = num.to_bytes(2, 'big')
    tcp_socket.sendall(data)
except OSError as e:
    tcp_socket.close()
    print("Error sending TCP", e)

resp = None
while True:
    result = receive_tcp_data(tcp_socket)
    if result:
        break
    print("awaiting response")
    time.sleep(1)

tcp_socket.close()
