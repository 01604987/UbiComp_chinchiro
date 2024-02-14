from machine import Pin
from micropython import const
import neopixel
import time
import uasyncio as asyncio


# all colors are 1/5 bright
#               "red",   "green",   "blue",    "yellow",   "purple", "turkoise"
LIGHTS = const(((64,0,0), (0,64,0), (0,0,64), (64,64,0), (64,0,64), (0,64,64)))

NUMS = [[], [3], [0, 6], [2, 3, 4], [0, 2, 4, 6], [0, 2, 3, 4, 6], [0, 1, 2, 4, 5, 6]]

class Led:

    def __init__(self, data, pixel_nr) -> None:
        self.pixel_nr = pixel_nr
        self.data = data
        self.data_pin = Pin(data)
        self.np = None
        self.sleep_time_ms = 1000
        self.number = [0,0,0]
        self.color = LIGHTS[0]
        

    
    def initialize(self) -> None:
        self.np = neopixel.NeoPixel(self.data_pin, self.pixel_nr)

    def reset(self) -> None:
        for index, val in enumerate(self.np):
            self.np[index] = (0,0,0)

    def light_up(self) -> None:
        self.np.write()

    def set_light(self, nr, color = None) -> None:
        if not color:
            self.np[nr] = LIGHTS[0]
        else:
            self.np[nr] = color

    def create_task(self):
        asyncio.create_task(self.start())

    def light_numbers(self, number):
        if not isinstance (number,list):
            print("number not a list")
            return
        if number[0] > 6:
            return
        
        self.reset()


        for i in NUMS[number[0]]:
            self.np[i] = self.color


        for i in NUMS[number[1]]:
            val = i + 1 * int(self.pixel_nr/3)
            self.np[val] = self.color

        for i in NUMS[number[2]]:
            val = i + 2 * int(self.pixel_nr/3)
            self.np[val] = self.color


        self.light_up()
            

    async def start(self) -> None:
        while True:
            print(0)
            await asyncio.sleep_ms(self.sleep_time_ms)
  


async def sleeper(led):
    while True:
        await asyncio.sleep(1)
        led.sleep_time_ms = led.sleep_time_ms - 100
        if led.sleep_time_ms <= 100:
            led.sleep_time_ms = 1000



pin = const(21)
nr = const(21)
led = Led(pin, nr)
led.initialize()

#led.light_numbers([6, 1, 5])

counter = 0
while True:
    led.set_light(counter % 8)
    led.light_up()
    time.sleep(0.001)
    led.set_light(counter % 8, (0,0,0))
    led.light_up
    time.sleep(0.001)
    counter += 1

#asyncio.create_task(sleeper(led))
#asyncio.run(led.start())

#led.set_light(0)
#led.set_light(7)
#led.light_up()
#time.sleep(3)
#led.reset()
#led.light_up()

