from ChessBoard import *
from abc import ABC, abstractmethod
import numpy as np
import copy
from JudgmentStrategy import *

class AbstractPlayer(ABC):
    def __init__(self, player) -> None:
        super().__init__()
        self.player = player
    @abstractmethod
    def getStep(self, chessboard):
        pass

class FIRAI_A(AbstractPlayer):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.judgment = FIRJudgment()

    def getStep(self, chessboard):
        point = np.where(chessboard.board == 0)
        randomize = np.arange(len(point[0]))  #创建一个整数序列
        np.random.shuffle(randomize)  #打乱整数序列
        for i in randomize:
            x = point[0][i]
            y = point[1][i]
            if(self.judgment.isOk(chessboard,x,y,True)):
                return x,y
        
        return -1,-1
    


class WeiQiAI_A(AbstractPlayer):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.judgment = WeiqiJudgment()

    def getStep(self, chessboard):
        point = np.where(chessboard.board == 0)
        randomize = np.arange(len(point[0]))  #创建一个整数序列
        np.random.shuffle(randomize)  #打乱整数序列
        for i in randomize:
            x = point[0][i]
            y = point[1][i]
            if(self.judgment.isOk(chessboard,x,y,True)):
                return x,y
        return -1,-1

class ReversiAI_A(AbstractPlayer):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.judgment = ReversiJudgment()

    def getStep(self, chessboard):
        point = np.where(chessboard.board == 0)
        randomize = np.arange(len(point[0]))  #创建一个整数序列
        np.random.shuffle(randomize)  #打乱整数序列
        for i in randomize:
            x = point[0][i]
            y = point[1][i]
            if(self.judgment.test(chessboard,x,y,True)):
                return x,y
        return -1,-1



