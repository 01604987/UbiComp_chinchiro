from machine import Pin
from buttons_adc import Buttons_ADC
from state_manager import State
from logic import Logic
from led_manager import Led
from audio import Audio
from shake import Shake
from distance import Distance
from connection import Connection
from net2 import Client
from micropython import const, mem_info

# setup logging

# Main will be running after successful boot.
print("Hello World")

_IP_SERVER = const('192.168.1.10')
_IP_CLIENT = const('192.168.1.11')
_PORT = const(5002)
_SSID = 'TP-Link_2.4Ghz'
_PASSWORD = 'jkv777kim'

#! move comments to some other doc to safe on mem/storage ?
###### BUTTONS ######

# Button implementation with GPIO
# some pins do not have irq (interrupt)
#_L_BTN = const(10)
#_R_BTN = const(15)

# init GPIO button pins
#left_btn = Pin(_L_BTN, Pin.IN)
#right_btn = Pin(_R_BTN, Pin.IN)

# Button implementation with ADC (A0)
_T_BTN = const(0)
_L_BTN = const(96)
_R_BTN = const(180)

###### AUDIO ######

# UART(0) is used by REPL by default. Need to unbind first with os.dupterm(None, 1).
# Once unbound usb REPL will not work thus webREPL will be used.
# tx pin of UART(0) is at TX/Pin 1
# rx pin of UART(0) is at RX/Pin 3
_UART_0 = const(0)
# UART(1) only has tx as serial in is used by flash.
# tx pin of UART(1) is at D4/Pin 2
_UART_1 = const(1)

# In order to use USB repl for debugging after webrepl has been disabled, maybe a button or menu select can be used to reactivate os.dupterm

###### IMU ######

# init mpu6050 pins
scl = Pin(12)
sda = Pin(13)

###### HCSR04 ######

_TRIGGER = const(0)
_ECHO = const(16)



# init classes

#buttons = Buttons(None, left_btn, right_btn)
buttons = Buttons_ADC(_T_BTN, _L_BTN, _R_BTN)               
state = State()
led = Led()
# _UART_1 first because this address is not bound to USB repl and can safely be used. When reenable repl, can simply leave out second param.
#audio = Audio(_UART_1, _UART_0)
audio = Audio(_UART_1)
shake = Shake(scl, sda, 100000)
distance = Distance(_TRIGGER, _ECHO)
network = Client(_IP_SERVER, _PORT)
conn = Connection(_IP_CLIENT, _SSID, _PASSWORD)

g = Logic(buttons, state, led, audio, network, shake, distance, None, conn)


#dereference to safe a bit of mem ?
#left_btn = None
#right_btn = None
scl = None
sda = None
buttons = None
state = None
audio = None
shake = None
distance = None

#g = Logic(Buttons(None, left_btn, right_btn), State(), Led(), Audio(Dfplayer(_UART_0), Dfplayer(_UART_1)))
#print(free(True))
gc.collect()
mem_info()

g.start()
