from abc import ABC, abstractmethod
import numpy as np

class AbstractChessBoard(ABC):
    def __init__(self, w, h, nameList):
        super().__init__()
        self.w = w
        self.h = h
        self.nameList = nameList # 用户名字列表
        self.board = np.zeros((h,w),dtype=int)
        self.nstep = 0 # 当前棋手序号0-1
        self.piece = (0,1,2) # 棋子标识

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def step(self, x, y, flag):
        pass


class WeiqiBoard(AbstractChessBoard):
    def __init__(self, w, h, nameList):
        super().__init__(w, h, nameList)
        self.ko = [0,0,0]

    def show(self):
        print("当前玩家{}".format(self.nameList[self.nstep%2]))
        print(self.board)

    def step(self, x, y, flag):
        if(flag):
            self.board[x,y] = self.piece[self.nstep%2+1]
        self.nstep = self.nstep+1