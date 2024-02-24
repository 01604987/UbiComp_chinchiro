import socket
from time import sleep

# Startet den TCP Server
IP1 = "192.168.1.201"
server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tcp_socket.connect((IP1, 8080))
print("gestartet auf Port 8080...")

# UDP-Client initialisieren
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_tcp_data():
  try:
    data_to_send = 'data for you.'
    server_tcp_socket.send(data_to_send.encode('utf-8'))
  except Exception as e:
    print("Fehler bei der Bearbeitung der Anfrage:", e)

def receive_tcp_data():
  try:
    response = server_tcp_socket.recv(1024).decode('utf-8')
    print("Antwort vom Server:", response)
  except Exception as e:
    print("Fehler bei der Bearbeitung der Anfrage:", e)
    
def send_udp_data():
  try:
      data_to_send = 'UDP-Daten für Sie.'
      udp_socket.sendto(data_to_send.encode('utf-8'), (IP1, 8081))
  except Exception as e:
      print("Fehler beim Senden von UDP-Daten:", e)

def receive_udp_data():
  try:
      data, addr = udp_socket.recvfrom(1024)
      print(f"Antwort vom UDP-Server {addr}: {data.decode()}")
  except Exception as e:
      print("Fehler beim Empfangen von UDP-Daten:", e)


while True:  
  send_tcp_data() 
  receive_tcp_data()
  sleep(1)
  send_udp_data()
  receive_udp_data()
  sleep(1)


