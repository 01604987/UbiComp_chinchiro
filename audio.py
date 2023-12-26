class Audio:

    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2


    def play(self, player):
        if player:
            #self.player1._fadeout_timer.deinit()
            #self.player1.volume(self.player1._max_volume)
            #self.player2.fadeout()
            self.player1.play(1)
            
        else:
            #self.player2._fadeout_timer.deinit()
            #self.player2.volume(self.player2._max_volume)
            #self.player1.fadeout()
            self.player2.play(3)
