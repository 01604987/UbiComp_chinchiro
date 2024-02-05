from machine import Pin, ADC, Timer
import time
from micropython import const


# This implementation allows the use of the ESP 8266 ADC pin to detect button presses.
# Resistors and adc values need to be predetermined and hard coded to be able to distinguish between different
# 	button presses
# For this test, a schematic can be found here: https://miro.com/app/board/uXjVNarT9vY=/


buttons = ADC(0)


# 1k ohm ~ 96 ADC
_r_min = 92
_r_max = 102

# 2k ohm ~ 180 ADC
_l_min = 174
_l_max = 184

r_pressed = 0
l_pressed= 0
hold = 0

db_t = Timer(-1)
db_t_active = 0

def _debounce(func) -> None:
    global db_t_active
    global db_t
    if not db_t_active:
        print(f"starting debouncing")
        db_t_active = 1
        #! db_t_active needs to be reset within custom_function
        db_t.init(mode = Timer.ONE_SHOT, period = 30, callback = func)#lambda t: func(t))

def r_press(t) -> None:
    global buttons
    global r_pressed
    global hold
    global _r_min
    global _r_max
    if buttons.read() <= _r_max and buttons.read()>= _r_min:
        r_pressed = 1
        hold = 1
    reset_db_t()
    

def l_press(t) -> None:
    global buttons
    global l_pressed
    global hold
    global _l_min
    global _l_max
    if buttons.read() <= _l_max and buttons.read() >= _l_min:
        l_pressed = 1
        hold = 1
    reset_db_t()
    
    
def reset_db_t() -> None:
    global db_t
    global db_t_active
    db_t.deinit()
    db_t_active = 0

while True:
    val = buttons.read()
    #print(val)
    
    
    
    if val <= _l_max and val >= _l_min :
        if not hold:
            _debounce(l_press)
        
    if val <= _r_max and val >= _r_min:
        if not hold:
            _debounce(r_press)
        #print(r_pressed)
    if val >= 1000:
        hold = 0
    
    
    if r_pressed:
        r_pressed = 0
        print(f"r_pressed {buttons.read()}")
    if l_pressed:
        l_pressed = 0
        print(f"l_pressed {buttons.read()}")
    
    
    
    time.sleep(0.01)