# ESP 8266 Pin assignment

## Vibration motors
PWM -> GPIO 4 (safe to use because will use transistors and demux to control between vibration) <br>
Demux control pin A = button pin 1 <br>
Demux control pin B = button pin 2 <br>
(button pins will be disabled during shaking, while demux will be disabled during not shaking) <br>

## Buttons
button 1 = GPIO 10 (SD3) Pin.IN <br>
button 2 = GPIO 15 (D8)  Pin.IN <br>

Alternatively:

3x buttons = ADC0 (A0) <br>

## Audio    
DFPlayer 1 = GPIO 1 (TX) TX0 UART_0 <br>
DFPlayer 2 = GPIO 2 (D4) TX1 UART_1 <br>

## I2C
MPU 6050 SLC = GPIO 12 (D6) <br>
MPU 6050 SDA = GPIO 13 (D7)<br>

## LED
Data Out = GPIO 5 (D1) Pin.OUT <br>

## Distance Sensor
HCSR04 ECHO = GPIO 16 (D0) Pin.IN <br>
HCSR04 TRIG = GPIO 0 (D3) Pin.OUT <br>
Note: Other way will prevent boot if D3 is pulled LOW. <br>

## Free Pins:
GPIO 14 (D5) Safe to use <br>
<!--GPIO 0 (pulled up on input) <br> -->
<!--GPIO 4 (D2)<br> -->
<!--GPIO 5 (D1)<br> -->
<!--GPIO 16 (no interrup, no I2C, maybe usable for controlling demux) <br> -->
probably free:<br>
GPIO 10 (SD3) as input<br>
GPIO 15 (D8)<br>

NEED PINS FOR Digital potentiometer
NEED PINS FOR DEMUX SELECTOR

## Resources
https://lastminuteengineers.com/esp8266-pinout-reference/
https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/

## IDEAS

Possible to connect SCL clock of MPU6050 and Trigger Pin of HCSR04 to the same pin and in software keep switching and reinitializing stuff. 
