from machine import Pin
from micropython import const
import neopixel
import time
import uasyncio as asyncio


# all colors are 1/5 bright
#               "red",   "green",   "blue",    "yellow",   "purple", "turkoise"
LIGHTS = const(((64,0,0), (0,64,0), (0,0,64), (64,64,0), (64,0,64), (0,64,64)))


class Led:

    def __init__(self, data, pixel_nr) -> None:
        self.pixel_nr = pixel_nr
        self.data = data
        self.data_pin = Pin(data)
        self.np = None
        self.sleep_time_ms = 1000
        self.number = [0,0,0]
        

    
    def initialize(self) -> None:
        self.np = neopixel.NeoPixel(self.data_pin, self.pixel_nr)

    def reset(self) -> None:
        for index, val in enumerate(self.np):
            self.np[index] = (0,0,0)

    async def light_up(self) -> None:
        self.np.write()

    async def set_light(self, nr) -> None:
        self.np[nr] = LIGHTS[0]

    def create_task(self):
        asyncio.create_task(self.start())


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
nr = const(8)
led = Led(pin, nr)
led.initialize()
asyncio.create_task(sleeper(led))
asyncio.run(led.start())

#led.set_light(0)
#led.set_light(7)
#led.light_up()
#time.sleep(3)
#led.reset()
#led.light_up()

