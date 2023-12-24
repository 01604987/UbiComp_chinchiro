from lib import logging
from micropython import const

logger = logging.getLogger(__name__)

# MENU_STATES
MENU_S = const(("single","multi"))
# GAME_STATES
GAME_S = const(("initial", "shaking", "result", "reset", "change"))

class State:

    # only allow switching menu states in "initial"
    # index is important
    
    def __init__(self) -> None:
        self.current_menu_state = None
        self.current_game_state = None
    
    def set_menu_state(self, state : int) -> None :
        try:
            # cycle through states of the menu
            if state >= len(MENU_S):
                raise(ValueError)
            self.current_menu_state = state
            logger.info(f"Current menu state: {self.current_menu_state}")
        except ValueError as err:
            logger.error(str(err))
    
    def get_menu_state(self) -> int:
        return self.current_menu_state
    
    def set_game_state(self, state) -> None :
        try:
            if isinstance(state, int):
                if state >= len(GAME_S):
                   raise(ValueError)
                self.current_game_state = state

            elif isinstance(state, str):
                # index() raises ValueError if value not in list
                self.current_game_state = GAME_S.index(state)
            else:
                raise(TypeError)
            
        except ValueError as err:
            logger.error(f"invalid state value: {state} with err code: {str(err)}")
        except TypeError as err:
            logger.error(f"invalid state: {state}. Should be int or str. ErrorCode: {str(err)}")
            
    def get_game_state(self) -> int:
        return self.current_game_state
        
    def reset_state(self) -> None:
        self.current_menu_state = None
        self.current_game_state = None
