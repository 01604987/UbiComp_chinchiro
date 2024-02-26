from machine import Pin, PWM, Timer

# A0 = TOP == 0
# A1 = BOTTOM == 1
# A2 = LEFT == 2
# A3 = RIGHT == 3

class Vibration:

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
        
        
        self.pwm0.duty(800)
        self.timer.init(mode = Timer.ONE_SHOT, period = 150, callback = lambda t: self.stop(t))


    def stop(self, t):
        self.pwm0.duty(0)
