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

def play_game_test(chess_board: ChessBoard, depth, legnth):

    for i in range(legnth):
        chess_board_mut = copy.deepcopy(chess_board)

        play_game(chess_board_mut, depth)


def play_game(chess_board, depth):

    while legal_board(chess_board):
        moves = find_all_moves(chess_board)

        engine(chess_board,depth)
        
        move_ind = random.randint(0,moves.head)
        ind_pos = move_ind*5

        make_move(chess_board, moves.stack[ind_pos],moves.stack[ind_pos+1], moves.stack[ind_pos+2], moves.stack[ind_pos+3], moves.stack[ind_pos+4])
        

def engine(chess_board, depth):

    if depth > 0 and legal_board(chess_board):
        moves = find_all_moves(chess_board)

        for ind in range(moves.head):
            ind_pos = ind*5
            make_move(chess_board, moves.stack[ind_pos],moves.stack[ind_pos+1], moves.stack[ind_pos+2], moves.stack[ind_pos+3], moves.stack[ind_pos+4])
            
            engine(chess_board, depth-1)
                
            undo_last_move(chess_board)


def legal_board(chess_board: ChessBoard):
    save_color = chess_board.color_to_move
    chess_board.color_to_move = WHITE
    white_moves = find_all_moves(chess_board)
    chess_board.color_to_move = BLACK
    black_moves = find_all_moves(chess_board)

    white_king_pos = chess_board.white_pieces[chess_board.king_pos].position
    black_king_pos = chess_board.black_pieces[chess_board.king_pos].position

    chess_board.color_to_move = save_color

    if not (chess_board.white_pieces[chess_board.king_pos].is_alive and chess_board.black_pieces[chess_board.king_pos].is_alive):
        return False
    
    for ind in range(white_moves.head):
        ind_pos = ind*5
        if white_moves.stack[ind_pos+2] == black_king_pos[0] and white_moves.stack[ind_pos+3] == black_king_pos[1]:
            return False
    
    for ind in range(black_moves.head):
        ind_pos = ind*5
        if black_moves.stack[ind_pos+2] == white_king_pos[0] and black_moves.stack[ind_pos+3] == white_king_pos[1]:
            return False
    
    return True

    