#include<cstdio>
#include<iostream>
#include<vector>
#include<stack>
#include<string>
#include<fstream>
#include "ChessBoard.cpp"

using namespace std;

class ChessMemento
{
public:
    int player;
    int w, h;
    vector< vector<char>> board;

    ChessMemento(int w, int h, int player, vector< vector<char>> board){
        this->board = board;
        this->w = w;
        this->h = h;
        this->player = player;
    }


};

class ChessCaretaker
{
public:
    vector<ChessMemento> MementoList;
    string path = "./save/";

    void pushMemento(ChessMemento memento){
        MementoList.push_back(memento);
    }

    ChessMemento topMemento(){
        ChessMemento temp = MementoList[MementoList.size()-1];
        return temp;
    }

    void popMemento(){
        ChessMemento temp = MementoList[MementoList.size()-1];
        MementoList.pop_back();
    }

    int getSize(){
        return MementoList.size();
    }

    bool saveInText(int fileId = 0){
        string file = path+"save"+to_string(fileId)+".txt";
        cout << file << endl;
        ofstream outFile(file);
        if(outFile.is_open()) 
        {   
            for(int i = 0; i < MementoList.size(); i++){
                ChessMemento temp = MementoList[i];
                outFile << temp.player <<endl;
                outFile << temp.h << endl;
                outFile << temp.w << endl;

                for(int j = 0; j < temp.w; j++){
                    for(int k = 0; k < temp.h; k++){
                        outFile << temp.board[j][k] << " ";
                    }
                    outFile << endl;
                }
            }
            outFile.close();
        }else{
            cout << "Save Fail!" << endl;
            return false;
        }
        return true;
    }

    bool restoreFormText(int fileId = 0 ){
        MementoList.clear();
        string file = path+"save"+to_string(fileId)+".txt";
        fstream inFile(file);
        if(inFile.is_open()){
            int w,h,player;
            while(inFile >> player){
                inFile >> h >> w;
                vector< vector<char>> board(w, vector<char>(h));
                for(int i = 0; i < w; i++){
                    for(int j =0; j < h; j++){
                        inFile >> board[i][j];
                    }
                }
                this->pushMemento(ChessMemento(w, h, player, board));
            }
        }else{
            cout << "Read Fail!" << endl;
            return false;
        }
        return true;
    }
    
};

class ChessOriginator
{
public:
    AbstractChessBoard* board_ptr;
    ChessOriginator(AbstractChessBoard* board_ptr){
        this->board_ptr = board_ptr;
    }

    ChessMemento save(){
        return ChessMemento(this->board_ptr->w, this->board_ptr->h, this->board_ptr->player, this->board_ptr->board);
    }

    void restore(ChessMemento memento){
        this->board_ptr->player = memento.player;
        this->board_ptr->h = memento.h;
        this->board_ptr->w = memento.w;
        this->board_ptr->board = memento.board;
    }

};


// int main(){
//     vector<string> nameList = {"a", "b"};
//     AbstractChessBoard* board_ptr = new WeiqiBoard(8,8,nameList);
//     ChessOriginator originator = ChessOriginator(board_ptr);
//     ChessCaretaker caretaker = ChessCaretaker();
//     caretaker.pushMemento(originator.save());
//     board_ptr->step(1,2, true);
//     caretaker.pushMemento(originator.save());
//     board_ptr->step(3,2, true);
//     caretaker.pushMemento(originator.save());
//     caretaker.saveInText();
//     caretaker.restoreFormText();
//     caretaker.saveInText(1);
//     caretaker.popMemento();
//     originator.restore(caretaker.topMemento());
//     caretaker.saveInText(3);
// }