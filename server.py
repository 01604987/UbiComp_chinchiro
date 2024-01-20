import socket
from time import sleep

# Startet den TCP Server
IP2 = "192.168.1.91"
server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tcp_socket.bind(('', 8080))  # Bindet den Server an Port 80
server_tcp_socket.listen(1)
print("tcp socket gestartet auf Port 8080...")
print("Warte auf eine Verbindung...")
client_tcp_socket, addr = server_tcp_socket.accept()
print("Verbindung von", addr)
# Startet den UDP Server
server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_udp_socket.bind(('', 8081))


def send_tcp_data():
  try:
    response = "TCP Nachricht empfangen"
    client_tcp_socket.send(response.encode('utf-8'))
  except Exception as e:
    print("Fehler bei der Handhabung der TCP-Anfrage:", e)

def recieve_tcp_data():
  try:
    tcp_message = client_tcp_socket.recv(1024).decode('utf-8')
    print("TCP Empfangene Nachricht:", tcp_message)
  except Exception as e:
    print("Fehler bei der Handhabung der TCP-Anfrage:", e)

def recieve_udp_data():
  udp_message, udp_addr = server_udp_socket.recvfrom(1024)  # Puffergröße ist 1024 Bytes
  print(f"Nachricht von {udp_addr}: {udp_message.decode()}")
  return udp_message, udp_addr

def send_udp_data(message, udp_addr):
  server_udp_socket.sendto(message.encode(), udp_addr)

 
while True:
  recieve_tcp_data()
  send_tcp_data()
  sleep(1)
  udp_data, udp_addr = recieve_udp_data()
  send_udp_data(udp_data.decode(), udp_addr)
  sleep(1)
  




