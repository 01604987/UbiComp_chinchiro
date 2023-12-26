from lib import logging
from state_manager import MENU_S, State
from led_manager import LIGHTS, Led
from audio import Audio
from buttons import Buttons
from time import sleep
from micropython import mem_info
import random
import gc


logger = logging.getLogger(__name__)

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
        self.audio.player1.volume(15)
        self.audio.player2.volume(15)
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
            #logger.info("in initial sleeping")
            # self.led.set_light(self.btns.get_r_pressed(len(LIGHTS))))
            
            # poll distance sensor
            distance = 0
            # if sensor measure > interval
            if distance > interval:
                # stop any blinking leds, timers or sound effect that are designed only for initial
                break

    def _shaking(self):
        raise(NotImplementedError)
    
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
            logger.info(f"Current menu counter: {self.btns.get_r_pressed()}")
                    
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
            logger.info(f"Setting light to: {self.btns.get_r_pressed(len(LIGHTS))}")
            gc.collect()
            mem_info()
            #self.led.set_light(self.btns.get_r_pressed(len(LIGHTS)))
        self.btns.reset_db_t()

    def _end_game(self, t):
        if self.btns.check_btn_val("left"):
            logger.info(f"Ending current game")
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
