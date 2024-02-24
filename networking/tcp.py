import network
from time import sleep
import errno
import select

ssid = "TP-Link_2.4Ghz"
password = "jkv777kim"

sta_if = None

def connect_to_wifi():
    global sta_if
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.ifconfig(('192.168.1.99', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
    sta_if.connect(ssid, password)

    while not sta_if.isconnected():
        sleep(1)

    print("Connected to WiFi")
    print(sta_if.ifconfig())

# Versuche, eine Verbindung zum WiFi herzustellen
connect_to_wifi()
import socket
from time import sleep
import select

IP = '192.168.1.10'
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setblocking(False)
#tcp_socket.connect((IP, 5000))


counter = 0

while False:
    try:
        counter = counter +1 
        tcp_socket.connect((IP, 5002))
    except OSError as err:
        if err.errno in (errno.EINPROGRESS, errno.EBADF):
            print(counter, "Awaiting connection", err)
            time.sleep(1)
            if counter >= 10:
                tcp_socket.close()
                counter = 0
            continue  # Continue the loop to retry the connection
        elif err.errno == 106 or err.errno == errno.EALREADY:  # Check for error code 106
            print("Connection established", err)
            break  # Exit the loop as connection is successful
        else:
            print(f"Error: {err}")
            raise
        


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
        

conn(tcp_socket, IP)



data = 0
tcp_socket.send(b'')
while True:
    try:
        data = tcp_socket.recv(2)
        break
    except OSError as err:
        print(str(err))
        if err.errno in (errno.ECONNABORTED,errno.ECONNRESET, errno.EBADF):
            tcp_socket.close()
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.setblocking(False)
            time.sleep(1)
            conn(tcp_socket, IP)
        time.sleep(2)

print(data)


num = 6
try:
    data = num.to_bytes(2, 'big')
    tcp_socket.sendall(data)
except OSError as e:
    tcp_socket.close()
    print("Error sending TCP", e)

resp = None
while True:
    try:
        resp = tcp_socket.recv(2)
        print(resp)
        if resp:
            break
    except OSError as err:
        if err.args[0] == errno.EAGAIN:
            pass
        else:
            tcp_socket.close()
            print("Error receiving TCP", err)
            break
if resp:
    data = int.from_bytes(resp, 'big')
    print("Received data:", data)
else:
    print("No data received")

tcp_socket.close()
        

