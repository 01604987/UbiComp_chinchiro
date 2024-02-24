from net2 import Client
from connection import Connection
import time
import random


ip = '192.168.1.99'
server_ip = '192.168.1.10'
server_port = 5002

ssid = "TP-Link_2.4Ghz"
password = "jkv777kim"

conn = Connection(ip, ssid, password)
conn.init()
conn.connect()
print(conn.net.ifconfig())

import socket
from time import sleep
netw = Client(conn.net.ifconfig()[0],server_ip, server_port)
netw.init_tcp()

netw.connect_tcp()
time.sleep(1)

def roll_1():
    # random 3 numbers
    counter = 1
    while True:
        rand = random.getrandbits(4)

        if rand < 12:
            die_1 = rand % 6 + 1
            counter += 1
        if counter > 1:
            break
    
    # check if numbers clears table
    
    return die_1

def _establish_start(netw):
    while True:
        my_num = roll_1()
        my_num = 1
        # show my num on led left in blue
        print(f"my rolled num: {my_num}")
        netw.send_tcp_data(my_num)
        print("data sent")
        while not (op_num := netw.receive_tcp_data()):
            print("awaiting response")
            sleep(1)
            
        print(f"op rolled num: {op_num}")
        # show op num on led right in red

        # sleep 0.5

        if my_num > op_num:
            # blink left
            return 1
        elif my_num < op_num:
            # blink right
            return 0

while not (res := netw.establish_tcp()) :
    netw.connect_tcp()    
    time.sleep(1)

turn = _establish_start(netw)
print("My Turn" if turn else "Op Turn")

#netw.deinit_tcp()

netw.init_udp()

last_data = time.ticks_ms()
print(last_data)
result = None
print(netw.client_udp)
while True:
    data = netw.receive_udp_data()
    if data is not None:
        last_data = time.ticks_ms()
        # play sound from data etc...
        print(data)
    time.sleep(0.01)
    if time.ticks_ms() - last_data >= 3000:
        print("checking tcp")
        last_data = time.ticks_ms()
        result = netw.receive_tcp_data()
        
        if result:
            break

print(result)
        
    # poll udp socket
    # if for longer than 2 sec no udp socket, we poll tcp socket
    # if tcp socket contains a number ->
    # check what number does ->
    # if not end -> process that number eg print
    # 
