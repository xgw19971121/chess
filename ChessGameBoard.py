from tkinter import *
import tkinter.messagebox
import numpy as np

class GameShow:
    def __init__(self, width = 1000, height = 1000, step = 50) -> None:

        self.w = 0
        self.h = 0

        self.width = width
        self.height = height
        self.step = step

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
        

    def drawBoard(self, w, h, wstart, hstart, step):
        "根据起始位置和步长绘制棋盘"
        wend = wstart+step*(w-1)
        hend = hstart+step*(h-1)
        for i in range(0, w):
            self.canvas.create_line(i * step + wstart, hstart, i * step + wstart, hend)
        for i in range(0, h):
            self.canvas.create_line(wstart, i * step + hstart, wend, i * step + hstart)
        
    
    def setFuncFrame(self):
        label1 = Label(self.funcFrame, text="棋盘大小")
        entry1 = Entry(self.funcFrame)
        startButton = Button(self.funcFrame, text="开始游戏", command=self.startGame)
        undoButton = Button(self.funcFrame, text="悔棋", command=self.unDo)
        giveupButton = Button(self.funcFrame, text="认输", command=self.giveUp)
        saveButton = Button(self.funcFrame, text="保存", command=self.saveGame)
        loadButton = Button(self.funcFrame, text="读取", command=self.loadGame)
        self.Funclist.append(label1)
        self.Funclist.append(entry1)
        self.Funclist.append(startButton)
        self.Funclist.append(undoButton)
        self.Funclist.append(giveupButton)
        self.Funclist.append(saveButton)
        self.Funclist.append(loadButton)
        label1.pack(side=LEFT)
        entry1.pack(side=LEFT)
        startButton.pack(side=LEFT)
        undoButton.pack(side=LEFT)
        giveupButton.pack(side=LEFT)
        saveButton.pack(side=LEFT)
        loadButton.pack(side=LEFT)

    def setTextFrame(self):
        curUserText = Text(self.textFrame, height=15)
        user1Text = Text(self.textFrame, height=15)
        user2Text = Text(self.textFrame, height=15)
        tipText = Text(self.textFrame, height=15)
        self.Textlist.append(curUserText)
        self.Textlist.append(user1Text)
        self.Textlist.append(user2Text)
        self.Textlist.append(tipText)
        curUserText.insert("insert","当前用户为:")
        curUserText.configure(state="disabled")
        user1Text.insert("insert","用户1")
        user1Text.configure(state="disabled")
        user2Text.insert("insert","用户2")
        user2Text.configure(state="disabled")
        tipText.insert("insert","提示")
        tipText.configure(state="disabled")
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
            self.w = int(self.Funclist[1].get())
            self.h = int(self.Funclist[1].get())
            self.canvas.delete(ALL)
            
            self.hstart = self.height/2 - (self.h-1)/2*self.step
            self.wstart = self.width/2 - (self.w-1)/2*self.step
            self.drawBoard(self.w, self.h, self.wstart, self.hstart, self.step)
            tkinter.messagebox.showinfo("","开始游戏，棋盘大小{}".format(w))
    
    def unDo(self):
        tkinter.messagebox.showinfo("","悔棋")
    
    def giveUp(self):
        tkinter.messagebox.showinfo("","认输")

    def saveGame(self):
        tkinter.messagebox.showinfo("","保存")

    def loadGame(self):
        tkinter.messagebox.showinfo("","读取")

    def processPoint(self, event):
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
        self.goStep(self.hstart+xi*self.step, self.wstart+yi*self.step, 0)

        # self.goStep(120, 350, 0)

    def goStep(self, x, y, id):
        if(id == 0):
            self.canvas.create_oval(x-15,y-15,x+15,y+15,fill="black")
        else:
            self.canvas.create_oval(x-15,y-15,x+15,y+15,fill="white")





if __name__ == '__main__':
    # gameshow = GameShow(10,10)
    GameShow()
