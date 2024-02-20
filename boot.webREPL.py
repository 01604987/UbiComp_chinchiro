# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import os, machine, time, net
os.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl

_IP = '192.168.1.10'
def do_connect():
    
    # WiFi SSID and Password
    wifi_ssid = None         # YOUR WiFi SSID
    wifi_password = None     # YOUR WiFi PASSWORD

    # Wireless config : Station mode
    station = net.WLAN(net.STA_IF)
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
    


do_connect(_IP)
webrepl.start()
# set cpu to 160mhz
machine.freq(160000000)
gc.collect()