class FIRAI_B(AbstractPlayer):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.judgment = FIRJudgment()
        self.level = 15
        self.grade = 10
        self.MAX = 1008611

    def getStep(self, chessboard):
        self.level = chessboard.w
        if(chessboard.nstep < 2):
            point = np.where(chessboard.board == 0)
            randomize = np.arange(len(point[0]))  #创建一个整数序列
            np.random.shuffle(randomize)  #打乱整数序列
            for i in randomize:
                x = point[0][i]
                y = point[1][i]
                if(self.judgment.isOk(chessboard,x,y,True)):
                    print("随机落子{},{}".format(x,y))
                    return x,y
        else:
            x,y = self.BetaGo(chessboard)
            print(x,y)
            return x,y
        
        return -1,-1

    def Scan(self, chessboard, player):
        shape = [[[0 for high in range(5)] for col in range(self.level)] for row in range(self.level)]
        # 扫描每一个点，然后在空白的点每一个方向上做出价值评估！！
        for i in range(self.level):
            for j in range(self.level):

                # 如果此处为空 那么就可以开始扫描周边
                if chessboard.board[i][j] == 0:
                    m = i
                    n = j
                    # 如果上方跟当前传入的颜色参数一致，那么加分到0位！
                    while n - 1 >= 0 and chessboard.board[m][n - 1] == player+1:
                        n -= 1
                        shape[i][j][0] += self.grade
                    if n-1>=0 and chessboard.board[m][n - 1] == 0:
                        shape[i][j][0] += 1
                    if n-1 >= 0 and chessboard.board[m][n - 1] == (player+1)%2+1:
                        shape[i][j][0] -= 2
                    m = i
                    n = j
                    # 如果下方跟当前传入的颜色参数一致，那么加分到0位！
                    while (n + 1 < self.level  and chessboard.board[m][n + 1] == player+1):
                        n += 1
                        shape[i][j][0] += self.grade
                    if n + 1 < self.level  and chessboard.board[m][n + 1] == 0:
                        shape[i][j][0] += 1
                    if n + 1 < self.level  and chessboard.board[m][n + 1] == (player+1)%2+1:
                        shape[i][j][0] -= 2
                    m = i
                    n = j
                    # 如果左边跟当前传入的颜色参数一致，那么加分到1位！
                    while (m - 1 >= 0 and chessboard.board[m - 1][n] == player+1):
                        m -= 1
                        shape[i][j][1] += self.grade
                    if m - 1 >= 0 and chessboard.board[m - 1][n] == 0:
                        shape[i][j][1] += 1
                    if m - 1 >= 0 and chessboard.board[m - 1][n] == (player+1)%2+1:
                        shape[i][j][1] -= 2
                    m = i
                    n = j
                    # 如果右边跟当前传入的颜色参数一致，那么加分到1位！
                    while (m + 1 < self.level  and chessboard.board[m + 1][n] == player+1):
                        m += 1
                        shape[i][j][1] += self.grade
                    if m + 1 < self.level  and chessboard.board[m + 1][n] == 0:
                        shape[i][j][1] += 1
                    if m + 1 < self.level  and chessboard.board[m + 1][n] == (player+1)%2+1:
                        shape[i][j][1] -= 2
                    m = i
                    n = j
                    # 如果左下方跟当前传入的颜色参数一致，那么加分到2位！
                    while (m - 1 >= 0 and n + 1 < self.level  and chessboard.board[m - 1][n + 1] == player+1):
                        m -= 1
                        n += 1
                        shape[i][j][2] += self.grade
                    if m - 1 >= 0 and n + 1 < self.level  and chessboard.board[m - 1][n + 1] == 0:
                        shape[i][j][2] += 1
                    if m - 1 >= 0 and n + 1 < self.level  and chessboard.board[m - 1][n + 1] == (player+1)%2+1:
                        shape[i][j][2] -= 2
                    m = i
                    n = j
                    # 如果右上方跟当前传入的颜色参数一致，那么加分到2位！
                    while (m + 1 < self.level  and n - 1 >= 0 and chessboard.board[m + 1][n - 1] == player+1):
                        m += 1
                        n -= 1
                        shape[i][j][2] += self.grade
                    if m + 1 < self.level  and n - 1 >= 0 and chessboard.board[m + 1][n - 1] == 0:
                        shape[i][j][2] += 1
                    if m + 1 < self.level  and n - 1 >= 0 and chessboard.board[m + 1][n - 1] == (player+1)%2+1:
                        shape[i][j][2] -= 2
                    m = i
                    n = j
                    # 如果左上方跟当前传入的颜色参数一致，那么加分到3位！
                    while (m - 1 >= 0 and n - 1 >= 0 and chessboard.board[m - 1][n - 1] == player+1):
                        m -= 1
                        n -= 1 
                        shape[i][j][3] += self.grade
                    if m - 1 >= 0 and n - 1 >= 0 and chessboard.board[m - 1][n - 1] == 0:
                        shape[i][j][3] += 1
                    if m - 1 >= 0 and n - 1 >= 0 and chessboard.board[m - 1][n - 1] == (player+1)%2+1:
                        shape[i][j][3] -= 2
                    m = i
                    n = j
                    # 如果右下方跟当前传入的颜色参数一致，那么加分到3位！
                    while m + 1 < self.level  and n + 1 < self.level  and chessboard.board[m + 1][n + 1] == player+1:
                        m += 1
                        n += 1
                        shape[i][j][3] += self.grade
                    if m + 1 < self.level  and n + 1 < self.level  and chessboard.board[m + 1][n + 1] == 0:
                        shape[i][j][3] += 1
                    if m + 1 < self.level  and n + 1 < self.level  and chessboard.board[m + 1][n + 1] == (player+1)%2+1:
                        shape[i][j][3] -= 2
        return shape


    def Sort(self, shape):
        for i in shape:
            for j in i:
                for x in range(5):
                    for w in range(3, x - 1, -1):
                        if j[w - 1] < j[w]:
                            temp = j[w]
                            j[w - 1] = j[w]
                            j[w] = temp
        print("This Time Sort Done !")
        return shape


    def Evaluate(self, shape):
        for i in range(self.level):
            for j in range(self.level):

                if shape[i][j][0] == 4:
                    return i, j, self.MAX
                shape[i][j][4] = shape[i][j][0]*1000 + shape[i][j][1]*100 + shape[i][j][2]*10 + shape[i][j][3]
        max_x = 0
        max_y = 0
        max = 0
        for i in range(self.level):
            for j in range(self.level):
                if max < shape[i][j][4]:
                    max = shape[i][j][4]
                    max_x = i
                    max_y = j
        print("the max is "+ str(max) + " at ( "+ str(max_x)+" , "+str(max_y)+" )")
        return max_x, max_y, max

    def BetaGo(self, chessboard):
        
        shape_P = self.Scan(chessboard, (chessboard.nstep+1)%2)
        shape_C = self.Scan(chessboard, chessboard.nstep%2)
        shape_P = self.Sort(shape_P)
        shape_C = self.Sort(shape_C)
        max_x_P, max_y_P, max_P = self.Evaluate(shape_P)
        max_x_C, max_y_C, max_C = self.Evaluate(shape_C)
        if max_P>max_C and max_C<self.MAX:
            return max_x_P,max_y_P
        else:
            return max_x_C,max_y_C


