# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import os, machine, time, network
#os.dupterm(None, 1) # disable REPL on UART(0)
# reattach usb repl
uart = machine.UART(0, 115200)
os.dupterm(uart, 1)
import gc
import webrepl

_IP = '192.168.1.10'

def do_connect():
    
    # WiFi SSID and Password
    wifi_ssid = "TP-Link_2.4Ghz"             # YOUR WiFi SSID
    wifi_password = "jkv777kim"     # YOUR WiFi PASSWORD

    # Wireless config : Station mode
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.ifconfig((_IP, '255.255.255.0', '192.168.1.1', '8.8.8.8'))


    # Continually try to connect to WiFi access point
    while not station.isconnected():
    
        # Try to connect to WiFi access point
        print("Connecting...")
        station.connect(wifi_ssid, wifi_password)
        time.sleep(10)

    # Display connection details
    print("Connected!")
    print("My IP Address:", station.ifconfig()[0])
    


do_connect()
webrepl.start()
machine.freq(160000000)

gc.collect()


