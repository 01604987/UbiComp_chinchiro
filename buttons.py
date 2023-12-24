from lib import logging
from machine import Pin, Timer
from micropython import const

logger = logging.getLogger(__name__)


BTNS = const(("left", "right", "top"))

class Buttons:


    def __init__(self, top_pin, left_button, right_button) -> None:
        # init interrupts
        self.left_button = left_button
        self.right_button = right_button
        self.debounce_timer_running = 0
        self.debounce_timer = Timer(0)
        self.right_pressed = 0
        self.left_pressed = 0
        self._init_interrupts()

    
    def _init_interrupts(self):
        self.left_button.irq(trigger = Pin.IRQ_RISING, handler = lambda t: self._debounce(t, 0))
        self.right_button.irq(trigger = Pin.IRQ_RISING, handler = lambda t: self._debounce(t, 1))

    def _debounce(self, t, button):
        if not self.debounce_timer_running:
            logger.info(f"starting debouncing")
            self.debounce_timer_running = 1
            if button:
                self.debounce_timer.init(mode = Timer.ONE_SHOT, period = 30, callback = lambda t: self._step_menu(t))
            else:
                self.debounce_timer.init(mode = Timer.ONE_SHOT, period = 30, callback = lambda t: self._choose_menu(t))

    def _step_menu(self, t):
        if self.right_button.value():
            self.right_pressed += 1
            logger.info(f"Current menu counter: {self.right_pressed}")
                    
        self.debounce_timer.deinit()
        self.debounce_timer_running = 0


    def _choose_menu(self, t):
        if self.left_button.value():
            self.left_pressed = 1
            #self.state_manager.set_menu_state(self.right_pressed)
        
        self.debounce_timer.deinit()
        self.debounce_timer_running = 0

    def get_left_pressed(self) -> int:
        if self.left_pressed:
            self.left_pressed = 0
            return 1
        else:
            return 0

    def get_right_pressed(self, max) -> int:
        return self.right_pressed % max
    
    def reset_buttons(self) -> None:
        self.right_pressed = 0
        self.left_pressed = 0
        self.reset_debounce_timer()
        self._init_interrupts()
    
    def reset_debounce_timer(self) -> None:
        self.debounce_timer.deinit()
        self.debounce_timer_running = 0

    def check_button_value(self, button) -> int:
        try:
            btn = self._check_instance(button)
        except ValueError as err:
            logger.error(f"invalid button")
        
        if btn == 0:
            return self.left_button.value()
        if btn == 1:
            return self.right_button.value()
        if btn == 2:
            return 0
    

    
    def custom_button_irq(self, button, custom_function)-> None:

        try:
            btn = self._check_instance(button)
        except ValueError as err:
            logger.error("Invalid button")

        if btn == 0:
            self.left_button.irq(trigger = Pin.IRQ_RISING, handler = lambda t: self._custom_debounce(t, custom_function))
        elif btn == 1:
            self.right_button.irq(trigger = Pin.IRQ_RISING, handler = lambda t: self._custom_debounce(t, custom_function))
        elif btn == 2:
            pass

    def _custom_debounce(self, t, custom_function) -> None:
        if not self.debounce_timer_running:
            logger.info(f"starting debouncing")
            self.debounce_timer_running = 1
            #! debounce_timer_running needs to be reset within custom_function
            self.debounce_timer.init(mode = Timer.ONE_SHOT, period = 30, callback = lambda t: custom_function(t))

    def _check_instance(self, button) -> int:
        if isinstance(button, str):
            return BTNS.index(button)

        if isinstance(button, int):
            if button >= len(BTNS):
                raise ValueError
            return button
        