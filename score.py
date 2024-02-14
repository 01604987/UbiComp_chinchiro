from micropython import const

class Score:

    SCORE_TABLE = const((None, 0, 1, 2, 3, 4, 5, 6, 7, 8))
    
    def __init__(self) -> None:
        self.my_score = 0
        self.op_score = 0
        self.my_nums = [0, 0, 0]
        self.op_nums = [0, 0, 0]


    def reset_score(self):
        self.my_score = 0
        self.op_score = 0
        self.my_nums = [0, 0, 0]
        self.op_nums = [0, 0, 0]


    def check_score(self, player) -> int:
        num = None
        if player:
            num = self.my_nums.copy()
        else:
            num = self.op_nums.copy()
        
        num.sort()
        # check for hit
        if num[0] == num[1]:
            # check for zorome
            if num[0] == num[2]:
                self.my_score = int(''.join(map(str, num)))
            # hit is last number
            else:
                self.score = num[2]
            return 1
        
        # check for hit
        if num[1] == num[2]:
            # hit is first number
            self.my_score = num[0]
            return 1
        
        # check for hifumi
        if num[0] == 1 and num[1] == 2 and num[2] == 3:
            self.my_score = -1
            return 1
        # else no hit
        else:
            self.my_score = 0
            return 0
            