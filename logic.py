from buttons import Buttons
from state_manager import StateManager
import time

class Logic:

    def __init__(self, buttons : Buttons, state_manager : StateManager, network = None, accel = None, vibration = None, audio = None) -> None:
        self.buttons = buttons
        self.state_manager = state_manager


    def start(self):
        while True:
            self._menu_select()
            self._game(self.state_manager.get_menu_state())

    def _menu_select(self):
        while True:
            time.sleep(0.5)
            # check button menu selection
            if self.buttons.get_left_pressed():
                self.state_manager.set_menu_state(self.buttons.get_right_pressed(len(StateManager.MENU_STATES)))
                #break
            # check state ? 

    def _game(self, state):
        while True:

            break
