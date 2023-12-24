from machine import Pin
from buttons import Buttons
from state_manager import State
from logic import Logic
from led_manager import Led
from lib import logging
from micropython import const, mem_info

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main will be running after successful boot.
print("Hello World")

# some pins do not have irq (interrupt)
_L_BTN = const(10)
_R_BTN = const(13)

# init pins
left = Pin(_L_BTN, Pin.IN)
right = Pin(_R_BTN, Pin.IN)


# init classes

g = Logic(Buttons(None, left, right), State(), Led())
#print(free(True))
gc.collect()
logger.info(mem_info())

g.start()
