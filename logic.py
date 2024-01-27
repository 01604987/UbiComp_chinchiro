from state_manager import MENU_S, State
from led_manager import LIGHTS, Led
from audio import Audio
from buttons import Buttons
from time import sleep
from micropython import mem_info
import random
import gc


class EndGame(Exception):
    pass

class Logic:

    def __init__(self, btns:Buttons, s_m:State, led:Led , audio: Audio ,network = None, accel = None, vibration = None) -> None:
        self.btns = btns
        # state_manager
        self.s_m = s_m
        self.network_config = network
        self.network = None
        # reset or game ended trigger
        self.rst = 0
        self.led = led
        self.audio = audio

    def start(self):
        while True:
            self._menu_select()
            try:
                self._game()
            except EndGame:
                self.reset_logic()
                pass

    def _menu_select(self):
        # on right button press light up different light configs
        # on left button press blink for confirmation

        self.btns.set_btn_irq("right", self._step_menu)
        self.btns.set_btn_irq("left", self._choose_menu)

        while True:
            sleep(0.5)
            # check button menu selection
            if self.btns.get_l_pressed():
                self.s_m.set_menu_state(self.btns.get_r_pressed(len(MENU_S)))
                break

    def _game(self):
        # initiate game state
        
        state = self.s_m.get_menu_state()

        if state == 0:
            # single player
            self.network = None
        if state == 1:
            # multiplayer
            # initialize network
            #! dummy value
            self.network = 1
        
        self.s_m.set_game_state("initial")

        self.btns.set_btn_irq("right", self._play_sound)
        self.audio.player1.volume(20)
        self.audio.player2.volume(20)
        #self.btns.set_btn_irq("right", self._set_light)
        self.btns.set_btn_irq("left", self._end_game)

        # led light determined by right button presse counter

        while True:
            self._initial(self.network)
            self._shaking()
            self._end()
            
    
    def _initial(self, network = None):
        # setup distance sensor
        
        interval = 2

        # setup timer to periodically blink stuff

        while True:
            sleep(0.5)
            if self.rst:
                raise EndGame
            #print("in initial sleeping")
            # self.led.set_light(self.btns.get_r_pressed(len(LIGHTS))))
            
            # poll distance sensor
            distance = 5
            # if sensor measure > interval
            if distance > interval:
                # stop any blinking leds, timers or sound effect that are designed only for initial
                break

    def _shaking(self):
        
        from lib.mpu6050 import accel
        from machine import I2C, Pin
        import time

        i = I2C(scl=Pin(12), sda=Pin(13), freq = 100000)
        print(i)
        a = accel(i)
        mem_info()

        default_interval = 10000

        # [[current val, last val, interval, max val], ...]
        values = [[0,0,default_interval, 0],[0,0,default_interval, 0],[0,0,default_interval, 0]]
        max_set = 0
        def acc(accel, values):
            raw = accel.get_values()
            axis = [0,0,0]
            axis[0] = raw['AcX']
            axis[1] = raw['AcY']
            axis[2] = raw['AcZ'] - 19000
            
            for index, val in enumerate(values):
                
                #if abs(axis[index]) > 500:            
                    # copy current value to last value
                    val[1] = val[0]
                    # update current value with new value
                    val[0] = axis[index]
                
        def calculate_interval(axis ,values, default_interval):
            if axis == None:
                for val in values:
                    val[2] = default_interval
                    #print("resetting interval for all")
                return
            
            for index, val in enumerate(values):
                if index == axis:
                    continue
                val[2] = abs(values[axis][0]) + default_interval

        # return x, y, z or no axis
        def detect_axis(values, default_interval):
            for index, val in enumerate(values):
                # value smaller than interval
                if abs(val[0]) < val[2]:
                    continue
                else:
                    return index
            return None

        def max_val(values, axis):
            if axis == None:
                return
            
            if abs(values[axis][3]) < abs(values[axis][0]):
                values[axis][3] = values[axis][0]

        counter = 0
        while True:
            # poll accel values
            acc(a, values)
            # detect axis being shaken
            axis = detect_axis(values, default_interval)
            # recalculate interval for other axis
            calculate_interval(axis, values, default_interval)
            max_val(values, axis)
            #max_set = max_val(values, axis)
            #print(values[2])
            #continue
            #print(values[1])
            #print(axis)
            if axis == None:
                #print(values)
                continue
            
            #print(values[0])
            try:
                if values[axis][3] / values[axis][1] <= 0:
                    print(axis)
                    print(values)
                    values[axis][3] = 0
                    if values[axis][0] <= 0:
                        self.audio.play(0)
                    else:
                        self.audio.play(1)
                    time.sleep(0.01)
                    continue
            except ZeroDivisionError as err:
                continue
                
            if values[axis][1] > 0 and values[axis][0] > 0:
                continue
            if values[axis][1] < 0 and values[axis][0] < 0:
                continue
        
    
    def _end(self):
        raise(NotImplementedError)

    def reset_logic(self):
        self.btns.reset_buttons()
        self.s_m.reset_state()
        self.rst = 0
        self.network = None


    ##################################################################################################################
    # irq for button presses are defined here
        
    def _step_menu(self, t):
        if self.btns.check_btn_val("right"):
            self.btns.r_pressed += 1
            print(f"Current menu counter: {self.btns.get_r_pressed()}")
                    
        self.btns.reset_db_t()

    def _choose_menu(self, t):
        if self.btns.check_btn_val("left"):
            self.btns.l_pressed = 1
            #self.state_manager.set_menu_state(self.r_pressed)
        
        self.btns.reset_db_t()

    def _set_light(self, t):
        if self.btns.check_btn_val("right"):
            # TODO change this to function set
            self.btns.r_pressed += 1
            print(f"Setting light to: {self.btns.get_r_pressed(len(LIGHTS))}")
            gc.collect()
            mem_info()
            #self.led.set_light(self.btns.get_r_pressed(len(LIGHTS)))
        self.btns.reset_db_t()

    def _end_game(self, t):
        if self.btns.check_btn_val("left"):
            print(f"Ending current game")
            self.rst = 1
            self.audio.player1.module_reset()
            self.audio.player2.module_reset()
        self.btns.reset_db_t()

    def _play_sound(self, t):
        if self.btns.check_btn_val("right"):
            gc.collect()
            mem_info()
            self.btns.r_pressed +=1
            if self.btns.r_pressed % 2:
                self.audio.play(0)
            else:
                self.audio.play(1)
                
        self.btns.reset_db_t()
