from tkinter import *
import tkinter.messagebox
import numpy as np
from GameEnv import *
from JudgmentStrategy import *
from ChessBoard import *
from Memento import *

class GameShow:
    def __init__(self, width = 1000, height = 1000, step = 50) -> None:
        self.w = 0
        self.h = 0
        self.gameList = ["五子棋", "围棋", "黑白棋"]

        self.width = width
        self.height = height
        self.step = step

        """aaa"""
        self.nameList = ['A','B']
        self.gameEnv = GameFactory(self.h, self.w, 0, self.nameList)

        self.root = Tk()
        self.root.title("游戏")
        self.funcFrame = Frame(self.root)
        self.canFrame = Frame(self.root,width=width,height=height)
        self.textFrame = Frame(self.root,width=250,height=height)
        self.Funclist = []
        self.Textlist = []

        self.funcFrame.pack(anchor="w")
        self.canFrame.pack(side=LEFT)
        self.textFrame.pack(side=LEFT)

        self.setFuncFrame()
        self.setTextFrame()
        self.canvas = Canvas(self.canFrame, width = self.width, height = self.height, background='chocolate')
        self.hstart = -1
        self.wstart = -1
        self.canvas.pack()
        self.canvas.bind("<Button -1>", self.processPoint)
        self.root.mainloop()

        
        

    def drawBoard(self):
        """根据起始位置和步长绘制棋盘"""
        self.Textlist[0].configure(state="normal")
        self.Textlist[0].delete("1.0","end")
        self.Textlist[0].insert("insert","当前用户为:{}".format(self.nameList[self.gameEnv.chessboard.nstep%2]))
        self.Textlist[0].configure(state="disabled")
        self.numText.delete("1.0","end")
        self.numText.insert("insert","{}".format(self.gameEnv.chessboard.nstep))
        self.canvas.delete(ALL)
        wend = self.wstart+self.step*(self.w-1)
        hend = self.hstart+self.step*(self.h-1)
        for i in range(0, self.w):
            self.canvas.create_line(i * self.step + self.wstart, self.hstart, i * self.step + self.wstart, hend)
        for i in range(0, self.h):
            self.canvas.create_line(self.wstart, i * self.step + self.hstart, wend, i * self.step + self.hstart)

        for i in range(self.h):
            for j in range(self.w):
                if(self.gameEnv.chessboard.board[i,j] == 1):
                    self.goStep(i,j,0)
                elif(self.gameEnv.chessboard.board[i,j] == 2):
                    self.goStep(i,j,1)
        
    
    def setFuncFrame(self):
        var = StringVar()
        var.set(self.gameList)
        self.listbox = Listbox(self.funcFrame, listvariable=var, height=3)
        label1 = Label(self.funcFrame, text="棋盘大小")
        entry1 = Entry(self.funcFrame)
        startButton = Button(self.funcFrame, text="开始游戏", command=self.startGame)
        undoButton = Button(self.funcFrame, text="悔棋", command=self.unDo)
        giveupButton = Button(self.funcFrame, text="认输", command=self.giveUp)
        saveButton = Button(self.funcFrame, text="保存", command=self.saveGame)
        loadButton = Button(self.funcFrame, text="读取", command=self.loadGame)
        self.skipButton = Button(self.funcFrame, text="虚着", command=self.skip)
        self.Funclist.append(label1)
        self.Funclist.append(entry1)
        self.Funclist.append(startButton)
        self.Funclist.append(undoButton)
        self.Funclist.append(giveupButton)
        self.Funclist.append(saveButton)
        self.Funclist.append(loadButton)
        self.listbox.pack(side=LEFT)
        label1.pack(side=LEFT)
        entry1.pack(side=LEFT)
        startButton.pack(side=LEFT)
        undoButton.pack(side=LEFT)
        giveupButton.pack(side=LEFT)
        saveButton.pack(side=LEFT)
        loadButton.pack(side=LEFT)
        self.skipButton.pack(side=LEFT)
        self.skipButton.config(state=DISABLED)

    def setTextFrame(self):
        curUserText = Text(self.textFrame, height=15)
        user1Text = Text(self.textFrame, height=15)
        user2Text = Text(self.textFrame, height=15)
        tipText = Text(self.textFrame, height=14)
        self.numText = Text(self.textFrame, height=1)
        self.Textlist.append(curUserText)
        self.Textlist.append(user1Text)
        self.Textlist.append(user2Text)
        self.Textlist.append(tipText)
        curUserText.insert("insert","当前用户为:")
        curUserText.configure(state="disabled")
        user1Text.insert("insert","用户1:{}".format(self.nameList[0]))
        user1Text.configure(state="disabled")
        user2Text.insert("insert","用户2:{}".format(self.nameList[1]))
        user2Text.configure(state="disabled")
        tipText.insert("insert","提示")
        tipText.configure(state="disabled")
        self.numText.pack()
        curUserText.pack()
        user1Text.pack()
        user2Text.pack()
        tipText.pack()

    def startGame(self):

        w = self.Funclist[1].get()
        if(w == ''):
            tkinter.messagebox.showinfo("错误", "请输入棋盘大小")
        elif(int(w)<8 or int(w)>19):
            tkinter.messagebox.showinfo("错误", "棋盘大小不可超过19或低于8")
        else:
            if(self.listbox.curselection() == ()):
                tkinter.messagebox.showinfo("错误", "选择游戏模式")
                return
            self.w = int(self.Funclist[1].get())
            self.h = int(self.Funclist[1].get())
            
            if( self.listbox.curselection()[0] != 1):
                self.skipButton.config(state=DISABLED)
            else:
                self.skipButton.config(state=NORMAL)
            self.gameEnv = GameFactory(self.h, self.w, self.listbox.curselection()[0], self.nameList)
            self.hstart = self.height/2 - (self.h-1)/2*self.step
            self.wstart = self.width/2 - (self.w-1)/2*self.step
            self.drawBoard()
            tkinter.messagebox.showinfo("","开始游戏，棋盘大小{}".format(w))
    
    def unDo(self):
        if(self.gameEnv.gameover):
            return
        if(self.gameEnv.undo() == False):
            tkinter.messagebox.showinfo("","当前不可悔棋")
            return
        self.drawBoard()
        tkinter.messagebox.showinfo("","悔棋")
    
    def giveUp(self):
        if(self.gameEnv.gameover):
            return
        tkinter.messagebox.showinfo("","玩家{}认输".format(self.nameList[self.gameEnv.chessboard.nstep%2]))
        self.gameEnv.giveup()

    def saveGame(self):
        if(self.gameEnv.gameover):
            return
        self.gameEnv.save()
        tkinter.messagebox.showinfo("","保存")

    def loadGame(self):
        if(self.gameEnv.restore() == False):
            tkinter.messagebox.showinfo("","读取失败")
            return
        self.drawBoard()
        tkinter.messagebox.showinfo("","读取")

    def skip(self):
        self.gameEnv.step(0,0,False)
        self.drawBoard()

    def processPoint(self, event):
        if(self.gameEnv.gameover):
            return
        x = int(event.x)
        y = int(event.y)
        if(x < self.hstart-10 or y < self.wstart-10 or x > self.hstart+(self.w-1)*self.step+10 or y >self.wstart+(self.w-1)*self.step+10):
            return
        xi = (x - self.hstart)//self.step
        rx = (x - self.hstart)%self.step
        yi = (y - self.wstart)//self.step
        ry = (y - self.wstart)%self.step
        if((rx>10 and rx<self.step-10)or(ry>10 and ry<self.step-10)):
            return
        if(rx>=self.step-10):
            xi += 1
        if(ry>=self.step-10):
            yi += 1
        flag, winId = self.gameEnv.step(int(xi), int(yi))
        if(flag == False):
            tkinter.messagebox.showinfo("","落子错误")
            return
        # self.goStep(self.hstart+xi*self.step, self.wstart+yi*self.step, self.gameEnv.chessboard.player)
        self.drawBoard()
        if(winId != -1 and winId != 2):
            tkinter.messagebox.showinfo("游戏结束","获胜者：{}".format(self.nameList[int(winId)]))
        elif(winId == 2):
            tkinter.messagebox.showinfo("游戏结束","平局")


        # self.goStep(120, 350, 0)

    def goStep(self, x, y, id):
        if(id == 0):
            self.canvas.create_oval(self.hstart+x*self.step-15,self.wstart+y*self.step-15,self.hstart+x*self.step+15,self.wstart+y*self.step+15,fill="black")
        else:
            self.canvas.create_oval(self.hstart+x*self.step-15,self.wstart+y*self.step-15,self.hstart+x*self.step+15,self.wstart+y*self.step+15,fill="white")
        





if __name__ == '__main__':
    # gameshow = GameShow(10,10)
    GameShow()
