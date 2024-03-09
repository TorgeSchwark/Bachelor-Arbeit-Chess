from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece_rules import PieceRules
from chess_implementation.piece import Piece
from chess_implementation.move_stack import MoveStack
import numpy as np
from chess_implementation.chess_variables import *

def make_move(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Executes moves"""
    if move_type == NORMAL_MOVE or move_type == DOUBLE_PAWN:
        make_normal_move(chess_board, from_x, from_y, to_x, to_y, move_type)
    elif move_type == CASTLING:
        make_castling_move(chess_board,from_x, from_y, to_x, to_y, move_type)
    elif move_type == EN_PASSANT:
        make_en_passant(chess_board, from_x, from_y, to_x, to_y, move_type)
    elif move_type >= 0: #Promotion
        make_promotion(chess_board, from_x, from_y, to_x, to_y, move_type)

def make_normal_move(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Executes normal (also capturing) moves"""
    piece_number = chess_board.board[from_x][from_y]
    pos_in_piece_list = abs(piece_number)-1
    
    if chess_board.color_to_move == WHITE:
        piece: Piece= chess_board.white_pieces[pos_in_piece_list]
    else:
        piece: Piece = chess_board.black_pieces[pos_in_piece_list]

    if piece.rules.pawn:
        chess_board.fifty_move_rule[chess_board.move_count] = 0
    else: 
        if chess_board.move_count >= 1:
            chess_board.fifty_move_rule[chess_board.move_count] = chess_board.fifty_move_rule[chess_board.move_count-1]+1
        else:
            chess_board.fifty_move_rule[chess_board.move_count] = 1 

    chess_board.board[from_x][from_y] = 0
    on_field = chess_board.board[to_x][to_y]
    #if a piece gets captured
    if on_field != 0:
        chess_board.fifty_move_rule[chess_board.move_count] = 0
        chess_board.captured_pieces[chess_board.move_count] = on_field
        pos_in_piece_list_captured = abs(on_field)-1
        
        if chess_board.color_to_move == WHITE:
            captured_piece:Piece = chess_board.black_pieces[pos_in_piece_list_captured]
        else:
            captured_piece:Piece = chess_board.white_pieces[pos_in_piece_list_captured]
        captured_piece.is_alive = False
    if piece.first_move == -1:
        piece.first_move = chess_board.move_count

    #save the move
    save_in_last_moves(chess_board, from_x, from_y, to_x, to_y, move_type)

    #set piece on position update piece position
    chess_board.board[to_x][to_y] = piece_number
    piece.position[0] = to_x
    piece.position[1] = to_y

    #change color to move and move count
    chess_board.color_to_move *= -1
    chess_board.move_count += 1


def make_en_passant(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Executes en Passant moves"""
    piece_number = chess_board.board[from_x][from_y]
    pos_in_piece_list = abs(piece_number)-1

    if chess_board.color_to_move == WHITE:
        piece: Piece = chess_board.white_pieces[pos_in_piece_list]
    else:
        piece: Piece = chess_board.black_pieces[pos_in_piece_list]
    
    chess_board.board[from_x][from_y] = 0

    on_field = chess_board.board[to_x][from_y]
    pos_in_piece_list_captured = abs(on_field)-1
    chess_board.captured_pieces[chess_board.move_count] = on_field
    

    if chess_board.color_to_move == WHITE:
        captured_piece:Piece = chess_board.black_pieces[pos_in_piece_list_captured]
    else:
        captured_piece:Piece = chess_board.white_pieces[pos_in_piece_list_captured]
    captured_piece.is_alive = False
    chess_board.board[to_x][from_y] = 0

    #save the move
    save_in_last_moves(chess_board, from_x, from_y, to_x, to_y, move_type)

    #set piece on position update piece position
    chess_board.board[to_x][to_y] = piece_number
    piece.position[0] = to_x
    piece.position[1] = to_y

    chess_board.fifty_move_rule[chess_board.move_count] = 0

    #change color to move and move count
    chess_board.color_to_move *= -1
    chess_board.move_count += 1


def make_castling_move(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Executes castling moves"""
    king_moving_direction = (from_x-to_x)//abs(from_x-to_x)
    
    if chess_board.color_to_move == WHITE:
        king_number = chess_board.board[chess_board.white_king_pos[0]][chess_board.white_king_pos[1]]
        king_in_piece_list = abs(king_number)-1
        king: Piece = chess_board.white_pieces[king_in_piece_list]
    else:
        king_number = chess_board.board[chess_board.black_king_pos[0]][chess_board.black_king_pos[1]]
        king_in_piece_list = abs(king_number)
        king: Piece = chess_board.black_king_pos[king_in_piece_list]

    chess_board.board[king.position[0]][king.position[1]] = 0
    king.position[0] = king.position[0]+ 2*king_moving_direction
    chess_board.board[king.position[0]][king.position[1]] = king_number

    king.first_move = chess_board.move_count

    if chess_board.color_to_move == WHITE:
        chess_board.white_king_pos[0] = king.position[0]
        chess_board.white_king_pos[2] = chess_board.move_count
    else:
        chess_board.black_king_pos[0] = king.position[0]
        chess_board.black_king_pos[2] = chess_board.move_count
    
    make_normal_move(chess_board, from_x, from_y, to_x, to_y, move_type)


def make_promotion(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """ Executes a Promotion move """
    piece_number = chess_board.board[from_x][from_y]
    pos_in_piece_list = abs(piece_number)-1
    
    if chess_board.color_to_move == WHITE:
        piece: Piece= chess_board.white_pieces[pos_in_piece_list]
        piece_alike: Piece = chess_board.white_pieces[chess_board.all_non_pawn_pieces[move_type]]
    else:
        piece: Piece = chess_board.black_pieces[pos_in_piece_list]
        piece_alike: Piece = chess_board.black_pieces[chess_board.all_non_pawn_pieces[move_type]]

    piece.rules = piece_alike.rules
    
    make_normal_move(chess_board, from_x, from_y, to_x, to_y, move_type)
    

def undo_last_move(chess_board: ChessBoard):
    """Undoes the last move"""
    move_count = chess_board.move_count
    last_move_from_x = chess_board.past_moves[(move_count-1)*5]
    last_move_from_y = chess_board.past_moves[(move_count-1)*5+1]
    last_move_to_x   = chess_board.past_moves[(move_count-1)*5+2]
    last_move_to_y   = chess_board.past_moves[(move_count-1)*5+3]
    last_move_type   = chess_board.past_moves[(move_count-1)*5+4]
    if last_move_type == NORMAL_MOVE or last_move_type == DOUBLE_PAWN:
        undo_normal_move(chess_board, last_move_from_x, last_move_from_y, last_move_to_x, last_move_to_y, last_move_type)
    elif last_move_type == EN_PASSANT:
        undo_en_passant(chess_board, last_move_from_x, last_move_from_y, last_move_to_x, last_move_to_y, last_move_type)
    elif last_move_type == CASTLING:
        undo_castling_move(chess_board, last_move_from_x, last_move_from_y, last_move_to_x, last_move_to_y, last_move_type)
    elif last_move_type >= 0:
        undo_promotion(chess_board, last_move_from_x, last_move_from_y, last_move_to_x, last_move_to_y, last_move_type)

def undo_normal_move(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Undoes the last normal move"""

    piece_number = chess_board.board[to_x][to_y]
    pos_in_piece_list = abs(piece_number)-1
    move_count = chess_board.move_count

    if chess_board.color_to_move == WHITE:
        piece: Piece= chess_board.black_pieces[pos_in_piece_list]
    else:
        piece: Piece = chess_board.white_pieces[pos_in_piece_list]

    captured_piece_number = chess_board.captured_pieces[move_count-1]
    captured_piece_pos_in_piece_list = abs(captured_piece_number)-1
    chess_board.board[to_x][to_y] = captured_piece_number
    if captured_piece_number != 0:
        if chess_board.color_to_move == WHITE:
            chess_board.white_pieces[captured_piece_pos_in_piece_list].is_alive = True
        else:
            chess_board.black_pieces[captured_piece_pos_in_piece_list].is_alive = True

    chess_board.board[from_x][from_y] = piece_number

    piece.position[0] = from_x
    piece.position[1] = from_y

    if piece.first_move == move_count-1:
        piece.first_move = -1
    
    chess_board.color_to_move *= -1
    chess_board.move_count -= 1
    
def undo_en_passant(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Undoes the last move it was an en passant"""

    #puts the captured pawn on the to_x to_y field where it shouldnt be    
    undo_normal_move(chess_board, from_x, from_y, to_x, to_y, move_type)

    #this is slower but since en passant is a rare case Ok ...
    captured_piece_number = chess_board.board[to_x][to_y]
    print(captured_piece_number)
    pos_in_piece_list = abs(captured_piece_number)-1

    if chess_board.color_to_move == WHITE:
        piece: Piece = chess_board.black_pieces[pos_in_piece_list]
    else: 
        piece: Piece = chess_board.white_pieces[pos_in_piece_list]
    
    piece.position[0] = to_x
    piece.position[1] = from_y
    piece.is_alive = True
    chess_board.board[to_x][to_y] = 0
    chess_board.board[to_x][from_y] = captured_piece_number

def undo_castling_move(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Undoes the last move if it was an castling move"""
    king_moving_direction = (-(from_x-to_x))//abs(from_x-to_x)

    if chess_board.color_to_move == WHITE:
        king_number = chess_board.board[chess_board.black_king_pos[0]][chess_board.black_king_pos[1]]
        king_in_piece_list = abs(king_number)
        king: Piece = chess_board.black_king_pos[king_in_piece_list]
    else:
        king_number = chess_board.board[chess_board.white_king_pos[0]][chess_board.white_king_pos[1]]
        king_in_piece_list = abs(king_number)-1
        king: Piece = chess_board.white_pieces[king_in_piece_list]

    chess_board.board[king.position[0]][king.position[1]] = 0
    king.position[0] = king.position[0] + 2*king_moving_direction
    chess_board.board[king.position[0]][king.position[1]] = king_number

    king.first_move = -1

    if chess_board.color_to_move == WHITE:
        chess_board.black_king_pos[0] = king.position[0]
        chess_board.black_king_pos[2] = -1
    else:
        chess_board.white_king_pos[0] = king.position[0]
        chess_board.white_king_pos[2] = -1

    undo_normal_move(chess_board, from_x, from_y, to_x, to_y, move_type)

def undo_promotion(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Undoes Promotion move"""
    piece_number = chess_board.board[to_x][to_y]
    pos_in_piece_list = abs(piece_number)-1

    if chess_board.color_to_move == WHITE:
        piece: Piece = chess_board.black_pieces[pos_in_piece_list]
        piece.rules = chess_board.black_pawn
    else:
        piece: Piece = chess_board.white_pieces[pos_in_piece_list]
        piece.rules = chess_board.white_pawn
    
    undo_normal_move(chess_board, from_x, from_y, to_x, to_y, move_type)

def save_in_last_moves(chess_board: ChessBoard, from_x, from_y, to_x, to_y, move_type):
    """Saves the move in the past_moves stack"""
    chess_board.past_moves[chess_board.move_count*5] = from_x
    chess_board.past_moves[chess_board.move_count*5+1] = from_y
    chess_board.past_moves[chess_board.move_count*5+2] = to_x
    chess_board.past_moves[chess_board.move_count*5+3] = to_y
    chess_board.past_moves[chess_board.move_count*5+4] = move_type

