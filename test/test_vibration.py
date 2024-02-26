from machine import Pin, PWM
import time

s0 = Pin(10, Pin.OUT)
s1 = Pin(15, Pin.OUT)

pwm0 = PWM(Pin(4), freq=150, duty=800)  # create and configure in one go
print(pwm0)                               # view PWM settings


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
    pwm0.duty(700)
    time.sleep(0.25)
    pwm0.duty(0)
    time.sleep(2)

while True:
    step(0)
    vib()
    step(1)
    vib()
    step(2)
    vib()
    step(3)
    vib()
        