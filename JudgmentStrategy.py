from abc import ABC, abstractmethod
import numpy as np
from ChessBoard import *
from scipy.ndimage import label as CCL

class JudgmentStrategy(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def victory(self, chessBoard, x, y, flag) -> int:
        """
        输入为:棋盘,坐标x,y,是否落子的标识true表示落子
        判断局势的输赢
        """
        pass

    @abstractmethod
    def isOk(self, chessBoard, x, y, flag) -> bool:
        """判断是否能落子"""
        pass


class FIRJudgment(JudgmentStrategy):
    def __init__(self) -> None:
        super().__init__()

    def victory(self, chessBoard, x, y, flag) -> int:
        # 终局判定 2表示平局
        cur_id = (chessBoard.nstep+1)%2
        cur_piece = chessBoard.piece[cur_id+1]

        if(np.where(chessBoard.board == 0)[0].shape[0] == 0):
            return 2
        
        # 上下
        count = 1
        i = x+1
        while((i < chessBoard.h) and (chessBoard.board[i,y] == cur_piece)):
            count += 1
            i += 1
        i = x-1
        while((i > -1) and (chessBoard.board[i,y] == cur_piece)):
            count += 1
            i -= 1
        if(count >= 5):
            return cur_id

        # 左右
        count = 1
        i = y+1
        while((i < chessBoard.w) and (chessBoard.board[x,i] == cur_piece)):
            count += 1
            i += 1
        i = y-1
        while((i > -1) and (chessBoard.board[x,i] == cur_piece)):
            count += 1
            i -= 1
        if(count >= 5):
            return cur_id

        # 左上右下
        count = 1
        i = x+1
        j = y+1
        while((i < chessBoard.h and j < chessBoard.w) and (chessBoard.board[i,j] == cur_piece)):
            count += 1
            i += 1
            j += 1
        i = x-1
        j = y-1
        while((i >= 0 and j >= 0) and (chessBoard.board[i,j] == cur_piece)):
            count += 1
            i -= 1
            j -= 1
        if(count >= 5):
            return cur_id

        # 左下右上
        count = 1
        i = x-1
        j = y+1
        while((i >= 0 and j < chessBoard.w) and (chessBoard.board[i,j] == cur_piece)):
            count += 1
            i -= 1
            j += 1
        i = x+1
        j = y-1
        while((i < chessBoard.h and j >= 0) and (chessBoard.board[i,j] == cur_piece)):
            count += 1
            i += 1
            j -= 1
        if(count >= 5):
            return cur_id

        return -1

    def isOk(self, chessBoard, x, y, flag) -> bool:
        if(flag is False):
            print("不可虚着！！！")
            return False
        if(flag and (x >= 0) and (x < chessBoard.h) and (y >= 0) and (y < chessBoard.w) and chessBoard.board[x,y] == 0):
            return True
        print("误操作")
        return False


class WeiqiJudgment(JudgmentStrategy):
    def __init__(self) -> None:
        super().__init__()

    def victory(self, chessBoard, x, y, flag) -> int:
        return -1

    def isOk(self, chessBoard, x, y, flag) -> bool:
        self.MapL = chessBoard.w
        self.step = chessBoard.nstep
        if(flag is False):
            print("虚着")
            return True
        if(flag and (x >= 0) and (x < chessBoard.h) and (y >= 0) and (y < chessBoard.w) and chessBoard.board[x,y] == 0):
            # 提子
            return self.move(x,y,chessBoard)
        print("误操作")
        return False
    
    def CalcQi(self, component, board):
        '''计算一块棋的气'''
        qi = 0    
        zeros = np.where(board == 0)   
        for n in range(len(zeros[0])):
            i,j = zeros[0][n], zeros[1][n]
            if i < np.min(component[0])-1 or i > np.max(component[0])+1: continue
            if j < np.min(component[1])-1 or j > np.max(component[1])+1: continue
            exit_flag = 0
            for offset in [[0, -1], [1, 0], [-1, 0], [0, 1]]:
                i2, j2 = i + offset[0], j + offset[1]
                if 0 <= i2 < self.MapL and 0 <= j2 < self.MapL:
                    for m in range(len(component[0])):
                        if i2 == component[0][m] and component[1][m] == j2:
                            qi += 1
                            if (min(i,j)==0 or max(i,j)==self.MapL-1) and (min(i2,j2)==0 or max(i2,j2)==self.MapL-1):
                                qi += 0.15
                            exit_flag = True
                            break
                if exit_flag: break                
        return qi

    def tizi(self, board):
        '''提子，返回提子的数量'''
        #print("tizi")
        tizi_nums = [0,0]
        board_0 = board.copy()
        for n, player in enumerate([1+self.step%2, 2-self.step%2]):
            board_1 = board_0 == player
            components = CCL(board_1)[0]
            for i in range(int(np.max(components))):
                component = np.where(components==i+1)
                if self.CalcQi(component, board) == 0: 
                    tizi_nums[n] += np.shape(component)[1]
                    if n: board[component] = 0
        return tizi_nums

    def move(self, y, x, chessBoard):
        '''走一步棋'''
        y += 1
        x += 1
        i, j = y-1, x-1

        if not chessBoard.board[i][j]: 
            chessBoard.board[i][j] = self.step%2 + 1
            tizis = self.tizi(chessBoard.board)
            # 判断是否有气
            if not tizis[1] and tizis[0]:
                chessBoard.board[i][j] = 0
                print("无气。不能在此落子。")
                return False
            # 判断是否劫争
            elif chessBoard.ko[0] and abs(x-chessBoard.ko[1]) + abs(y-chessBoard.ko[2]) == 1:
                chessBoard.board[i][j] = 0
                chessBoard.board[chessBoard.ko[2]-1][chessBoard.ko[1]-1] = 2 - self.step%2
                print("劫争。不能在此落子。")
                return False
            if tizis[0] == 1 and tizis[1] == 1:
                chessBoard.ko = [1,x,y]
            else: chessBoard.ko = [0,-1,-1]
            chessBoard.board[i][j] = 0
            return True   
 
