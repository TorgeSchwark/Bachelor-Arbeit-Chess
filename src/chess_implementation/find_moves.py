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
    size = chess_board.size
    color = chess_board.color_to_move
    board = chess_board.board

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
        field_x  = pos_x+direction_x
        field_y  = pos_y+direction_y
        while dist <= rangee and on_board(field_x, size) and on_board(field_y,size):
            #promotion need extra case !!!!
            if board[field_x][field_y] == 0:
                if dist <= real_range and (not promotion(field_y, size, color)):
                    add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)
                elif dist >= real_range and (not promotion(field_y, size, color)):
                    add_move(pos_x, pos_y, field_x, field_y, moves, DOUBLE_PAWN)
                elif promotion(field_y, color, size):
                    add_promotions(pos_x, pos_y, field_x, field_y, moves, chess_board)
            else:
                break

            field_x += direction_x
            field_y += direction_y
            dist += 1
    
    direction_y = chess_board.color_to_move

    #diagonal capture Moves(on_board(x,y) and gegner and not_promotion field)
    if on_board(pos_x+1, size) and on_board(pos_y+direction_y, size) and (board[pos_x+1][pos_y+direction_y] * board[pos_x][pos_y] < 0) and (not promotion(pos_y +direction_y,size,color)):
        add_move(pos_x, pos_y, pos_x+1,pos_y+direction_y, moves, NORMAL_MOVE)
    elif on_board(pos_x+1, size) and on_board(pos_y+direction_y, size) and (board[pos_x+1][pos_y+direction_y] * board[pos_x][pos_y] < 0) and promotion(pos_y +direction_y,size,color):
        add_promotions(pos_x, pos_y, pos_x+1,pos_y+direction_y, moves, chess_board)
    if on_board(pos_x-1, size) and on_board(pos_y+direction_y, size) and (board[pos_x-1][pos_y+direction_y] * board[pos_x][pos_y] < 0) and (not promotion(pos_y +direction_y,size,color)):
        add_move(pos_x,pos_y, pos_x+1,pos_y+direction_y, moves, NORMAL_MOVE)
    elif on_board(pos_x-1, size) and on_board(pos_y+direction_y, size) and (board[pos_x-1][pos_y+direction_y] * board[pos_x][pos_y] < 0) and promotion(pos_y +direction_y,size,color):
        add_promotions(pos_x,pos_y, pos_x+1,pos_y+direction_y, moves, chess_board)
    
    #jump moves on a pawn dont make sense but any ways 
    find_jump_moves(chess_board, piece, moves)

def find_move_directions(chess_board: ChessBoard, piece: Piece, moves):

    move_directions = piece.rules.move_directions

    pos_x = piece.position[0]
    pos_y = piece.position[1]
    size = chess_board.size
    color = chess_board.color_to_move
    board = chess_board.board

    for ind in range(len(move_directions)//3):
        direction_x = move_directions[ind*3]
        direction_y = move_directions[ind*3+1]
        rangee = move_directions[ind*3+2]

        dist = 1
        field_x  = pos_x + direction_x
        field_y  = pos_y + direction_y
        while dist <= rangee and on_board(field_x, size) and on_board(field_y, size): 
            
            if board[field_x][field_y] == 0:
                add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)
            elif board[field_x][field_y] * board[pos_x][pos_y] > 0:
                break
            elif board[field_x][field_y] * board[pos_x][pos_y] < 0:
                add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)

            field_x += direction_x
            field_y += direction_y
            dist += 1


def find_jump_moves(chess_board: ChessBoard, piece: Piece, moves):

    jump_moves = piece.rules.jump_moves

    pos_x = piece.position[0]
    pos_y = piece.position[1]
    size = chess_board.size
    board = chess_board.board

    for ind in range(len(jump_moves)//2):
        field_x = pos_x + jump_moves[ind*2]
        field_y = pos_y + jump_moves[ind*2+1]
        
        if on_board(field_y, size) and on_board(field_x, size) and board[field_x][field_y] <= 0 :
            add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)





def add_move(from_x, from_y, to_x, to_y, moves: MoveStack, move_type):
    move_ind = moves.head
    moves.stack[move_ind*5] = from_x
    moves.stack[move_ind*5+1] = from_y
    moves.stack[move_ind*5+2] = to_x
    moves.stack[move_ind*5+3] = to_y
    moves.stack[move_ind*5+4] = move_type
    moves.head += 1

    

def add_promotions(from_x,from_y, to_x, to_y, moves: MoveStack, chess_board: ChessBoard):
    for ind in range(len(chess_board.all_non_pawn_pieces)):
        move_ind = moves.head
        moves.stack[move_ind*5] = from_x
        moves.stack[move_ind*5+1] = from_y
        moves.stack[move_ind*5+2] = to_x
        moves.stack[move_ind*5+3] = to_y
        moves.stack[move_ind*5+4] = ind
        moves.head += 1

def promotion(y, color, size):
    if (color == 1 and y == size-1) or (color == -1 and y == 0):
        return True
    return False

def on_board(x,size):
    return (x >= 0 and x < size)