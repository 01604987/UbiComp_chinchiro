from machine import Pin, I2C
from hcsr04 import HCSR04
import time



distance = HCSR04(trigger_pin = 0, echo_pin = 16)




while True:
    i = I2C(scl=Pin(12), sda=Pin(13), freq = 100000)
    
    distance.trigger = Pin(0, Pin.OUT)
    distance.trigger.value(0)
    print(distance.distance_cm())
    time.sleep(0.01)