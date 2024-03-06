from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece_rules import PieceRules
from chess_implementation.piece import Piece
from chess_implementation.move_stack import MoveStack
import numpy as np
from chess_implementation.chess_variables import *

def make_move(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    if move_type == NORMAL_MOVE or DOUBLE_PAWN:
        make_normal_move(chess_board, from_x, from_y, to_x, to_y, move_type)
    elif move_type == CASTLING:
        make_castling_move(chess_board,from_x, from_y, to_x, to_y, move_type)

def make_normal_move(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    color = chess_board.color_to_move
    piece_number = chess_board.board[from_x][from_y]
    pos_in_piece_list = abs(piece_number)-1
    
    move_count = chess_board.move_count
    
    if color == WHITE:
        piece: Piece= chess_board.white_pieces[pos_in_piece_list]
    else:
        piece: Piece = chess_board.black_pieces[pos_in_piece_list]

    chess_board.board[from_x][from_y] = 0
    on_field = chess_board.board[to_x][to_y]
    #if a piece gets captured
    if on_field != 0:
        chess_board.captured_pieces[move_count] = on_field
        pos_in_piece_list_captured = abs(on_field)-1
        
        if color == WHITE:
            captured_piece:Piece = chess_board.black_pieces[pos_in_piece_list_captured]
        else:
            captured_piece:Piece = chess_board.white_pieces[pos_in_piece_list_captured]
        captured_piece.is_alive = False
    piece.first_move = move_count

    #save the move
    chess_board.past_moves[move_count*5] = from_x
    chess_board.past_moves[move_count*5+1] = from_y
    chess_board.past_moves[move_count*5+2] = to_x
    chess_board.past_moves[move_count*5+3] = to_y
    chess_board.past_moves[move_count*5+4] = move_type

    #set piece on position update piece position
    chess_board.board[to_x][to_y] = piece_number
    piece.position[0] = to_x
    piece.position[1] = to_y

    #change color to move and move count
    chess_board.color_to_move *= -1
    chess_board.move_count += 1

def make_castling_move(chess_board,from_x, from_y, to_x, to_y, move_type):
    pass