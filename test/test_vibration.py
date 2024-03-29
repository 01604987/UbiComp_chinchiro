from machine import Pin, PWM, Timer
import time

class Vibration():
    def __init__(self, s0= None, s1=None, pwm0=None) -> None:
        self.s0 = Pin(10, Pin.OUT)
        self.s1 = Pin(15, Pin.OUT)
        self.pwm0 = PWM(Pin(5), freq=200, duty=0)
        self.timer = Timer(-1)

    def vibrate(self, motor):
        self.pwm0.duty(0)
        if motor == 0:
            self.s0.value(0)
            self.s1.value(0)
            print('00  TOP')
        if motor == 1:
            self.s0.value(1)
            self.s1.value(0)
            print('01 BOTTOM')
        if motor == 2: 
            self.s0.value(0)
            self.s1.value(1)
            print('10 LEFT')
        if motor == 3:
            self.s0.value(1)
            self.s1.value(1)
            print('11 RIGHT')
        
        
        self.pwm0.duty(600)
        self.timer.init(mode = Timer.ONE_SHOT, period = 200, callback = lambda t: self.stop(t))


    def stop(self, t):
        self.pwm0.duty(0)


def step(num):
    if num == 0:
        # A0
        s0.value(0)
        s1.value(0)
    if num == 1:
        # A1
        s0.value(1)
        s1.value(0)
    if num == 2:
        # A2
        s0.value(0)
        s1.value(1)
    if num == 3:
        # A3
        s0.value(1)
        s1.value(1)

def vib():
    print(pwm0)
    pwm0.duty(800)
    time.sleep(0.25)
    pwm0.duty(0)
    time.sleep(2)

v = Vibration()


while True:
    v.vibrate(2)
    time.sleep(0.3)
    v.vibrate(3)
    time.sleep(0.3)
        