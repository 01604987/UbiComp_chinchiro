from lib.dfplayermini import Dfplayer

class Audio:

    def __init__(self, player_addr_0, player_addr_1 = None) -> None:
        self.player_0 = None
        self.player_1 = None
        self.player_0_addr = player_addr_0
        self.player_1_addr = player_addr_1

        self.initialize()
    
    def initialize(self):
        if self.player_0_addr:
            self.player_0 = Dfplayer(self.player_0_addr)
        if self.player_1_addr:
            self.player_1 = Dfplayer(self.player_1_addr)

    def volume(self, volume):
        if self.player_0:
            self.player_0.volume(volume)
        if self.player_1:
            self.player_1.volume(volume)
    
    def reset(self):
        if self.player_0:
            self.player_0.module_reset()
        if self.player_1:
            self.player_1.module_reset()

    def play(self, player):
        if player:
            #self.player1._fadeout_timer.deinit()
            #self.player1.volume(self.player1._max_volume)
            #self.player2.fadeout()
            if self.player_0:
                self.player_0.play(1)
            
        else:
            #self.player2._fadeout_timer.deinit()
            #self.player2.volume(self.player2._max_volume)
            #self.player1.fadeout()
            if self.player_1:
                self.player_1.play(3)
