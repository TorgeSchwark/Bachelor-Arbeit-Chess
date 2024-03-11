from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece_rules import PieceRules
from chess_implementation.piece import Piece
from chess_implementation.move_stack import MoveStack
import numpy as np
from chess_implementation.chess_variables import *
from numba import jit 


def find_all_moves(chess_board: ChessBoard):
    """ Finds all move for the Player which has to move"""

    moves = MoveStack()
    for piece in chess_board.white_pieces if chess_board.color_to_move == 1 else chess_board.black_pieces:
        if piece.is_alive:
            if piece.rules.pawn:
                find_pawn_moves(chess_board, piece, moves)
            elif piece.rules.king:
                find_jump_moves(chess_board, piece, moves)
                find_move_directions(chess_board, piece, moves)
            else:
                if piece.rules.castling:
                    add_castling(chess_board, piece, moves)
                find_jump_moves(chess_board, piece, moves)
                find_move_directions(chess_board, piece, moves)
    return moves



def add_castling(chess_board: ChessBoard, piece: Piece, moves):
    """ Checks if castling is possible. If so it adds the castling move"""

    if chess_board.white_king_pos[2] != -1 or piece.first_move != -1:
        return
    else:
        color = chess_board.color_to_move
        if color == 1:
            king_pos = chess_board.white_king_pos
        else:
            king_pos = chess_board.black_king_pos

        #from king to piece
        is_free = True
        direction = (piece.position[0]-king_pos[0]) // abs(piece.position[0]-king_pos[0])
        field_x = king_pos[0] + direction
        field_y = king_pos[1]
        while  field_x != piece.position[0]:
            if chess_board.board[field_x][field_y] != 0:
                is_free = False 
            field_x += direction
        if is_free:
            add_move(piece.position[0], piece.position[1], king_pos[0] + direction, king_pos[1], moves, CASTLING)


def find_pawn_moves(chess_board: ChessBoard, piece: Piece, moves):
    """ Extra function to find pawn moves. Handles extra cases: double move, promotion"""
    
    pos_x = piece.position[0]
    pos_y = piece.position[1]
    size = chess_board.size
    color = chess_board.color_to_move
    board = chess_board.board

    if piece.first_move == -1:
        move_directions = [d * 2 if i % 3 == 2 else d for i, d in enumerate(piece.rules.move_directions)]
        double_move = True
    else: 
        double_move = False
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
            if board[field_x][field_y] == 0:
                if dist <= real_range and (not promotion(field_y, size, color)):
                    add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)
                elif dist >= real_range: #pawns cant promote in fist move!
                    add_move(pos_x, pos_y, field_x, field_y, moves, DOUBLE_PAWN)
                elif promotion(field_y, color, size):
                    add_promotions(pos_x, pos_y, field_x, field_y, moves, chess_board)
            else:
                break

            field_x += direction_x
            field_y += direction_y
            dist += 1
    
    direction_y = chess_board.color_to_move

    min_move_on_board_attack =  on_board(pos_x-1, size) and on_board(pos_y+direction_y, size) and (board[pos_x-1][pos_y+direction_y] * board[pos_x][pos_y] < 0) 
    plus_move_on_board_attack =  on_board(pos_x+1, size) and on_board(pos_y+direction_y, size) and (board[pos_x+1][pos_y+direction_y] * board[pos_x][pos_y] < 0)
    #diagonal capture Moves(on_board(x,y) and gegner and not_promotion field)
    if plus_move_on_board_attack and (not promotion(pos_y +direction_y,color, size)):
        add_move(pos_x, pos_y, pos_x+1,pos_y+direction_y, moves, NORMAL_MOVE)
    elif plus_move_on_board_attack and promotion(pos_y +direction_y,color, size):
        add_promotions(pos_x, pos_y, pos_x+1,pos_y+direction_y, moves, chess_board)
    if min_move_on_board_attack and (not promotion(pos_y +direction_y,color,size)):
        add_move(pos_x,pos_y, pos_x-1,pos_y+direction_y, moves, NORMAL_MOVE)
    elif min_move_on_board_attack and promotion(pos_y +direction_y,color,size):
        add_promotions(pos_x,pos_y, pos_x-1,pos_y+direction_y, moves, chess_board)
    
    add_en_passant(chess_board, piece, moves)


