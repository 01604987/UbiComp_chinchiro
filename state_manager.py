from micropython import const


# TODO maybe use int instead of str
# MENU_STATES
MENU_S = const(("single","multi"))
# GAME_STATES
GAME_S = const(("initial", "shaking", "result", "reset", "change"))

class State:

    # only allow switching menu states in "initial"
    # index is important
    
    def __init__(self) -> None:
        self.curr_menu_state = None
        self.curr_menu_state = None
    
    def set_menu_state(self, state : int) -> None :
        try:
            # cycle through states of the menu
            if state >= len(MENU_S):
                raise(ValueError)
            self.curr_menu_state = state
            print(f"Current menu state: {self.curr_menu_state}")
        except ValueError as err:
            print(str(err))
    
    def get_menu_state(self) -> int:
        return self.curr_menu_state
    
    # TODO reduce by only allowing int as state
    def set_game_state(self, state) -> None :
        try:
            if isinstance(state, int):
                if state >= len(GAME_S):
                   raise(ValueError)
                self.curr_menu_state = state

            elif isinstance(state, str):
                # index() raises ValueError if value not in list
                self.curr_menu_state = GAME_S.index(state)
            else:
                raise(TypeError)
            
        except ValueError as err:
            print(f"invalid state value: {state} with err code: {str(err)}")
        except TypeError as err:
            print(f"invalid state: {state}. Should be int or str. ErrorCode: {str(err)}")
            
    # TODO maybe discard getter and setter and instead use direct vairable access
    def get_game_state(self) -> int:
        return self.curr_menu_state
        
    def reset_state(self) -> None:
        self.curr_menu_state = None
        self.curr_menu_state = None
