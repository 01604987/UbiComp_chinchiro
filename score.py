import random

class Score:

    #-1 = hifumi
    # 0 = no hit
    # 1 = hit 1
    # 2 = hit 2
    # 3 = hit 3
    # 4 = hit 4
    # 5 = hit 5
    # 6 = hit 6
    # 7 = hit 456
    # 111 = hit 111
    # 222 = hit 222
    # 333 = hit 333
    # 444 = hit 444
    # 555 = hit 555
    # 666 = hit 666  
     
    def __init__(self) -> None:
        # index 0 = my_score, index 1 = op_score
        #self.score = [0, 0]
        self.my_nums = []
        self.op_nums = []


    def reset_score(self):
        #self.score.clear()
        #self.score.extend((0, 0))
        self.my_nums.clear()
        self.op_nums.clear()

    
    def roll_dice(self, dice):
        # random 3 numbers
        self.my_nums.clear()
        counter = 1
        while True:
            rand = random.getrandbits(4)

            if rand < 12:
                self.my_nums.append(rand % 6 + 1)
                counter += 1
            if counter > dice:
                break


    def check_score(self, player) -> int:
        num = None
        if player == 0:
            num = tuple(sorted(self.my_nums))
        else:
            num = tuple(sorted(self.op_nums))

        if len(num) != 3:
            print("Error: Expected exactly three numbers")
            raise Exception
        
        # check for hit
        if num[0] == num[1]:
            # check for zorome
            if num[0] == num[2]:
                return int(''.join(map(str, num)))
                #self.score[player] = int(''.join(map(str, num)))
            # hit is last number
            else:
                #self.score[player] = num[2]
                return num[2]
        
        # check for hit
        if num[1] == num[2]:
            # hit is first number
            #self.score[player] = num[0]
            return num[0]
        
        if num[0] == 4 and num[1] == 5 and num[2] == 6:
            #self.score[player] = 7
            return 7

        # check for hifumi
        if num[0] == 1 and num[1] == 2 and num[2] == 3:
            # self.score[player] = -1
            return -1
        # else no hit
        else:
            # self.score[player] = 0
            return 0

    def list_to_nums(self):
        concat_nums = ''.join(map(str, self.my_nums))
        val = int(concat_nums)
        return val    
          
    def nums_to_list(self, nums):
        self.op_nums.clear()
        self.op_nums.extend(int(d) for d in str(nums))
