from lib.dfplayermini import Player

from time import sleep

music = Player(pin_TX=1, pin_RX=3)

music.volume(20)
music.play(1)
sleep(10)
