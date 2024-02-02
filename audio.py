from lib.dfplayermini import Dfplayer

class Audio:

    def __init__(self, player_addr_0, player_addr_1 = None) -> None:
        self.player_0 = Dfplayer(player_addr_0)
        if player_addr_1 is not None:
            self.player_1 = Dfplayer(player_addr_1)
            self.modules = 2
        else:
            self.modules = 1


    def play(self, player):
        if player:
            #self.player1._fadeout_timer.deinit()
            #self.player1.volume(self.player1._max_volume)
            #self.player2.fadeout()
            self.player_0.play(1)
            
        else:
            #self.player2._fadeout_timer.deinit()
            #self.player2.volume(self.player2._max_volume)
            #self.player1.fadeout()
            self.player_1.play(3)
