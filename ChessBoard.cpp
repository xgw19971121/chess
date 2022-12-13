#include<cstdio>
#include<iostream>
#include<vector>

using namespace std;

// char piece[2] = {'X', 'O'};

class AbstractChessBoard
{
private:
public:
    int player;
    char piece[3] = {'X', 'O', '-'};
    int w, h;
    vector< vector<char>> board;
    vector<string> nameList;

    virtual void show() = 0;
    virtual bool step(int x, int y, bool flag) = 0;

};

class WeiqiBoard:public AbstractChessBoard
{
private:
    /* data */
public:
    WeiqiBoard(int w, int h, vector<string> nameList){
        this->nameList = nameList;
        this->player = 0;
        this->w = w;
        this->h = h;
        this->board = vector< vector<char>>(this->w, vector<char>(this->h));

        for(int i = 0; i < this->w; i++){
            for(int j = 0; j < this->h; j++){
                this->board[i][j] = this->piece[2];
            }
        }
    }

    void show(){
        cout << "当前玩家：" << this->nameList[this->player] << endl;
        for(int i = 0; i < this->w; i++){
            for(int j = 0; j < this->h; j++){
                cout << this->board[i][j] << " ";
            }
            cout << endl;
        }
    }

    bool step(int x, int y, bool flag){
        if(!flag) this->player = (this->player+1)%2;
        if(flag && x >= 0 && x < this->w && y >= 0 && y < this->h){
            this->board[x][y] = this->piece[this->player];
            this->player = (this->player+1)%2;
            return true;
        }
        return false;

    }
};


// int main(){

//     //棋盘类走子打印测试
//     vector<string> nameList = {"a", "b"};
//     AbstractChessBoard* board_ptr = new WeiqiBoard(3,3,nameList);
//     board_ptr->show();
//     board_ptr->step(1,0,true);
//     board_ptr->show();
// }
