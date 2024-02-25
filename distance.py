from lib.hcsr04 import HCSR04
from micropython import const

_THRESH = const(30)

class Distance:

    def __init__(self, trigger, echo) -> None:
        self.sensor = HCSR04(trigger, echo)

    def set_threshold(self, value) -> None:
        self.threshold = value
    
    def static(self) -> int:
        return self.sensor.distance_mm() <= _THRESH
    
    def pick_up(self):
        return self.sensor.distance_mm() >= _THRESH * 3
    