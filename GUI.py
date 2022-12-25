from tkinter import *
import tkinter.messagebox
import numpy as np
from GameEnv import *
from JudgmentStrategy import *
from ChessBoard import *
from Memento import *
from Player import *
import time

WIDTH = 1000
HEIGHT = 1000
STEP = 50
class GameShow:
    def __init__(self) -> None:
        self.w = 0
        self.h = 0
        self.gameList = ["五子棋", "围棋", "黑白棋"]

        self.width = WIDTH
        self.height = HEIGHT
        self.step = STEP

        self.numAI = 0

        self.showtipflag = True
        self.stopClick = False
        self.playing = False

        self.AIplayer = [False, False]
        self.AI = [None, None]

        """aaa"""
        self.nameList = []
        # self.nameList = []
        # self.gameEnv = GameFactory(self.h, self.w, 0, self.nameList)

        self.gameEnv = GameProxy(self.h, self.w, 0, self.nameList)

        self.root = Tk()
        self.root.title("游戏")
        # self.root.geometry('1500x1100')
        # self.root.resizable(width=False, height=False)
        self.initLoginGUI()
        self.root.mainloop()

    
    def initLoginGUI(self):
        self.LoginRoot = Frame(self.root, width=620, height=500)
        self.LoginRoot.pack(side=LEFT)
        self.LoginDict = {}
        labelUser = Label(self.LoginRoot, text='User Name:',fg='yellow',bg='purple',font=("微软雅黑",16), justify=tkinter.RIGHT, anchor='e', width=80)
        labelUser.place(x=150, y=50, width=125, height=25)

        # 创建字符串变量和文本框组件，同时设置关联的变量
        varName = StringVar(self.LoginRoot, value='')
        entryName = Entry(self.LoginRoot, width=80, textvariable=varName)
        entryName.place(x=290, y=50, width=180, height=25)

        # 在窗口上创建标签组件（User Pwd）
        labelPwd = Label(self.LoginRoot, text='User Pwd:',fg='yellow',bg='purple',font=("微软雅黑",16), justify=tkinter.RIGHT, anchor='e', width=80)
        # 显示该组件的位置及大小
        labelPwd.place(x=150, y=90, width=125, height=25)

        # 创建密码文本框,同时设置关联的变量
        varPwd = StringVar(self.LoginRoot, value='')
        entryPwd = Entry(self.LoginRoot, show='*', width=80, textvariable=varPwd)
        entryPwd.place(x=290, y=90, width=180, height=25)

        # 登录按钮
        loginButton = Button(self.LoginRoot, text='登录', activeforeground='#ff0000', command=self.login)
        loginButton.place(x=160, y=175, width=80, height=25)

        # 注册按钮
        registerButton = Button(self.LoginRoot, text='注册', command=self.register)
        registerButton.place(x=360, y=175, width=80, height=25)

        LoginText = Text(self.LoginRoot, height=14,font=("微软雅黑",16))
        LoginText.place(x=150, y=230, width=320, height=200)
        LoginText.insert("insert","游客登录:\n请输入账户'游客1'或'游客2'，密码为空\n\nAI模式:\n请输入账户'AI1','AI2','AI3'密码为空，分别对应不同智能的AI")
        LoginText.configure(state="disabled")

        self.LoginDict['labelUser'] = labelUser
        self.LoginDict['varName'] = varName
        self.LoginDict['entryName'] = entryName
        self.LoginDict['labelPwd'] = labelPwd
        self.LoginDict['varPwd'] = varPwd
        self.LoginDict['entryPwd'] = entryPwd
        self.LoginDict['loginButton'] = loginButton
        self.LoginDict['registerButton'] = registerButton
        

    def login(self):
        user = self.LoginDict['entryName'].get()
        pwd = self.LoginDict['entryPwd'].get()
        if(user == ""):
            tkinter.messagebox.showinfo("错误", "请输入用户名")
            return
        re, flag = self.gameEnv.login(user,pwd)
        if(flag):
            tkinter.messagebox.showinfo("", re)
            self.nameList.append(user)
            if(user == "AI1" or user == "AI2" or user == "AI3"):
                self.numAI += 1
                self.AIplayer[len(self.nameList)-1] = True
        else:
            tkinter.messagebox.showinfo("错误", re)
            return


        if(len(self.nameList) == 2):
            self.gameEnv.start(self.h, self.w, 0)
            self.initGameGUI()
            self.GameRoot.pack()
            self.LoginRoot.pack_forget()

    def register(self):
        user = self.LoginDict['entryName'].get()
        pwd = self.LoginDict['entryPwd'].get()
        if(user == ""):
            tkinter.messagebox.showinfo("错误", "请输入用户名")
            return
        if(pwd == ""):
            tkinter.messagebox.showinfo("错误", "请输入密码")
            return
        re, flag = self.gameEnv.register(user,pwd)
        if(flag):
            tkinter.messagebox.showinfo("", re)
            self.nameList.append(user)
        else:
            tkinter.messagebox.showinfo("错误", re)
            return


    def initGameGUI(self):
        self.GameRoot = Frame(self.root)
        self.GameRoot.pack(side=LEFT)
        self.funcFrame = Frame(self.GameRoot)
        self.canFrame = Frame(self.GameRoot,width=WIDTH,height=HEIGHT)
        self.textFrame = Frame(self.GameRoot,width=250,height=HEIGHT)
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


        
        

    def drawBoard(self):
        """根据起始位置和步长绘制棋盘"""
        self.updateText()

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
        self.showtip = Button(self.funcFrame, text="显示\隐藏提示", command=self.showTip)
        self.playButton = Button(self.funcFrame, text="播放\结束", command=self.playGame)
        self.nextButton = Button(self.funcFrame, text="下一步", command=self.nextStep)
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
        self.showtip.pack(side=LEFT)
        self.playButton.pack(side=LEFT)
        self.nextButton.pack(side=LEFT)

    def setTextFrame(self):
        curUserText = Text(self.textFrame, height=15)
        user1Text = Text(self.textFrame, height=15)
        user2Text = Text(self.textFrame, height=15)
        self.tipText = Text(self.textFrame, height=14)
        self.numText = Text(self.textFrame, height=1)
        self.Textlist.append(curUserText)
        self.Textlist.append(user1Text)
        self.Textlist.append(user2Text)
        self.Textlist.append(self.tipText)
        curUserText.insert("insert","当前用户为:")
        curUserText.configure(state="disabled")
        try:
            user1Text.insert("insert","用户1:{}\n".format(self.nameList[0]))
            user1Text.insert("insert","局数:{}\n".format(self.gameEnv.Account[self.nameList[0]]['count']))
            user1Text.insert("insert","胜场:{}\n".format(self.gameEnv.Account[self.nameList[0]]['win']))
        except:
            pass
        user1Text.configure(state="disabled")
        try:
            user2Text.insert("insert","用户2:{}\n".format(self.nameList[1]))
            user2Text.insert("insert","局数:{}\n".format(self.gameEnv.Account[self.nameList[1]]['count']))
            user2Text.insert("insert","胜场:{}\n".format(self.gameEnv.Account[self.nameList[1]]['win']))
        except:
            pass
        user2Text.configure(state="disabled")
        self.tipText.insert("insert","提示:选择游戏方式，输入棋盘大小后，点击开始游戏即可")
        self.tipText.configure(state="disabled")
        self.numText.pack()
        curUserText.pack()
        user1Text.pack()
        user2Text.pack()
        self.tipText.pack()

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
            
            if( self.listbox.curselection()[0] == 0):
                self.skipButton.config(state=DISABLED)
            else:
                self.skipButton.config(state=NORMAL)
            if(self.listbox.curselection()[0] == 2):
                self.w = 8
                self.h = 8

            self.gameEnv.start(self.h, self.w, self.listbox.curselection()[0])
            """测试AI"""
            if(self.numAI != 0):
                for i in range(2):
                    if(self.listbox.curselection()[0] == 0):
                        if(self.AIplayer[i]):
                            if(self.nameList[i] == 'AI1'):
                                self.AI[i] = FIRAI_A(i)
                            elif(self.nameList[i] == 'AI2'):
                                self.AI[i] = FIRAI_B(i)
                            else:
                                self.AI[i] = FIRAI_B(i)
                    elif(self.listbox.curselection()[0] == 1):
                        if(self.AIplayer[i]):
                            self.AI[i] = WeiQiAI_A(i)
                    else:
                        if(self.AIplayer[i]):
                            self.AI[i] = ReversiAI_A(i)
            """hh"""
            self.hstart = self.height/2 - (self.h-1)/2*self.step
            self.wstart = self.width/2 - (self.w-1)/2*self.step
            self.drawBoard()
            tkinter.messagebox.showinfo("","开始游戏，棋盘大小{}".format(w))
        self.stopClick = False
        self.playing = False
    
    def unDo(self):
        if(self.gameEnv.gameover or self.stopClick):
            return
        if(self.gameEnv.undo() == False):
            tkinter.messagebox.showinfo("","当前不可悔棋")
            return
        self.drawBoard()
        tkinter.messagebox.showinfo("","悔棋")
    
    def giveUp(self):
        if(self.gameEnv.gameover or self.stopClick):
            return
        tkinter.messagebox.showinfo("","玩家{}认输".format(self.nameList[self.gameEnv.chessboard.nstep%2]))
        self.gameEnv.giveup()
        self.gameEnv.update((self.gameEnv.chessboard.nstep+1)%2)
        self.updateText()

    def saveGame(self):
        if(self.gameEnv.gameover or self.stopClick):
            return
        self.gameEnv.save()
        tkinter.messagebox.showinfo("","保存")

    def loadGame(self):
        if(self.gameEnv.restore() == False):
            tkinter.messagebox.showinfo("","读取失败")
            return
        self.w = self.gameEnv.w
        self.h = self.gameEnv.h
        self.hstart = self.height/2 - (self.h-1)/2*self.step
        self.wstart = self.width/2 - (self.w-1)/2*self.step
        self.drawBoard()
        tkinter.messagebox.showinfo("","读取")

    def skip(self):
        flag, _ = self.gameEnv.step(0,0,False)
        if(flag is False):
            tkinter.messagebox.showinfo("错误","不可虚着")
        self.drawBoard()

    def processPoint(self, event):
        if(self.gameEnv.gameover or self.stopClick):
            return
        if(self.AIplayer[self.gameEnv.chessboard.nstep%2]):
            xi, yi = self.AI[self.gameEnv.chessboard.nstep%2].getStep(self.gameEnv.chessboard)
        else:
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

        print("{},{}".format(xi, yi))
        if(xi == -1 and yi == -1):
            flag, winId = self.gameEnv.step(int(xi), int(yi),FALSE)
        else:
            flag, winId = self.gameEnv.step(int(xi), int(yi))
        if(flag == False):
            tkinter.messagebox.showinfo("","落子错误")
            return
        # self.goStep(self.hstart+xi*self.step, self.wstart+yi*self.step, self.gameEnv.chessboard.player)
        
        if(winId != -1 and winId != 2):
            self.gameEnv.update(winId)
        elif(winId == 2):
            self.gameEnv.update(winId)

        self.drawBoard()
        if(winId != -1 and winId != 2):
            tkinter.messagebox.showinfo("游戏结束","获胜者：{}".format(self.nameList[int(winId)]))
        elif(winId == 2):
            tkinter.messagebox.showinfo("游戏结束","平局")

        # # time.sleep(10)
        # if(winId != -1):
        #     x,y = self.AIplayer.getStep(self.gameEnv.chessboard)
        #     flag, winId = self.gameEnv.step(x, y)
        #     if(flag == False):
        #         tkinter.messagebox.showinfo("","落子错误")
        #         return
        #     # self.goStep(self.hstart+xi*self.step, self.wstart+yi*self.step, self.gameEnv.chessboard.player)
        #     self.drawBoard()
        #     if(winId != -1 and winId != 2):
        #         tkinter.messagebox.showinfo("游戏结束","获胜者：{}".format(self.nameList[int(winId)]))
        #     elif(winId == 2):
        #         tkinter.messagebox.showinfo("游戏结束","平局")



        # self.goStep(120, 350, 0)

    def goStep(self, x, y, id):
        if(id == 0):
            self.canvas.create_oval(self.hstart+x*self.step-15,self.wstart+y*self.step-15,self.hstart+x*self.step+15,self.wstart+y*self.step+15,fill="black")
        else:
            self.canvas.create_oval(self.hstart+x*self.step-15,self.wstart+y*self.step-15,self.hstart+x*self.step+15,self.wstart+y*self.step+15,fill="white")
        
    def showTip(self):
        if(self.showtipflag):
            self.tipText.pack_forget()
            self.showtipflag = False
        else:
            self.tipText.pack()
            print("显示控件")
            self.showtipflag = True

    def updateText(self):
        self.Textlist[0].configure(state="normal")
        self.Textlist[0].delete("1.0","end")
        self.Textlist[0].insert("insert","当前用户为:{}".format(self.nameList[self.gameEnv.chessboard.nstep%2]))
        self.Textlist[0].configure(state="disabled")
        self.numText.delete("1.0","end")
        self.numText.insert("insert","{}".format(self.gameEnv.chessboard.nstep))

        self.Textlist[1].configure(state="normal")
        self.Textlist[1].delete("1.0","end")
        try:
            self.Textlist[1].insert("insert","用户1:{}\n".format(self.nameList[0]))
            self.Textlist[1].insert("insert","局数:{}\n".format(self.gameEnv.Account[self.nameList[0]]['count']))
            self.Textlist[1].insert("insert","胜场:{}\n".format(self.gameEnv.Account[self.nameList[0]]['win']))
        except:
            pass
        self.Textlist[1].configure(state="disabled")
        self.Textlist[2].configure(state="normal")
        self.Textlist[2].delete("1.0","end")
        try:
            self.Textlist[2].insert("insert","用户2:{}\n".format(self.nameList[1]))
            self.Textlist[2].insert("insert","局数:{}\n".format(self.gameEnv.Account[self.nameList[1]]['count']))
            self.Textlist[2].insert("insert","胜场:{}\n".format(self.gameEnv.Account[self.nameList[1]]['win']))
        except:
            pass
        self.Textlist[2].configure(state="disabled")

    
    def playGame(self):
        if(self.playing is False):
            if(self.gameEnv.restore(True) == False):
                tkinter.messagebox.showinfo("","没有可读取的录像文件")
                return
            self.w = self.gameEnv.w
            self.h = self.gameEnv.h
            self.hstart = self.height/2 - (self.h-1)/2*self.step
            self.wstart = self.width/2 - (self.w-1)/2*self.step
            self.drawBoard()
            tkinter.messagebox.showinfo("","开始播放录像")
            self.stopClick = True
            self.playing = True
            self.round = 1
        else:
            self.playing = False
            self.stopClick = False
            tkinter.messagebox.showinfo("","播放已结束")

    def nextStep(self):
        if(self.playing):
            flag = self.gameEnv.restoreIndex(self.round)
            self.round += 1
            self.drawBoard()
            if(flag is False):
                tkinter.messagebox.showinfo("","播放已结束")
                self.playing = False
                self.stopClick = False
            return
            
            


        




if __name__ == '__main__':
    # gameshow = GameShow(10,10)
    GameShow()
