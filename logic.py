from state_manager import MENU_S, State
from led_manager import LIGHTS, Led
from audio import Audio
from buttons import Buttons
from shake import Shake
from time import sleep
from micropython import mem_info
import random
import gc


class EndGame(Exception):
    pass

class Logic:

    def __init__(self, btns:Buttons, s_m:State, led:Led , audio: Audio ,network = None, shake: Shake = None, vibration = None) -> None:
        self.btns = btns
        # state_manager
        self.s_m = s_m
        self.network_config = network
        self.network = None
        # reset or game ended trigger
        self.rst = 0
        self.led = led
        self.audio = audio
        self.shake = shake

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
        

        while True:
            # poll accel values
            self.shake.update()
            # detect axis being shaken
            axis = self.shake.get_axis()
            
            if axis == None:
                # no shaking or undefined axis
                continue

            # faster skip on no shake 
            if abs(self.shake.values[axis][0]) >= abs(self.shake.values[axis][3]):
                continue 


            #! detect micro shake
            # micro shake has max audio volume cap because values very high

            #! shake detection on sign change
            try:
                # max value divided by last value = negative => sign changed == shake detected
                sign_inverse = self.shake.values[axis][3] / self.shake.values[axis][1]
            except ZeroDivisionError as err:
                continue
                
            try:
                if sign_inverse <= 0:
                    # reset max value
                    self.shake.values[axis][3] = 0

                    #! calculate magnitude

                    #! set audio volume
                    
                    #! change led dice

                    # play the correct audio with correct audio channel
                    # left, right, up, down based on axis.
                    # if axis == 0 and values[0][0] <= 0 -> left
                    # axis == 1 ? -> diagonal or left, right, up, down

                    #! play audio
                    if self.shake.values[axis][0] <= 0:
                        self.audio.play(0)
                    else:
                        self.audio.play(1)
                    #! start vibration
                        
                    #! send udp package                        
            
            except Exception as err:
                print(f"Exception during shaking with err code {str(err)}")

    
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
