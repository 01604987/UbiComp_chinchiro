from machine import Pin
from lib.hcsr04 import HCSR04

class Distance:

    def __init__(self, trigger, echo) -> None:
        self.trigger = trigger
        self.echo = echo
        self.sensor = None
        self.threshold = 30
        self.overflow = 2400
        self.is_static = 0

    def initialize(self) -> None:
        self.sensor = HCSR04(self.trigger, self.echo)

    def set_threshold(self, value) -> None:
        self.threshold = value
    
    def static(self) -> int:
        return self.sensor.distance_mm() <= self.threshold
    
    def pick_up(self):
        return self.sensor.distance_mm() >= 100
    