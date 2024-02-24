import network
from micropython import const
from time import ticks_ms

class Connection:
    def __init__(self, ip, ssid, password) -> None:
        self.ip = const(ip)
        self.ssid = const(ssid)
        self.password = const(password)
        self.net = None
        self.conn_t = const(0)

    def init(self):
            self.net = network.WLAN(network.STA_IF)
            self.net.active(True)
            self.net.ifconfig((self.ip, '255.255.255.0', '192.168.1.1', '8.8.8.8'))

    def deinit(self):
        if self.net:
            self.net.disconnect()
            self.net = None
        
    def connect(self, threshold = 10000):
        if not self.net.isconnected():
            if ticks_ms() - self.conn_t > threshold:
                self.net.connect(self.ssid, self.password)
                self.conn_t = ticks_ms()
            return 0
        else:
            self.conn_t = 0
            return 1

        