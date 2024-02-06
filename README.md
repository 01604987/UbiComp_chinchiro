# Chinchiro
This repository contains micropython code for a Ubiquitous Computing project using the esp8266.

A workflow documentation as well as parts list and idea protype can be found in this [miro board](https://miro.com/app/board/uXjVNw7E-uI=/?share_link_id=554810757735).

# Issues and Limitations
## ESP8266
### Serial TX/RX
The ESP8266 supports 2 hardware serial ports. TX0/RX0 on pin 1/3 respectively and TX1/RX1 on pin 2/0. On the pin out sheet, TX2/RX2 are marked on pin 15/13, however, these are the same serial connections as TX0/RX0 and with switchable can be made active in TX2/RX2 instead.<br>
Unfortunately TX0/RX0 is already reserved for USB serial communication (REPL) by default. This means TX0/RX0 can not be used for UART unless REPL is disabled with `os.dupterm(None, 1)`. Once disabled, UART(0)(=serial com on TX0/RX0) can be used normally, however, developing, uploading and downloading scripts via USB connection will not work anymore. In this case, webREPL can be used instead. Please see [this](https://bhave.sh/micropython-webrepl-thonny/) for further instructions. A webrepl configured boot script can be found in this repository as well. Just rename boot.webREPL.py to boot.py. <br>
As for TX1/RX1, the read port (RX) is reserved for flash memory on the esp 8266, therefore, only TX1 (write) is available.

Micropython does not seem to support software serial on the esp 8266.

## DFplayer mini
### Multichannel
The DFplayer mini does not support multi channel audio playback on speakers. Every file played will be mono.<br>

### Simulatenous Playback
The DFplayer mini does not support simultaneos playback of mutliple files. Everytime play has been invoked, the currently playing file will be over-written. If 2 or more audio files are played back rapidly (high frequency), harsh cutoffs of the previous sound will be audible. This makes simulating dice shaking unnatural. To combat this, 2 DFplayer minis can be used, resulting in 2 speakers per device and allowing stereo output.
However, as mentioned in section [ESP8266 Serial](#serial-txrx), the ESP8266 only support 2 HW serial ports, resulting in further development only possible with webREPL.

### Volume
Setting the volume level onto the DFplayer can result in delays, therefore, it is advised to avoid many and rapid calls to set new volume.

### HW Bug
On some occasions, the DFplayer may hang up and stop receiving write commands. This may be solvable [via software](https://reprage.com/posts/2018-05-08-dfplayer-mini-cheat-sheet/), however, it might be easier to include a switch to cut and connect the vcc on the DFplayer mini. This can also be used as a mute switch.

## Buttons
Unfortunately the nodemcu ESP8266 comes with a variety of limitations regarding Pin state, GPIO input and output. Information can be taken from here: <br>
https://lastminuteengineers.com/esp8266-pinout-reference/ <br>
https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/ <br>
Because this project utilizes a lot of different modules and components, availability of pins are also limited, therefore a way to generally save on GPIO pins is to move the control of buttons to the single unused ADC pin (A0) on the ESP8266. By correctly setting up resistors and voltage drops for each push buttons, different buttons can represent different voltages detectable by the ADC and thus map to different button functions.

The ESP 8266 can support up to 10 bit resolution leading to 1024 samples for the its ADC. It should be noted that the ADC can not handle voltages beyond 1v, however, most dev boards, including the NodeMCU ESP 8266, have internal voltage deviders that allow the ADC to operate with up to 3.3v.


This strategy allows us to control all buttons with a single pin, essentially saving up to 3 GPIO pins.
For this current button setup, please see the included Circuit Diagram in the Miro Board.
