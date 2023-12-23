from machine import Pin
import buttons
import state_manager
import logic
from lib import logging

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main will be running after successful boot.
print("Hello World")

# some pins do not have irq (interrupt)
LEFT_BUTTON = 10
RIGHT_BUTTON = 13

# init pins
left = Pin(LEFT_BUTTON, Pin.IN)
right = Pin(RIGHT_BUTTON, Pin.IN)


# init classes
but = buttons.Buttons(None, left, right)
state = state_manager.StateManager()
g = logic.Logic(buttons=but, state_manager = state)
g.start()


