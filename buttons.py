from machine import Pin, Timer, ADC
from micropython import const


_BTNS = const(("left", "right", "top"))

class Buttons:

    def __init__(self, top_pin, l_btn, r_btn) -> None:
        # init interrupts
        self.l_btn = l_btn
        self.r_btn = r_btn
        # debounce timer active
        self.db_t_active = 0
        # debounce timer
        # TODO check if can use virtual timer -1
        self.db_t = Timer(0)
        self.r_pressed = 0
        self.l_pressed = 0
        self._init_interrupts()
 
    def _init_interrupts(self):
        self.l_btn.irq(trigger = 0, handler = None)
        self.r_btn.irq(trigger = 0, handler = None)

    def set_btn_irq(self, button, func, trg = Pin.IRQ_RISING)-> None:

        try:
            btn = self._check_instance(button)
        except ValueError as err:
            print(f"Invalid button with err code: {str(err)}")

        if btn == 0:
            self.l_btn.irq(trigger = trg, handler = lambda t: self._debounce(t, func))
        elif btn == 1:
            self.r_btn.irq(trigger = trg, handler = lambda t: self._debounce(t, func))
        elif btn == 2:
            pass

    def _debounce(self, t, func) -> None:
        if not self.db_t_active:
            print(f"starting debouncing")
            self.db_t_active = 1
            #! db_t_active needs to be reset within custom_function
            self.db_t.init(mode = Timer.ONE_SHOT, period = 30, callback = lambda t: func(t))

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
    
    def reset_buttons(self) -> None:
        self.r_pressed = 0
        self.l_pressed = 0
        self.reset_db_t()
        self._init_interrupts()
    
    def reset_db_t(self) -> None:
        self.db_t.deinit()
        self.db_t_active = 0

    def check_btn_val(self, button) -> int:
        try:
            btn = self._check_instance(button)
        except ValueError as err:
            print(f"invalid button")
        
        if btn == 0:
            return self.l_btn.value()
        if btn == 1:
            return self.r_btn.value()
        if btn == 2:
            return 0

    def _check_instance(self, button) -> int:
        if isinstance(button, str):
            return _BTNS.index(button)

        if isinstance(button, int):
            if button >= len(_BTNS):
                raise ValueError
            return button
        
class Buttons_ADC:

    def __init__(self, t_ADC_val, l_ADC_val, r_ADC_val) -> None:

        # initialize analog digital converter
        buttons = ADC(0)

        self.l_btn = [l_ADC_val - 5, l_ADC_val + 5, 0]
        self.r_btn = [r_ADC_val - 5, r_ADC_val + 5, 0]
        self.t_btn = [0, 0, 0]

        self.db_t = Timer(-1)
        self.db_t_active = 0

        self.l_pressed = 0
        self.r_pressed = 0
        self.hold = 0

    def _debounce(self, func) -> None:
        if not self.db_t_active:
            self.db_t_active = 1
            #! db_t_active needs to be reset within custom_function
            self.db_t.init(mode = Timer.ONE_SHOT, period = 30, callback = lambda t: func(t))
    
    def reset_db_t(self) -> None:
        self.db_t.deinit()
        self.db_t_active = 0

    def set_btn_irq(self, button, func) -> None:
        try:
            btn = self._check_instance(button)
        except ValueError as err:
            print(f"invalid button")
        
        if btn == 0:
            self.l_btn[3] = func
        if btn == 1:
            self.r_btn[3] = func
        if btn == 2:
            self.t_btn[3] = func


    def _check_instance(self, button) -> int:
        if isinstance(button, str):
            try:
                return _BTNS.index(button)
            except ValueError as err:
                print(f"Button name not defined. Error: {str(err)}")

        if isinstance(button, int):
            if button >= len(_BTNS):
                raise ValueError
            return button
        
        raise ValueError


    def poll_adc(self) -> None:
        val = self.buttons.read()
        if self.l_btn[3] == 0:
            return
        if self.r_btn[3] == 0:
            return
        #if self.t_btn[3] == 0:
        #    return

        # debug
        # print(val)

        if val >= 1000:
            hold = 0

        if val >= self.l_btn[0] and val <= self.l_btn[1] :
            if not hold:
                self._debounce(self.l_btn[3])
            
        if val >= self.r_btn[0] and val <= self.r_btn[1]:
            if not hold:
                self._debounce(self.r_btn[3])
        # 1024 ADC value = no button presses

        
        
        if r_pressed:
            r_pressed = 0
            #print(f"r_pressed {buttons.read()}")
        if l_pressed:
            l_pressed = 0
            #print(f"l_pressed {buttons.read()}")

#------------------------------------------------------------
# default button interrupts
        
    def r_press(self, t) -> None:
        if self.btns.buttons.read() >= self.btns.r_btn[0] and self.btns.buttons.read() <= self.btns.r_btn[1]:
            self.btns.r_pressed = 1
            self.btns.hold = 1
        self.btns.reset_db_t()
    

    def l_press(self, t) -> None:
        if self.btns.buttons.read() >= self.btns.l_btn[0] and self.btns.buttons.read() <= self.btns.l_btn[1]:
            self.btns.l_pressed = 1
            self.btns.hold = 1
        self.btns.reset_db_t()
