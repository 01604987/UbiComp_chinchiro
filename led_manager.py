from micropython import const
from neopixel import NeoPixel
from machine import Timer


#               "red",   "green",   "blue",    "yellow",   "purple", "turkoise"
LIGHTS = const(((3,0,0), (0,4,0), (0,0,4), (2,2,0), (2,0,2), (0,2,2)))
NUMS = [[], [3], [0, 6], [2, 3, 4], [0, 2, 4, 6], [0, 2, 3, 4, 6], [0, 1, 2, 4, 5, 6]]
LOADING = const((15, 17, 19, 5, 3, 1))

class Led:

    def __init__(self, data_p, p_nr) -> None:
        self.np = NeoPixel(data_p, p_nr)
        self.sleep_time_ms = 1000
        self.timer = None
        self.step = 0
        self.col = LIGHTS[0]

    def reset_light(self) -> None:
        self.np.fill((0, 0, 0))
        self.np.write()
        

    # expect num to be well formed chinchiro valid dice rolls
    def numbers (self, num):
        if not isinstance (num, list):
            print("Not a list")
            raise Exception
        
        self.reset()

        for i, val in enumerate(num):
            offset = i * int(len(self.np)/ 3)
            for i in NUMS[val]:
                self.np[i + offset] = self.col
        
        self.np.write()

    # TODO change/add to pingpong animation
    def display_loading(self, t):
        self.np[LOADING[self.step % 6]] = self.col
        self.np[LOADING[(self.step - 1) % 6]] = (0, 0, 0)
        self.step += 1
        self.np.write()



    def start_loading(self, interval_ms = 1000):
        self.stop_loading()
        if not self.timer:
            self.timer = Timer(-1)
            self.timer.init(period=interval_ms, mode=Timer.PERIODIC, callback=self.display_loading)
            self.reset()
        
    
    def stop_loading(self):
        if self.timer:
            self.timer.deinit()
            self.timer = None
        self.reset()
        self.step = 0
