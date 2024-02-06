from lib.mpu6050 import accel
from machine import I2C
import time

class Shake:

    def __init__(self, scl, sda, freq=100000) -> None:

        self.scl = scl
        self.sda = sda
        self.freq = freq

        self.i2c = None
        self.imu = None

        self.default_interval = 10000
        # init: [[current val, last val, interval, max val], ...]
        self.values = [[-1,-1,self.default_interval, -1],[-1,-1,self.default_interval, -1],[-1,-1,self.default_interval, -1]]
        self.axis = None
        self.max_set = 0
        
    def deinitialize(self) -> None:
        self.imu.sleep()
        self.i2c = None
        self.imu = None
        
    def initialize_module(self) -> None:
        try:
            self.i2c = I2C(scl = self.scl, sda = self.sda, freq = self.freq)
        except Exception as err:
            print(f"Error during i2c initialization with err code {str(err)}")
        
        try:
            self.imu = accel(self.i2c)
        except Exception as err:
            print(f"Error during imu initialization with err code {str(err)}")


    def get_axis(self):
        return self.axis

    def reset_values(self):
        self.values = [[-1,-1,self.default_interval, -1],[-1,-1,self.default_interval, -1],[-1,-1,self.default_interval, -1]]
        self.max_set = 0
    
    def update(self):
        raw = self.imu.get_values()
        accel = [0,0,0]
        accel[0] = raw['AcX']
        accel[1] = raw['AcY']
        # because gravity pulls down the z axis
        accel[2] = raw['AcZ'] - 19000

        for index, val in enumerate(self.values):
            # copy current value to last value
            val[1] = val[0]
            # update current value with new value
            val[0] = accel[index]

        self.axis = self._detect_axis()
        self._calculate_interval()
        self._set_max_val()

    def _calculate_interval(self):
        if self.axis == None:
            # reset all intervals to default
            for val in self.values:
                val[2] = self.default_interval
            return
        
        for index, val in enumerate(self.values):
            if index == self.axis:
                continue
            val[2] = abs(self.values[self.axis][0]) + self.default_interval

    # return x(0), y(1), z(2) or no axis
    def _detect_axis(self):
        for index, val in enumerate(self.values):
            # value larger than interval then return this axis
            if abs(val[0]) > val[2]:
                return index
        return None
    
    def _set_max_val(self):
        if self.axis == None:
            return
        
        if abs(self.values[self.axis][3]) < abs(self.values[self.axis][1]):
            self.values[self.axis][3] = self.values[self.axis][1]
