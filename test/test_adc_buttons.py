from machine import Pin, ADC, Timer
import time


# This implementation allows the use of the ESP 8266 ADC pin to detect button presses.
# Resistors and adc values need to be predetermined and hard coded to be able to distinguish between different
# 	button presses
# For this test, a schematic can be found here: https://miro.com/app/board/uXjVNarT9vY=/


buttons = ADC(0)


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
    if buttons.read() <= 130 and buttons.read()>=100:
        r_pressed = 1
        hold = 1
    reset_db_t()
    

def l_press(t) -> None:
    global buttons
    global l_pressed
    global hold
    if buttons.read() <= 190 and buttons.read() >= 170:
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
    
    
    
    if val <= 190 and val >=170 :
        if not hold:
            _debounce(l_press)
        
    if val <= 130 and val >= 100:
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