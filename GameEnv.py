from abc import ABC,abstractmethod
import numpy as np
from ChessBoard import *
from JudgmentStrategy import *
from Memento import *
import os
import pickle

class GameFactory(ABC):
    def __init__(self, h, w, type, nameList) -> None:
        self.h = h
        self.w = w
        self.chessboard = None
        self.judment = None
        self.orignator = None
        self.caretaker = None
        self.nameList = nameList
        self.gameover = False
        self.winId = 0
        self.n_undo = [True,True]
        self.type = type
        self.start(h,w,self.type)

    def start(self, h, w, type):
        self.h = h
        self.w = w
        self.gameover = False
        self.n_undo = [True,True]
        self.type = type
        
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
        elif(type == 2): #黑白棋
            print("黑白棋模式")
            self.chessboard = ReversiBoard(8, 8, self.nameList)
            self.judment = ReversiJudgment()
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
            print("落子错误")
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
        return self.caretaker.saveInPkl(self.nameList[self.chessboard.nstep%2], self.type)

    def restore(self, play = False, id = 0):
        if(self.caretaker.restoreFromPkl(self.nameList[self.chessboard.nstep%2], self.type) == False):
            return False
        if(play):
            self.orignator.restore(self.caretaker.getMemento(0))
        else:
            self.orignator.restore(self.caretaker.topMemento())
        self.chessboard = self.orignator.chessBoard
        self.w = self.chessboard.w
        self.h = self.chessboard.h
        self.gameover = False
        return True
    
    def restoreIndex(self,round):
        if(round < self.caretaker.getSize()):
            self.orignator.restore(self.caretaker.getMemento(round))
            self.chessboard = self.orignator.chessBoard
            return True
        return False

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


class GameProxy(GameFactory):
    def __init__(self, h, w, type, nameList) -> None:
        super().__init__(h, w, type, nameList)
        self.GameEnv = None
        self.path = "account/"
        self.file = self.path+"account.pkl"
        self.Account = {}
        if(os.path.exists(self.path) is False):
            os.makedirs(self.path)
        try:
            with open(self.file, 'rb') as f:
                self.Account = pickle.load(f)
                print("加载账户信息成功")
        except:
            print("加载账户信息失败")

    def login(self, user, password):
        if((user in self.nameList) and user != "AI1" and user != "AI2" and user != "AI3"):
            re = "重复登录"
            print(re)
            return re, False
        if(user in self.Account.keys() and password == self.Account[user]['password']):
            re = "登录成功！{}".format(user)
            print(re)
            # self.nameList[len(self.nameList)] = user
            return re, True
        else:
            re = "登录失败"
            print(re)
            return re, False

    def register(self, user, password):
        if(user in self.Account):
            re = "用户名重复!!!"
            print(re)
            return re, False
        self.Account[user] = {'password':password, 'count':0, 'win':0}

        try:
            with open(self.file, 'wb') as f:
                pickle.dump(self.Account, f)
                print("账户信息存储成功")
                re = "账户注册成功"
                return re, False
        except:
            print("账户信息存储失败")
            re = "账户注册失败"

        print(re)
        return re, False
    
    def update(self,winID):
        if winID != 2:
            self.Account[self.nameList[winID]]['win'] += 1
            self.Account[self.nameList[winID]]['count'] += 1
            self.Account[self.nameList[(winID+1)%2]]['count'] += 1
        else:
            self.Account[self.nameList[0]]['win'] += 1
            self.Account[self.nameList[1]]['win'] += 1
            self.Account[self.nameList[0]]['count'] += 1
            self.Account[self.nameList[1]]['count'] += 1
        try:
            with open(self.file, 'wb') as f:
                pickle.dump(self.Account, f)
                print("对局信息存储成功")
                re = "对局信息存储成功"
                return re, False
        except:
            print("对局信息存储失败")
            re = "对局信息存储失败"