def add_en_passant(chess_board : ChessBoard, piece: Piece, moves):
    """ Checks if a piece can do en passant"""

    if chess_board.past_moves[(chess_board.move_count-1)*5+4] == DOUBLE_PAWN:
        color = chess_board.color_to_move
        last_move_to_x = chess_board.past_moves[(chess_board.move_count-1)*5+2]
        last_move_to_y = chess_board.past_moves[(chess_board.move_count-1)*5+3]
        if (piece.position[0] == last_move_to_x + 1 or piece.position[0]  == last_move_to_x - 1) and piece.position[1] == last_move_to_y:
            add_move(piece.position[0], piece.position[1], last_move_to_x, last_move_to_y + color, moves, EN_PASSANT)


def find_move_directions(chess_board: ChessBoard, piece: Piece, moves):
    """ finds all directional moves of a piece e.g. bishop"""

    move_directions = piece.rules.move_directions

    pos_x = piece.position[0]
    pos_y = piece.position[1]
    size = chess_board.size
    board = chess_board.board

    for ind in range(len(move_directions)//3):
        direction_x = move_directions[ind*3]
        direction_y = move_directions[ind*3+1]
        rangee = move_directions[ind*3+2]
        
        if rangee == 0:
            rangee = 99999

        dist = 1
        field_x  = pos_x + direction_x
        field_y  = pos_y + direction_y
        while dist <= rangee and (on_board(field_x, size) or piece.rules.boarder_x) and (on_board(field_y, size) or piece.rules.boarder_y): 
            
            field_x %= size
            field_y %= size

            if board[field_x][field_y] == 0:
                add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)
            elif (board[field_x][field_y] >= 0) == (board[pos_x][pos_y] >= 0):
                break
            else:
                add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)
                break

            field_x += direction_x
            field_y += direction_y
            dist += 1


def find_jump_moves(chess_board: ChessBoard, piece: Piece, moves):
    """ Finds jump moves for jumping pieces e.g. knight"""
    jump_moves = piece.rules.jump_moves

    pos_x = piece.position[0]
    pos_y = piece.position[1]
    size = chess_board.size
    board = chess_board.board

    for ind in range(len(jump_moves)//2):
        field_x = pos_x + jump_moves[ind*2]
        field_y = pos_y + jump_moves[ind*2+1]

        if (on_board(field_y, size) or piece.rules.boarder_y) and (on_board(field_x, size) or piece.rules.boarder_x):
            field_x %= size 
            field_y %= size
        else:
            continue
        
        if (board[field_x][field_y] >= 0) != (board[pos_x][pos_y] >= 0):
            add_move(pos_x, pos_y, field_x, field_y, moves, NORMAL_MOVE)


def add_move(from_x, from_y, to_x, to_y, moves: MoveStack, move_type):
    """ adds a move to the move stack"""
    move_ind = moves.head*5
    moves.stack[move_ind] = from_x
    moves.stack[move_ind+1] = from_y
    moves.stack[move_ind+2] = to_x
    moves.stack[move_ind+3] = to_y
    moves.stack[move_ind+4] = move_type
    moves.head += 1


def add_promotions(from_x,from_y, to_x, to_y, moves: MoveStack, chess_board: ChessBoard):
    """ Adds all possible transition options for promoting pieces on the move stack"""
    for ind in range(len(chess_board.all_non_pawn_pieces)):
        move_ind = moves.head*5
        moves.stack[move_ind] = from_x
        moves.stack[move_ind+1] = from_y
        moves.stack[move_ind+2] = to_x
        moves.stack[move_ind+3] = to_y
        moves.stack[move_ind+4] = ind
        moves.head += 1
    

def promotion(y, color, size):
    """ Check if a field is the last rank for that color"""
    if (color == 1 and y == size-1) or (color == -1 and y == 0):
        return True
    else:
        return False

def on_board(x,size):
    return (x >= 0 and x < size)