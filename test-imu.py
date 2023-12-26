import gc
from micropython import mem_info
from machine import Pin, I2C
from mpu6050 import accel


i = I2C(scl=Pin(5), sda=Pin(4), freq = 10000)
print(i)
a = accel(i)
mem_info()

interval = 5000

x = 0
last_x = 0

last_x = a.get_values()['AcX']
counter=0
while True:
    counter +=1
    if not counter % 50 :
        mem_info()
    x = a.get_values()['AcX']
    if last_x > 0 and x > 0:
        continue
    if last_x < 0 and x < 0:
        continue
    
    if x < interval and x > -interval:
        continue
    
    print(f"last: {last_x}, curr: {x}")
    last_x = x
    
    
