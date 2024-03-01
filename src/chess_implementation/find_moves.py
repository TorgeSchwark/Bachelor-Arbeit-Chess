from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece_rules import PieceRules
from chess_implementation.piece import Piece
from chess_implementation.move_stack import MoveStack
import numpy as np
from chess_implementation.chess_variables import *

def find_all_moves(chess_board: ChessBoard):
    print("1")
    if chess_board.color_to_move == 1:
        pieces = chess_board.white_pieces
    else:
        pieces = chess_board.black_pieces
    
    moves = MoveStack()
    for ind in range(len(pieces)):
        piece: Piece = pieces[ind]
        if piece.is_alive:
            find_piece_moves(chess_board, piece, moves)
    return moves


def find_piece_moves(chess_board, piece, moves):
    if piece.rules.pawn:
        find_pawn_moves(chess_board, piece, moves)

def find_pawn_moves(chess_board: ChessBoard, piece: Piece, moves):
    
    pos_x = piece.position[0]
    pos_y = piece.position[1]

    if piece.first_move == -1:
        move_directions = piece.rules.move_directions.copy()
        move_directions[2::3] *= 2
        double_move = True
    else: 
        double_move == False
        move_directions = piece.rules.move_directions
    
    #could also chose to make a backwards running pawn!
    #Move directions double if pawn hasnt moved
    for ind in range(len(move_directions)//3):
        direction_x = move_directions[ind*3]
        direction_y = move_directions[ind*3+1]
        rangee = move_directions[ind*3+2]
        if double_move:
            real_range = rangee // 2
        else: 
            real_range = rangee

        dist = 1
        field_x  = pos_x
        field_y  = pos_y
        while dist <= rangee:
            field_x += direction_x
            field_y += direction_y
            
            #promotion need extra cas !!!!
            if chess_board.board[field_x][field_y] == 0:
                if dist <= real_range:
                    add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)
                else:
                    add_move(pos_x, pos_y, field_x, field_y, moves, DOUBLE_PAWN)
            else:
                break
            dist += 1
    
    direction_y = chess_board.color_to_move
    #diagonal capture Moves
    if chess_board[field_x+1][field_y+direction_y] * chess_board[pos_x][pos_y] < 0:
        add_move(pos_x,pos_y, field_x+1,field_y+direction_y, moves, NORMAL_MOVE)
    if chess_board[field_x-1][field_y+direction_y] * chess_board[pos_x][pos_y] < 0:
        add_move(pos_x,pos_y, field_x+1,field_y+direction_y, moves, NORMAL_MOVE)

    #jump moves on a pawn dont make sense but any ways 
    #add_jump_moves(chess_board: ChessBoard, piece: Piece, moves)

def add_move(from_x, from_y, to_x, to_y, moves: MoveStack, move_type):
    if move_type != PROMOTION:
        move_ind = moves.head
        moves.stack[move_ind*5] = from_x
        moves.stack[move_ind*5+1] = from_y
        moves.stack[move_ind*5+2] = to_x
        moves.stack[move_ind*5+3] = to_y
        moves.stack[move_ind*5+4] = move_type
        moves.head += 1
    else:
        pass



def on_board(x,size):
    return (x >= 0 and x < size)