import network
from time import sleep

ssid = "donaublick"
password = "Wowasako3807vuyubehe"

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)

    while not sta_if.isconnected():
        sleep(1)

    print("Connected to WiFi")
    print(sta_if.ifconfig())

# Versuche, eine Verbindung zum WiFi herzustellen
connect_to_wifi()


