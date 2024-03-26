from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece_rules import PieceRules
from chess_implementation.piece import Piece
from chess_implementation.chess_variables import *
from chess_implementation.find_moves import find_all_moves
from chess_implementation.make_moves import make_move, undo_last_move
from chess_implementation.move_stack import MoveStack
from model.main_model import Model
import copy
import time
import random

game = [6,0,5,2,-1,
        1,6,1,4,-4,
        5,2,6,4,-1,
        2,6,2,5,-1,
        6,1,5,2,-1,
        7,6,7,5,-1,
        7,0,6,0,-1,
        6,7,5,5,-1,
        1,1,1,2,-1,
        7,5,7,4,-1,
        5,1,5,2,-1,
        4,1,4,3,-4,
        3,0,4,1,-1,
        7,7,7,6,-1,
        6,2,6,3,-1,
        5,5,4,3,-1,
        0,1,0,3,-4,
        0,6,0,5,-1,
        3,1,3,2,-1,
        0,5,0,5,-1,
        4,1,4,2,-1,
        4,3,3,2,-1,
        4,2,5,1,-1]

def play_game(chess_board):
    for i in range(len(game)//5):
        ind = i*5
        if  game[ind] == 4 and game[ind+1] == 1 and game[ind+4] == -4:
            pass
        print(game[ind],game[ind+1],game[ind+2],game[ind+3],game[ind+4])
        make_move(chess_board,game[ind],game[ind+1],game[ind+2],game[ind+3],game[ind+4])
        if chess_board.black_pieces[chess_board.king_pos].position[0] != 3 or chess_board.black_pieces[chess_board.king_pos].position[1] != 7:
            #chess_board.show_board
            print(game[ind+4], "!!")
        
        