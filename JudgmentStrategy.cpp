#include<cstdio>
#include<iostream>
#include<vector>
#include "ChessBoard.cpp"

using namespace std;

class JudgmentStrategy
{
private:
public:
    virtual int victory(AbstractChessBoard* chessBoard, int x, int y, bool flag) = 0;
    virtual bool is_ok(AbstractChessBoard* chessBoard, int x, int y, bool flag) = 0;
};

class FIRJudgment:public JudgmentStrategy
{
    int victory(AbstractChessBoard* chessBoard, int x, int y, bool flag){
        //终局判定
        int cur_id = (chessBoard->player+1)%2;
        char cur_piece = chessBoard->piece[cur_id];
        int count;
        
        //上下
        count = 1;
        int i = x+1;
        while((i < chessBoard->w) && (chessBoard->board[i++][y] == cur_piece)){count++;}
        i = x-1;
        while((i > -1) && (chessBoard->board[i--][y] == cur_piece)){count++;}
        if(count >= 5) return cur_id;

        //左右
        count = 1;
        i = y+1;
        while((i < chessBoard->h) && (chessBoard->board[x][i++] == cur_piece)){count++;}
        i = y-1;
        while((i > -1) && (chessBoard->board[x][i--] == cur_piece)){count++;}
        if(count >= 5) return cur_id;

        //左上右下
        count = 1;
        i = x+1;
        int j = y+1;
        while((i < chessBoard->w && j < chessBoard->h) && (chessBoard->board[i++][j++] == cur_piece)){count++;}
        i = x-1;
        j = y-1;
        while((i >= 0 && j >= 0) && (chessBoard->board[i--][j--] == cur_piece)){count++;}
        if(count >= 5) return cur_id;

        //左下右上
        count = 1;
        i = x-1;
        j = y+1;
        while((i >= 0 && j < chessBoard->h) && (chessBoard->board[i--][j++] == cur_piece)){count++;}
        i = x+1;
        j = y-1;
        while((i < chessBoard->w && j >= 0) && (chessBoard->board[i++][j--] == cur_piece)){count++;}
        if(count >= 5) return cur_id;


        return -1;
    }

    bool is_ok(AbstractChessBoard* chessBoard, int x, int y, bool flag){
        if(!flag){
            cout << "不可虚着" << endl;
            return false;
        } 
        //判断落子是否可行
        if(flag && x >= 0 && x < chessBoard->w && y >= 0 && y < chessBoard->h && chessBoard->board[x][y] == chessBoard->piece[2]){
            return true;
        }
        cout << "误操作" << endl;
        return false;
    }
};


// int main(){
//     vector<string> nameList = {"a", "b"};
//     AbstractChessBoard* board_ptr = new WeiqiBoard(8,8,nameList);
//     JudgmentStrategy* judgment = new FIRJudgment();
//     board_ptr->show();
//     int x, y;
//     while(cin >> x >> y){
//         bool flag = true;
//         if(x == -1 && y == -1){
//             flag = false;
//         }
//         if(judgment->is_ok(board_ptr, x, y, flag)){
//             board_ptr->step(x,y,flag);
//             board_ptr->show();
//             int re = judgment->victory(board_ptr, x, y, flag);
//             board_ptr->step(x,y,false);
//             if(re != -1)
//                 cout << "胜利者为：" << re << endl;
//         }
//     }
// }
