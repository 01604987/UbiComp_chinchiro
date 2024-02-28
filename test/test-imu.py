import gc
from micropython import mem_info
from machine import Pin, I2C
from mpu6050 import accel
import time

i = I2C(scl=Pin(12), sda=Pin(13), freq = 100000)
print(i)
a = accel(i)
mem_info()

default_interval = 10000

x = 0
last_x = 0

# [[current val, last val, interval, max val], ...]
values = [[0,0,default_interval, 0],[0,0,default_interval, 0],[0,0,default_interval, 0]]
max_set = 0
def acc(accel, values):
    raw = accel.get_values()
    axis = [0,0,0]
    axis[0] = raw[0]
    axis[1] = raw[1]
    axis[2] = raw[2] - 19000
    
    
    
    for index, val in enumerate(values):
        
        #if abs(axis[index]) > 500:            
            # copy current value to last value
            val[1] = val[0]
            # update current value with new value
            val[0] = axis[index]
        


def calculate_interval(axis ,values, default_interval):
    if axis == None:
        for val in values:
            val[2] = default_interval
            #print("resetting interval for all")
        return
    
    for index, val in enumerate(values):
        if index == axis:
            continue
        val[2] = abs(values[axis][0]) + default_interval

# return x, y, z or no axis
def detect_axis(values, default_interval):
    for index, val in enumerate(values):
        # value smaller than interval
        if abs(val[0]) < val[2]:
            continue
        else:
            return index
    return None

def max_val(values, axis):
    if axis == None:
        return
    
    if abs(values[axis][3]) < abs(values[axis][0]):
        values[axis][3] = values[axis][0]

counter = 0
while True:
    # poll accel values
    acc(a, values)
    # detect axis being shaken
    axis = detect_axis(values, default_interval)
    # recalculate interval for other axis
    calculate_interval(axis, values, default_interval)
    max_val(values, axis)
    #max_set = max_val(values, axis)
    #print(values[2])
    #continue
    #print(values[1])

    if axis == None:
        #print(values)
        continue
    
    #print(values[0])
    
    if values[axis][3] / values[axis][1] <= 0:
        print(axis)
        print(values)
        values[axis][3] = 0
        time.sleep(0.01)
        continue
    
    if values[axis][1] > 0 and values[axis][0] > 0:
        continue
    if values[axis][1] < 0 and values[axis][0] < 0:
        continue
