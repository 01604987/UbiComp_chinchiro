from machine import Pin
from buttons_adc import Buttons_ADC
from state_manager import State
from logic import Logic
from led_manager import Led
from audio import Audio
from shake import Shake
from micropython import const, mem_info

# setup logging

# Main will be running after successful boot.
print("Hello World")

# some pins do not have irq (interrupt)
_L_BTN = const(10)
_R_BTN = const(15)

# UART(0) is used by REPL by default. Need to unbind first with os.dupterm(None, 1).
# Once unbound usb REPL will not work thus webREPL will be used.
# tx pin of UART(0) is at TX/Pin 1
# rx pin of UART(0) is at RX/Pin 3
_UART_0 = const(0)
# UART(1) only has tx as serial in is used by flash.
# tx pin of UART(1) is at D4/Pin 2
_UART_1 = const(1)

# In order to use USB repl for debugging after webrepl has been disabled, maybe a button or menu select can be used to reactivate os.dupterm

# init button pins
#left_btn = Pin(_L_BTN, Pin.IN)
#right_btn = Pin(_R_BTN, Pin.IN)


# init mpu6050 pins
scl = Pin(12)
sda = Pin(13)


# init classes

#buttons = Buttons(None, left_btn, right_btn)

t_btn = 0
l_btn = 96
r_btn = 180

buttons = Buttons_ADC(t_btn, l_btn, r_btn)
                  
state = State()
led = Led()
# _UART_1 first because this address is not bound to USB repl and can safely be used. When reenable repl, can simply leave out second param.
audio = Audio(_UART_1, _UART_0)
shake = Shake(scl, sda, 100000)

g = Logic(buttons, state, led, audio, None, shake)


#dereference to safe a bit of mem
left_btn = None
right_btn = None
t_btn = None
l_btn = None
r_btn = None
scl = None
sda = None
buttons = None
state = None
audio = None
shake = None

#g = Logic(Buttons(None, left_btn, right_btn), State(), Led(), Audio(Dfplayer(_UART_0), Dfplayer(_UART_1)))
#print(free(True))
gc.collect()
mem_info()

g.start()
