# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import os, machine, time, network
os.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl


def do_connect():
    
    # WiFi SSID and Password
    wifi_ssid = None         # YOUR WiFi SSID
    wifi_password = None     # YOUR WiFi PASSWORD

    # Wireless config : Station mode
    station = network.WLAN(network.STA_IF)
    station.active(True)

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
# set cpu to 160mhz
machine.freq(160000000)
gc.collect()

