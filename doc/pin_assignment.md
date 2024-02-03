# ESP 8266 Pin assignment

## Vibration motors
PWM -> GPIO 4 (safe to use because will use transistors and demux to control between vibration) <br>
Demux control pin A = button pin 1 <br>
Demux control pin B = button pin 2 <br>
(button pins will be disabled during shaking, while demux will be disabled during not shaking) <br>

Alternatively move buttons to ADC pin and free up 2 pins. 

## Buttons
button 1 = GPIO (10) Pin.IN <br>
button 2 = GPIO (15) Pin.IN <br>

## Audio
DFPlayer 1 = GPIO (1) TX0 UART_0 <br>
DFPlayer 2 = GPIO (2) TX1 UART_1 <br>

## I2C
MPU 6050 SLC = GPIO (12) <br>
MPU 6050 SDA = GPIO (13) <br>

## LED
Data Out = GPIO 5 (Safe to use) <br>


## Free Pins:
GPIO 14 Safe to use <br>
GPIO 0 (pulled up on input) <br>
GPIO 5 <br>
GPIO 16 (no interrup, no I2C, maybe usable for controlling demux) <br>

NEED PINS FOR Digital potentiometer

## Resources
https://lastminuteengineers.com/esp8266-pinout-reference/
https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/
