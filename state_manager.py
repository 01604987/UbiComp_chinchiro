from lib import logging

logger = logging.getLogger(__name__)



class StateManager:

    MENU_STATES = {
        0 : "single",
        1 : "multi"
    }

    # only allow switching menu states in "initial"

    GAME_STATES = {
        0 : "initial",
        1 : "shaking",
        2 : "result",
        3 : "reset",
        4 : "end"
    }

    def __init__(self) -> None:
        self.current_menu_state = None
        self.current_game_state = None
    
    def set_menu_state(self, state : int) -> None :
        try:
            # cycle through states of the menu
            if state >= len(StateManager.MENU_STATES):
                raise(ValueError)
            self.current_menu_state = state
            logger.info(f"Current menu state: {self.current_menu_state}")
        except ValueError as err:
            logger.error(str(err))
    
    def get_menu_state(self) -> int:
        return self.current_menu_state
    
    def set_game_state(self, state : int) -> None :
        self.current_game_state = state
        
    def reset_state(self) -> None:
        self.current_menu_state = None
        self.current_game_state = None
