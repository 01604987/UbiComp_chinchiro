from machine import Timer, ADC
from micropython import const

# 0 = left, 1 = right, 2 = top
#_BTNS = const(("left", "right", "top"))
#_BTNS = const((0, 1, 2))
        
class Buttons_ADC:

    def __init__(self, t_ADC_val, l_ADC_val, r_ADC_val) -> None:

        # initialize analog digital converter
        self.buttons = ADC(0)

        self.l_btn = [l_ADC_val - 10, l_ADC_val + 10, 0]
        self.r_btn = [r_ADC_val - 10, r_ADC_val + 10, 0]
        self.t_btn = [0, 0, 0]

        self.db_t = None

        self.l_pressed = 0
        self.r_pressed = 0
        self.hold = 0
        self.rst = 0
        self.is_static = 0

    def _debounce(self, func) -> None:
        if not func:
            return
        if not self.db_t:
            self.db_t = Timer(0)
            self.db_t.init(mode = Timer.ONE_SHOT, period = 30, callback = lambda t: func(t))
    
    def reset_db_t(self) -> None:
        self.db_t.deinit()
        self.db_t = None
        #print("reset")
    
    def reset_buttons(self) -> None:
        #self.buttons = ADC(0)

        self.l_btn[2] = 0
        self.r_btn[2] = 0
        self.r_btn[2] = 0

        self.reset_db_t()

        self.l_pressed = 0
        self.r_pressed = 0
        #self.hold = 0
        
    def set_btn_irq(self, btn, func) -> None:
        # try:
        #     btn = self._check_instance(button)
        # except ValueError as err:
        #     print(f"invalid button")
        
        if btn == 0:
            self.l_btn[2] = func
        if btn == 1:
            self.r_btn[2] = func
        if btn == 2:
            self.t_btn[2] = func


    # def _check_instance(self, button) -> int:
    #     if isinstance(button, str):
    #         try:
    #             return _BTNS.index(button)
    #         except ValueError as err:
    #             print(f"Button name not defined. Error: {str(err)}")

    #     if isinstance(button, int):
    #         if button >= len(_BTNS):
    #             raise ValueError
    #         return button
        
    #     raise ValueError

    def check_btn_val(self, btn):
        # try:
        #     btn = self._check_instance(button)
        # except ValueError as err:
        #     print(f"invalid button")
        
        if btn == 0:
            return self.buttons.read() >= self.l_btn[0] and self.buttons.read() <= self.l_btn[1]
        if btn == 1:
            return self.buttons.read() >= self.r_btn[0] and self.buttons.read() <= self.r_btn[1]
        if btn == 2:
            return 0
        
    def get_l_pressed(self) -> int:
        if self.l_pressed:
            self.l_pressed = 0
            return 1
        else:
            return 0

    def get_r_pressed(self, max = 0) -> int:
        if not max:
            return self.r_pressed
        return self.r_pressed % max

    def poll_adc(self) -> None:
        val = self.buttons.read()
        if self.l_btn[2] == 0:
            return
        if self.r_btn[2] == 0:
            return
        #if self.t_btn[3] == 0:
        #    return

        # debug
        # print(val)

        if val >= 1000:
            self.hold = 0

        if val >= self.l_btn[0] and val <= self.l_btn[1] :
            if not self.hold:
                self._debounce(self.l_btn[2])
            
        if val >= self.r_btn[0] and val <= self.r_btn[1]:
            if not self.hold:
                self._debounce(self.r_btn[2])
        # 1024 ADC value = no button presses



    def _step_menu_ADC(self, t):
        if self.check_btn_val(1):
            self.r_pressed += 1
            print(f"Current menu counter: {self.r_pressed}")
            self.hold = 1
        self.reset_db_t()
        
    def _choose_menu_ADC(self, t):
        if self.check_btn_val(0):
            self.l_pressed = 1
            self.hold = 1
        self.reset_db_t()
    
    def _end_game_ADC(self, t):
        if self.check_btn_val(0):
            self.hold = 1
            self.rst = 1
    
    def _distance_sim(self, t):
        if self.check_btn_val(1):
            print(f"distance static")
            self.hold = 1
            self.is_static = not self.is_static
        self.reset_db_t()
