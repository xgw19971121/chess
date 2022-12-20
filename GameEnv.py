from abc import ABC,abstractmethod
import numpy as np
from ChessBoard import *
from JudgmentStrategy import *
from Memento import *
import os

class GameFactory(ABC):
    def __init__(self, h, w, type, nameList) -> None:
        self.h = h
        self.w = w
        self.chessboard = None
        self.judment = None
        self.orignator = None
        self.caretaker = None
        self.nameList = None
        self.gameover = False
        self.winId = 0
        self.n_undo = [True,True]
        self.start(h,w,type,nameList)

    def start(self, h, w, type, nameList):
        self.h = h
        self.w = w
        self.nameList = nameList
        self.gameover = False
        self.n_undo = [True,True]
        
        if(type == 0): # 五子棋模式
            print("五子棋模式")
            self.chessboard = WeiqiBoard(self.w, self.h, self.nameList)
            self.judment = FIRJudgment()
            self.orignator = ChessOriginator(self.chessboard)
            self.caretaker = ChessCaretaker()
        elif(type == 1): # 围棋
            print("围棋模式")
            self.chessboard = WeiqiBoard(self.w, self.h, self.nameList)
            self.judment = WeiqiJudgment()
            self.orignator = ChessOriginator(self.chessboard)
            self.caretaker = ChessCaretaker()
        self.caretaker.pushMemento(self.orignator.save())


    def step(self, x, y, flag=True):
        """走一步，返回操作是否成功，以及胜者"""
        if(self.gameover):
            print("游戏已经结束")
            return True, self.winId
        if(self.judment.isOk(self.chessboard, x, y, flag)):
            self.chessboard.step(x, y, flag)
            self.caretaker.pushMemento(self.orignator.save())
        else:
            return False, -1
        self.winId = self.judment.victory(self.chessboard, x, y, flag)
        if(self.winId != -1):
            self.gameover = True
            if(self.winId == 2):
                print("平局")
            else:
                print("当前胜者为{}".format(self.nameList[self.chessboard.nstep%2]))
                
        return True, self.winId

    def save(self, id = 0):
        return self.caretaker.saveInPkl(id)

    def restore(self, id = 0):
        if(self.caretaker.restoreFromPkl(id) == False):
            return False

        self.orignator.restore(self.caretaker.topMemento())
        self.chessboard = self.orignator.chessBoard
        return True

    def savelist(self):
        path = "./save/"
        return os.listdir(path)

    def giveup(self):
        if(self.gameover):
            print("游戏已经结束")
        self.gameover = True
        self.winId = (self.chessboard.nstep+1)%2
        return self.winId

    def undo(self):
        if(self.caretaker.getSize() <= 2 or self.n_undo[self.chessboard.nstep%2] == False):
            return False
        self.n_undo[self.chessboard.nstep%2] = False
        self.caretaker.popMemento()
        self.caretaker.popMemento()
        self.orignator.restore(self.caretaker.topMemento())
 
        self.chessboard = self.orignator.chessBoard
        return True

    def show(self):
        print("当前玩家为{}".format(self.nameList[self.chessboard.nstep%2]))
        print(self.chessboard.board)
