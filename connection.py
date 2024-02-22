import network
from micropython import const

class Connection:
    def __init__(self, ip, ssid, password) -> None:
        self.ip = const(ip)
        self.ssid = const(ssid)
        self.password = const(password)
        self.net = None

    def init(self):
        if not self.net:
            self.net = network.WLAN(network.STA_IF)

        if not self.net.isconnected():
        
            self.net.active(True)
            self.net.ifconfig((self.ip, '255.255.255.0', '192.168.1.1', '8.8.8.8'))

    def deinit(self):
        if self.net:
            self.net.disconnect()
            self.net = None
        
    def connect(self):
        if not self.net.isconnected():
            self.net.connect(self.ssid, self.password)
            return 0
        else: 
            return 1

        