from micropython import const
from neopixel import NeoPixel
from machine import Timer


#               "red",   "green",   "blue",    "yellow",   "purple", "turkoise"
_LIGHTS = const(((3,0,0), (0,3,0), (0,0,3), (2,2,0), (2,0,2), (0,2,2)))
_NUMS = [[], [3], [0, 6], [2, 3, 4], [0, 2, 4, 6], [0, 2, 3, 4, 6], [0, 1, 2, 4, 5, 6]]
_LOADING = const((15, 17, 19, 5, 3, 1))

class Led:

    def __init__(self, data_p, p_nr) -> None:
        self.np = NeoPixel(data_p, p_nr)
        self.sleep_time_ms = 1000
        self.timer = None
        self.step = 0
        self.col = _LIGHTS[0]

    def reset(self) -> None:
        self.np.fill((0, 0, 0))
        self.np.write()
        

    # expect num to be well formed chinchiro valid dice rolls
    def numbers (self, num, col=0):
        if not isinstance (num, list):
            print("Not a list")
            raise Exception
        
        self.reset()
        if not col:
            col = self.col
        else:
            col = _LIGHTS[col]

        for i, val in enumerate(num):
            offset = i * int(len(self.np)/ 3)
            for i in _NUMS[val]:
                self.np[i + offset] = col
        
        self.np.write()

    # TODO change/add to pingpong animation
    def display_loading(self, t):
        self.np[_LOADING[self.step % 6]] = _LIGHTS[4]
        self.np[_LOADING[(self.step - 1) % 6]] = (0, 0, 0)
        self.step += 1
        self.np.write()



    def start_loading(self, interval_ms = 1000):
        self.stop_timer()
        if not self.timer:
            self.reset()
            self.timer = Timer(-1)
            self.timer.init(period=interval_ms, mode=Timer.PERIODIC, callback=self.display_loading)
            
        
    def stop_timer(self):
        if self.timer:
            self.timer.deinit()
            self.timer = None
        self.reset()
        self.step = 0

    def start_blinking(self, num1, num2=None, col = 0, interval_ms = 1000):
        self.stop_timer()
        if not self.timer:
            self.reset()
            self.timer = Timer(-1)
            self.timer.init(period = interval_ms, mode = Timer.PERIODIC, callback = lambda t: self.blink(t, num1, num2, col))


    def blink(self, t, num1, num2, col):
        if num2:
            if self.step % 4 == 0:
                self.numbers(num1, None)
            elif self.step % 4 == 2:
                self.numbers(num2, col)
            else:
                self.reset()
        else:
            if self.step % 2:
                self.numbers(num1, col)
            else:
                self.reset()

        self.step += 1
