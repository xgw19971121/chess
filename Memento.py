from ChessBoard import *
from abc import ABC, abstractmethod
import pickle
import numpy as np
import copy
import os


class ChessMemento:
    def __init__(self, chessBoard) -> None:
        self.chessBoard = copy.deepcopy(chessBoard)
        # self.w = w
        # self.h = h
        # self.player = player


class ChessCaretaker:
    def __init__(self) -> None:
        self.path = "./save/"
        self.MementoList = []

    def pushMemento(self, memento):
        self.MementoList.append(memento)
    
    def topMemento(self):
        temp = self.MementoList[-1]
        return temp

    def getMemento(self, round):
        temp = self.MementoList[round]
        return temp

    def popMemento(self):
        self.MementoList.pop()

    def getSize(self):
        return len(self.MementoList)
    
    def saveInPkl(self, user, fileId = 0) -> bool:
        path = self.path+user+"/"
        if(os.path.exists(path) is False):
            os.makedirs(path)
        file = path+"save{}.pkl".format(fileId)
        try:
            with open(file, 'wb') as f:
                pickle.dump(self.MementoList, f)
                print("存储文件{}成功".format(fileId))
                return True
        except:
            print("存储文件{}失败".format(fileId))
            return False

    def restoreFromPkl(self, user, fileId = 0) -> bool:
        self.MementoList.clear()
        path = self.path+user+"/"
        if(os.path.exists(path) is False):
            os.makedirs(path)
        file = path+"save{}.pkl".format(fileId)
        try:
            with open(file, 'rb') as f:
                self.MementoList = pickle.load(f)
                print("加载文件{}成功".format(fileId))
            return True
        except:
            print("加载文件{}失败".format(fileId))
            return False

class ChessOriginator:
    def __init__(self, chessBoard) -> None:
        self.chessBoard = chessBoard

    def save(self):
        return ChessMemento(self.chessBoard)

    def restore(self, memento):
        self.chessBoard = memento.chessBoard
