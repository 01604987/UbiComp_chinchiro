try:
  import usocket as socket
except:
  import socket
import network
import json

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = "donaublick"
password = "Wowasako3807vuyubehe"

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print("Connection successful")
print(station.ifconfig())



