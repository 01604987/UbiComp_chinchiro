from machine import Pin, PWM, Timer

# A0 = TOP == 0
# A1 = BOTTOM == 1
# A2 = LEFT == 2
# A3 = RIGHT == 3

class Vibration:

    def __init__(self, s0= None, s1=None, pwm0=None) -> None:
        self.s0 = Pin(10, Pin.OUT)
        self.s1 = Pin(15, Pin.OUT)
        self.pwm0 = PWM(Pin(5), freq=50, duty=0)
        self.timer = Timer(-1)

    
    def deinit(self):
        self.timer.deinit()
        self.pwm0.duty(0)

    def vibrate(self, motor, strength = None):

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
        
        duty = self.map_strength_to_duty(strength)
        
        self.pwm0.duty(duty)
        self.timer.init(mode = Timer.ONE_SHOT, period = 150, callback = lambda t: self.stop(t))


    def map_strength_to_duty(self, strength):
        if not strength:
            return 400
        # clamp between 8k & 30k
        strength = max(8000, min(abs(strength), 30000))

        # Define the source and target intervals
        #a, b = 8000, 30000  # Source interval [a, b]
        #c, d = 400, 900    # Target interval [c, d]

        # Apply the transformation formula
        #y = ((x - a) / (b - a)) * (d - c) + c

        duty = int(((strength - 8000) / (22000)) * (500) + 400)
        return duty


    def stop(self, t):
        self.pwm0.duty(0)
