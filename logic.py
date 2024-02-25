# from led_manager import LIGHTS, Led
# from audio import Audio
# from buttons_adc import Buttons_ADC
# from shake import Shake
# from distance import Distance
# from connection import Connection
# from net import Server
# from micropython import const, mem_info
from state_manager import MENU_S, State
from score import Score
from time import sleep
import gc


class EndGame(Exception):
    pass

class Logic:

    def __init__(self, btns, s_m, led , audio ,network = None, shake = None, distance = None, vibration = None, conn = None) -> None:
        self.btns = btns
        # state_manager
        self.s_m = s_m
        self.network = network
        self.network_active = False
        # reset or game ended trigger
        self.led = led
        self.audio = audio
        self.shake = shake
        self.distance = distance
        self.score = Score()
        self.conn = conn

    # def __init__(self, btns:Buttons_ADC, s_m:State, led:Led , audio: Audio ,network: Server = None, shake: Shake = None, distance: Distance = None, vibration = None, conn:Connection = None) -> None:
    #     self.btns = btns
    #     # state_manager
    #     self.s_m = s_m
    #     self.network = network
    #     self.network_active = False
    #     # reset or game ended trigger
    #     self.led = led
    #     self.audio = audio
    #     self.shake = shake
    #     self.distance = distance
    #     self.score = Score()
    #     self.conn = conn

    def start(self):
        while True:
            self._menu_select()
            try:
                self._game()
            except EndGame:
                print("Ending Game")
                sleep(0.1)
                if self.network_active:
                    print("sending end game over tcp")
                    self.network.send_tcp_data(14)
                    sleep(2)
                self.reset_logic()
                pass

    def _menu_select(self):
        # on right button press light up different light configs
        # on left button press blink for confirmation

        self.btns.set_btn_irq(1, self.btns._step_menu_ADC)
        self.btns.set_btn_irq(0, self.btns._choose_menu_ADC)
        
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

        while True:
            for i in range(3):
                try:
                    gc.collect()
                    self.s_m.set_game_state("initiate")
                    if self.s_m.my_turn:
                        self._initiate()

                    self.s_m.set_game_state("shaking")
                    if self.s_m.my_turn:
                        self._shaking()

                    if not self.s_m.my_turn:
                        # check udp, check tcp in loop
                        # if got tcp message break out of loop/ return from loop
                        pass

                    gc.collect()
                    self.s_m.set_game_state("result")
                    # both my turn + op turn:
                    # my turn = calculate result
                    # op turn = await for my result and calculate result/score
                    self._result()       

                    
                    
                    gc.collect()
                    # self.s_m.my_turn = 1 if my turn. self.score.score[1] is op_score.
                    #if self.score.score[not self.s_m.my_turn]:
                    if self.score.check_score(not self.s_m.my_turn):
                        print("Ending turn")
                        break
                except EndGame:
                    raise
                except Exception as err:
                    print(f"Exception in game with err code {str(err)}")
                    raise Exception
                
            
            # op_nums none during single player
            if self.score.my_nums and self.score.op_nums:
                # calculate winner & display blinking
                self._calculate_winner()
                # display score
                # speak out score

                sleep(4)
                # flush all nums and scores
                self.score.reset_score()


            # change turns
            #self._change_turns()
            if self.network_active:
                self.s_m.my_turn = not self.s_m.my_turn
            

    #! HANDLE ECONRESET
    def _init_multiplayer(self):
        self.led.start_loading(300)
        while not self.conn.connect():
            print('connecting to wifi')
            self._poll_btns()
            # do something blink or led
            # allow end game/break
            sleep(1)

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
        self.led.stop_timer()
        self.s_m.my_turn = self._establish_start()
        print("My Turn" if self.s_m.my_turn else "Op Turn")

        self.network.init_udp()

        #self.network.deinit_tcp()

    #! HANDLE ECONRESET
    def _establish_start(self):
        while True:
            self.score.reset_score()
            self.score.roll_dice(1)
            # show my num on led left in blue
            print(f"my rolled num: {self.score.my_nums[0]}")
            self.network.send_tcp_data(self.score.my_nums[0])
            print("data sent")
            while not (op_num := self.network.receive_tcp_data()):
                self._poll_btns()
                print("await response")
                sleep(1)

            print (f"op rolled num: {op_num}")
            
            # show op num on led right in red

            # sleep 0.5

            if self.score.my_nums[0] > op_num:
                # blink left
                self.score.reset_score()
                return 1
            elif self.score.my_nums[0] < op_num:
                # blink right
                self.score.reset_score()
                return 0

            # clear led, reroll
    
    #! maybe merge with initialize
    def _init_game(self):
        # setup distance sensor
        self.btns.set_btn_irq(1, None)
        self.btns.set_btn_irq(0, self.btns._end_game_ADC)
        self.distance.initialize()


        #! todo impl button to exit network
        # initiate game state
        

        if self.s_m.curr_menu_state == 0:
            # single player
            self.network_active = False
            self.s_m.my_turn = 1
        if self.s_m.curr_menu_state == 1:
            # multiplayer
            self.conn.init()
            self._init_multiplayer()
            self.network_active = True
       

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
            axis = self.shake.axis
            
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
                    if self.network_active:
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
        # only generate if it is my turn
        # if not my turn pass and receive

        if self.s_m.my_turn:
            self.score.roll_dice(3)
            
            self.led.numbers(self.score.my_nums)

            # check if numbers clears table
            self.score.check_score(0)
            
            sleep(3)

            # if multiplayer
            if self.network_active:

                self.network.send_tcp_data(self.score.list_to_nums())
                self.wait_for_ack()           

            print('My dice: ', self.score.my_nums)
        
        else:
            # check for op_nums
            while not (op_nums := self.network.receive_tcp_data()):
                self._poll_btns()
                print("listening")
                sleep(0.1)
            # not my turn, I play loading during result
            self.led.stop_timer()
            if op_nums == 14:
                raise EndGame
            print("Opponent rolled: ", op_nums)
            self.score.nums_to_list(op_nums)
            self.led.numbers(self.score.op_nums)
            # send ack of package
            self.network.send_tcp_data(11)
            sleep(3)
            

    def _calculate_winner(self):
        if self.score.check_score(0) > self.score.check_score(1):
            # if my_win : red display my_num
            print('red', self.score.my_nums)
            self.led.start_blinking(self.score.my_nums, interval_ms = 500)

        elif self.score.check_score(0) < self.score.check_score(1):
            # if op_win : blue display op_num
            print('blue', self.score.op_nums)
            self.led.start_blinking(self.score.op_nums, col = 2, interval_ms = 500)

        else:
            # can both be no hit = same score
            print('red', self.score.my_nums, 'blue', self.score.op_nums)
            # alternate blinking red, blue
            self.led.start_blinking(self.score, num1 = self.score.my_nums, num2 = self.score.op_nums, col = 2, interval_ms = 500)


    # def _change_turns(self):
    #     if self.network_active:
    #         if self.s_m.my_turn:
    #             # send turn end signal
    #             self.network.send_tcp_data(12)
    #             # await ack
    #             self.wait_for_ack()
            
    #         else:
    #             while not (code := self.network.receive_tcp_data()):
    #                 print('waiting for turn end')
    #                 self._poll_btns()
    #                 sleep(0.1)
    #             if code == 14:
    #                 raise EndGame
    #             # turn end
    #             elif code == 12:
    #                 pass
    #             print(code)
    #             #self.score.reset_score()
    #             self.network.send_tcp_data(11)

    #         self.s_m.my_turn = not self.s_m.my_turn

    def _poll_btns(self):
        self.btns.poll_adc()
        if self.btns.rst:
            raise EndGame
        
    def wait_for_ack(self):
        while not (ack := self.network.receive_tcp_data()):
            sleep(0.1)
            print('waiting for ack')
            self._poll_btns()
        if ack == 11:
            pass
        else: raise EndGame

    def reset_logic(self):
        self.led.stop_timer()
        self.btns.reset_buttons()
        self.s_m.reset_state()
        self.btns.rst = 0
        #self.network = None
        self.shake.reset_values()
        self.shake.deinitialize()
        self.audio.reset()
        self.score.reset_score()
        self.network.deinit_tcp()
        self.conn.deinit()
        gc.collect()
