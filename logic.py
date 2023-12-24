from lib import logging
from state_manager import MENU_S, State
from led_manager import LIGHTS, Led
from buttons import Buttons
from time import sleep
from micropython import mem_info
import gc


logger = logging.getLogger(__name__)

class EndGame(Exception):
    pass

class Logic:

    def __init__(self, btns:Buttons, s_m:State, led:Led ,network = None, accel = None, vibration = None, audio = None) -> None:
        self.btns = btns
        # state_manager
        self.s_m = s_m
        self.network_config = network
        self.network = None
        # reset or game ended trigger
        self.rst = 0
        self.led = led


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
        while True:
            sleep(0.5)
            # check button menu selection
            if self.btns.get_left_pressed():
                self.s_m.set_menu_state(self.btns.get_right_pressed(len(MENU_S)))
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

        self.btns.custom_button_irq("right", self._set_light)
        self.btns.custom_button_irq("left", self._end_game)

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
            # self.led.set_light(self.btns.get_right_pressed(len(LIGHTS))))
            
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


    def _set_light(self, t):
        if self.btns.check_button_value("right"):
            self.btns.right_pressed += 1
            logger.info(f"Setting light to: {self.btns.get_right_pressed(len(LIGHTS))}")
            gc.collect()
            mem_info()
            #self.led.set_light(self.btns.get_right_pressed(len(LIGHTS)))
        self.btns.reset_debounce_timer()

    def _end_game(self, t):
        if self.btns.check_button_value("left"):
            logger.info(f"Ending current game")
            self.rst = 1
        self.btns.reset_debounce_timer()
