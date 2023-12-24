from lib import logging
from buttons import Buttons
from state_manager import State
from led_manager import Led
import time

logger = logging.getLogger(__name__)

class EndGame(Exception):
    pass

class Logic:

    def __init__(self, buttons : Buttons, state_manager : State, led: Led ,network = None, accel = None, vibration = None, audio = None) -> None:
        self.buttons = buttons
        self.state_manager = state_manager
        self.network_config = network
        self.network = None
        self.game_ended = 0
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
            time.sleep(0.5)
            # check button menu selection
            if self.buttons.get_left_pressed():
                self.state_manager.set_menu_state(self.buttons.get_right_pressed(len(State.MENU_STATES)))
                break

    def _game(self):
        # initiate game state
        
        state = self.state_manager.get_menu_state()

        if state == 0:
            # single player
            self.network = None
        if state == 1:
            # multiplayer
            # initialize network
            #! dummy value
            self.network = 1
        
        self.state_manager.set_game_state("initial")

        self.buttons.custom_button_irq("right", self._set_light)
        self.buttons.custom_button_irq("left", self._end_game)

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
            time.sleep(0.5)
            if self.game_ended:
                raise EndGame
            #logger.info("in initial sleeping")
            # self.led.set_light(self.buttons.get_right_pressed(len(Led.lights))))
            
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
        self.buttons.reset_buttons()
        self.state_manager.reset_state()
        self.game_ended = 0
        self.network = None


    def _set_light(self, t):
        if self.buttons.check_button_value("right"):
            #TODO change this to public setter function instead
            self.buttons.right_pressed += 1
            logger.info(f"Setting light to: {self.buttons.get_right_pressed(len(Led.lights))}")
            #self.led.set_light(self.buttons.get_right_pressed(len(Led.lights)))
        self.buttons.reset_debounce_timer()

    def _end_game(self, t):
        if self.buttons.check_button_value("left"):
            logger.info(f"Ending current game")
            self.game_ended = 1
        self.buttons.reset_debounce_timer()
