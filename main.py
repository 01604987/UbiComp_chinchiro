from machine import Pin
from buttons import Buttons
from state_manager import State
from logic import Logic
from led_manager import Led
from lib.dfplayermini import Dfplayer
from audio import Audio
from lib import logging
from micropython import const, mem_info

# setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Main will be running after successful boot.
print("Hello World")

# some pins do not have irq (interrupt)
_L_BTN = const(10)
_R_BTN = const(13)

# UART(0) is used by REPL by default. Need to unbind first with os.dupterm(None, 1).
# Once unbound usb REPL will not work thus webREPL will be used.
# tx pin of UART(0) is at TX/Pin 1
# rx pin of UART(0) is at RX/Pin 3
_UART_0 = const(0)
# UART(1) only has tx as serial in is used by flash.
# tx pin of UART(1) is at D4/Pin 2
_UART_1 = const(1)

# init pins
left = Pin(_L_BTN, Pin.IN)
right = Pin(_R_BTN, Pin.IN)


# init classes

g = Logic(Buttons(None, left, right), State(), Led(), Audio(Dfplayer(_UART_0), Dfplayer(_UART_1)))
#print(free(True))
gc.collect()
logger.info(mem_info())

g.start()
