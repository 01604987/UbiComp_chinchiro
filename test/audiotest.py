from machine import Pin
from dfplayermini import Dfplayer
import time
import random

player = Dfplayer(1)
time.sleep(5)

player.play(15)

counter = 1
while True:
    try:
        c = random.getrandbits(5)
        time.sleep(0.05)
        player.volume(c)
    except KeyboardInterrupt as err:
        player.stop()
        raise KeyboardInterrupt
