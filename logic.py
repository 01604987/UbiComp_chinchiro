from state_manager import MENU_S, State
from led_manager import LIGHTS, Led
from audio import Audio
from buttons_adc import Buttons_ADC
from shake import Shake
from distance import Distance
from score import Score
from time import sleep
from connection import Connection
from net import Server
from micropython import mem_info
import random
import gc


class EndGame(Exception):
    pass

class Logic:

    def __init__(self, btns:Buttons_ADC, s_m:State, led:Led , audio: Audio ,network: Server = None, shake: Shake = None, distance: Distance = None, vibration = None, conn:Connection = None) -> None:
        self.btns = btns
        # state_manager
        self.s_m = s_m
        self.network = network
        self.network_active = 0
        # reset or game ended trigger
        self.rst = 0
        self.led = led
        self.audio = audio
        self.shake = shake
        self.distance = distance
        self.score = Score()
        self.conn = conn

    def start(self):
        while True:
            self._menu_select()
            try:
                self._game()
            except EndGame:
                self.reset_logic()
                pass

    def _menu_select(self):
        # on right button press light up different light configs
        # on left button press blink for confirmation

        self.btns.set_btn_irq("right", self._step_menu_ADC)
        self.btns.set_btn_irq("left", self._choose_menu_ADC)
        
        # TODO implement options handling like voice assistance or language?
        # TODO add debug option that activates webrepl
        while True:
            sleep(0.01)
            self.btns.poll_adc()
            # check button menu selection
            if self.btns.get_l_pressed():
                self.s_m.set_menu_state(self.btns.get_r_pressed(len(MENU_S)))
                break


    def _game(self):
        self._init_game()

        # led light determined by right button presse counter
        #! replace with for loop max length 3
        for i in range(3):
            try:
                gc.collect()
                self.s_m.set_game_state("initiate")
                self._initiate()

                self.s_m.set_game_state("shaking")
                self._shaking()

                gc.collect()
                self.s_m.set_game_state("result")
                hit = self._result()
                result = self.score.my_nums              
                # if multiplayer
                if self.s_m.get_menu_state():
                    try:
                        self.network.send_tcp_data(self.list_to_num(result))
                    except OSError as err:
                        print("Err sending result tcp", err)

                gc.collect()
                print(self.score.my_nums)
                if hit:
                    print("Ending turn")
                    break
            except EndGame as err:
                print(f"Ending Game")
                sleep(1)
                raise EndGame
            
            except Exception as err:
                print(f"Exception in game with err code {str(err)}")
                raise Exception
                
        raise EndGame
    
    #! HANDLE ECONRESET
    def _init_multiplayer(self):
        while not self.conn.connect():
            print('connecting to wifi')
            self._poll_btns()
            # do something blink or led
            # allow end game/break
            sleep(1.5)

        print("connected to wifi")
        print(self.conn.net.ifconfig())
        try:
            self.network.init_tcp()
        except Exception as err:
            print(str(err))
            raise

        while not self.network.accept_conn():
            self._poll_btns()
            print('awaiting incomming connection')
            # do led loading etc..
            # allow end game/break
            sleep(1)
        print("socket established")
        print(self.network.client_tcp_address)

        self.s_m.curr_turn = self._establish_start()
        print("My Turn" if self.s_m.curr_turn else "Op Turn")

        self.network.init_udp()

        #self.network.deinit_tcp()

    #! HANDLE ECONRESET
    def _establish_start(self):
        while True:
            self._poll_btns()
            
            my_num = self.score.roll_1()
            # show my num on led left in blue
            print(f"my rolled num: {my_num}")
            self.network.send_tcp_data(my_num)
            print("data sent")
            while not (op_num := self.network.receive_tcp_data()):
                print("await response")
                sleep(1)

            print (f"op rolled num: {op_num}")
            
            # show op num on led right in red

            # sleep 0.5

            if my_num > op_num:
                # blink left
                return 1
            elif my_num < op_num:
                # blink right
                return 0

            # clear led, reroll
    
    #! maybe merge with initialize
    def _init_game(self):
        # setup distance sensor
        self.btns.set_btn_irq("right", None)
        self.btns.set_btn_irq("left", self._end_game_ADC)
        self.distance.initialize()


        #! todo impl button to exit network
        # initiate game state
        
        
        state = self.s_m.get_menu_state()

        if state == 0:
            # single player
            self.network_active = None
        if state == 1:
            # multiplayer
            self.conn.init()
            self._init_multiplayer()
       

        self.audio.volume(20)
        

    def _initiate(self):
        # setup timer to periodically blink stuff
        while True:
            self._poll_btns()
            sleep(0.1)
            if self.distance.static():
                print('ready for pickup')
                break

            #! LED indicating setting down device

        sleep(1)

        while True:
            self._poll_btns()
            sleep(0.1)

            # if sensor measure > interval
            if self.distance.pick_up():
                # stop any blinking leds, timers or sound effect that are designed only for initial
                print('ready for shaking')
                break
        sleep(1)
        
    def _shaking(self):
        
        #! set button irq for shaking
        self.shake.initialize_module()
        sleep(0.5)
        shake_counter = 0
        while True:
            self._poll_btns()
            # poll accel values
            try:
                self.shake.update()
            except Exception as err:
                print(f"here wiht err {err}")
 
            # detect axis being shaken
            axis = self.shake.get_axis()
            
            if axis == None:
                # DEBUG
                # TODO add button to for simulating distance sensor
                if self.distance.static() and shake_counter != 0:
                    print("Ending shaking")
                    #! play dice done shaking sound
                    break
                # no shaking or undefined axis
                continue

            # faster skip on no shake 
            if abs(self.shake.values[axis][0]) >= abs(self.shake.values[axis][3]):
                continue 


            #! detect micro shake
            # micro shake has max audio volume cap because values very high

            #! shake detection on sign change
            if self.shake.values[axis][1] == 0:
                continue
            
            # max value divided by last value = negative => sign changed == shake detected
            sign_inverse = self.shake.values[axis][3] / self.shake.values[axis][1]
            
            
                
            try:
                if sign_inverse <= 0:
                    
                    print(axis)
                    shake_counter += 1
                    if shake_counter % 6 == 0:
                        self.audio.volume(20)
                    # reset max value
                    self.shake.values[axis][3] = 0
                    if self.s_m.get_menu_state():
                        self.network.send_udp_data(shake_counter)

                    #! calculate magnitude

                    #! set audio volume
                    
                    #! change led dice

                    # play the correct audio with correct audio channel
                    # left, right, up, down based on axis.
                    # if axis == 0 and values[0][0] <= 0 -> left
                    # axis == 1 ? -> diagonal or left, right, up, down

                    #! play audio
                    if self.shake.values[axis][0] <= 0:
                        print("left")
                        self.audio.play(0)
                    else:
                        print("right")
                        self.audio.play(1)
                    #! start vibration
                        
                    #! send udp package
                    #sleep(0.05)
            
            except Exception as err:
                print(f"Exception during shaking with err code {str(err)}")

    def _result(self):
        # random 3 numbers
        counter = 0
        while True:
            rand = random.getrandbits(4)

            if rand < 12:
                self.score.my_nums[counter] = rand % 6 + 1
                counter += 1
            if counter > 2:
                break
        
        # check if numbers clears table
        if self.score.check_score(1):
            return 1

        return 0

            


    def _poll_btns(self):
        self.btns.poll_adc()
        if self.rst:
            raise EndGame

    def reset_logic(self):
        if self.network.connected_tcp:
            self.network.send_tcp_data(13)

        self.btns.reset_buttons()
        self.s_m.reset_state()
        self.rst = 0
        #self.network = None
        self.shake.reset_values()
        self.shake.deinitialize()
        self.audio.reset()
        self.btns.reset_db_t()
        self.score.reset_score()
        self.network.deinit_tcp()
        gc.collect()



    ##################################################################################################################
    # irq for button presses are defined here
    # ADC buttons
    
    def _step_menu_ADC(self, t):
        if self.btns.check_btn_val(1):
            self.btns.r_pressed += 1
            print(f"Current menu counter: {self.btns.r_pressed}")
            self.btns.hold = 1
        self.btns.reset_db_t()
        
    def _choose_menu_ADC(self, t):
        if self.btns.check_btn_val(0):
            self.btns.l_pressed = 1
            self.btns.hold = 1
        self.btns.reset_db_t()
    
    def _end_game_ADC(self, t):
        if self.btns.check_btn_val("left"):
            print(f"Ending current game")
            self.btns.hold = 1
            self.rst = 1
    
    
# UTILS-----------------------------------
        
    def list_to_num(self, nums :list):
        concat_nums = ''.join(map(str, nums))
        val = int(concat_nums)
        return val
