from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece import Piece
import numpy as np
from chess_implementation.chess_variables import *

def find_all_moves(chess_board: ChessBoard):
    
    if chess_board.color_to_move == 1:
        pieces = chess_board.white_pieces
        pieces_pos = chess_board.white_pieces_pos
        pieces_start_pos = chess_board.white_pieces_start_pos
        pieces_state = chess_board.white_pieces_state
    else:
        pieces = chess_board.black_pieces_pos
        pieces_pos = chess_board.black_pieces_pos
        pieces_start_pos = chess_board.black_pieces_start_pos
        pieces_state = chess_board.black_pieces_state

    move_list = np.zeros(1000)
    move_ind = 0
    for ind in range(len(pieces_pos)):
        if pieces_state[ind]: #piece is alive
            piece_pos = (pieces_pos[ind*2], pieces_pos[ind*2+1])
            piece = pieces[ind]
            piece_start_pos = (pieces_start_pos[ind*2], pieces_start_pos[ind*2+1])
            find_piece_moves(piece, piece_pos, piece_start_pos, chess_board, move_list, move_ind)
    

def find_piece_moves(piece: Piece, piece_pos, piece_start_pos, chess_board: ChessBoard, move_list, move_ind): #do we need whole chessBoard or only board
    if piece.pawn:
        find_pawn_moves(piece, piece_pos, piece_start_pos, chess_board.board, move_list, move_ind)
    elif piece.king:
        #add_castling_moves(piece, piece_pos, chess_board.board)
        pass
    else:
        jump_moves(piece, piece.jump_moves, piece_pos, chess_board,  move_list, move_ind, False)
        move_directions(piece.move_directions, piece_pos, chess_board.board,  move_list, move_ind, False)
    if piece.castling:
        add_castling()

#extra becouse cant atack on normal moves...
def find_pawn_moves(piece: Piece, piece_pos, piece_start_pos, chess_board: ChessBoard, move_list, move_ind):
    if piece_start_pos == piece_pos:
        doble_moves = np.copy(piece.move_directions)
        doble_moves[2::3] *= 2 #doble reach of every directional move
        move_directions(piece, doble_moves, piece_pos, piece_start_pos, chess_board, move_list, move_ind, True)
    else:
        move_directions(piece, piece.move_directions, piece_pos, piece_start_pos, chess_board, move_list, move_ind, True)

    jump_moves(piece, piece.move_directions, piece_pos, piece_start_pos, chess_board, move_list, move_ind, True)
    add_en_passant_moves(piece_pos, chess_board, move_list, move_ind, True)


def add_en_passant_moves(piece_pos, chess_board: ChessBoard, move_list, move_ind):
    direction = chess_board.color_to_move
    last_move_type = chess_board.past_moves[chess_board.move_count*5 -1]
    last_move_to_y = chess_board.past_moves[chess_board.move_count*5 -2]
    last_move_to_x = chess_board.past_moves[chess_board.move_count*5 -3]
    if chess_board.move_count >= 0 and last_move_type == -4 and piece_pos[1] == last_move_to_y and abs(piece_pos[0]-last_move_to_x) == 1:
        add_move(move_list, move_ind, piece_pos[0], piece_pos[1],last_move_to_x, piece_pos[1]+direction, EN_PASSEN, chess_board)

def jump_moves(piece: Piece, piece_jump_moves, piece_pos, piece_start_pos, chess_board: ChessBoard, move_list, move_ind, pawn):
    size = chess_board.size
    board = chess_board.board
    for i in range(len(piece_jump_moves)//2):
        x_direction = piece_jump_moves[i*2]
        y_direction = piece_jump_moves[i*2+1]

        go_to_x = piece_pos[0] + x_direction
        go_to_y = piece_pos[1] + y_direction

        if not on_board(go_to_y, size) and not piece.boarder_y:
            continue
        elif not on_board(go_to_x, size) and not piece.boarder_x:
            continue
        #ether x and y are on board or piece is allowed to move beyond:
        go_to_y %= size 
        go_to_x %= size

        if board[go_to_x][go_to_y]* board[piece_pos[0]][piece_pos[1]] > 0:
            continue
        elif board[go_to_x][go_to_y] == 0 and not pawn:
            add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, NORMAL_MOVE, chess_board)
            continue
        elif board[go_to_x][go_to_y] == 0 and pawn:
            if (chess_board.color_to_move == 1 and go_to_y == size-1) or (chess_board.color_to_move == -1 and go_to_y == 0):
                add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, PROMOTION, chess_board)
            else:
                add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, NORMAL_MOVE, chess_board)
        elif board[go_to_x][go_to_y]* board[piece_pos[0]][piece_pos[1]] < 0 and not pawn:
            add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, NORMAL_MOVE, chess_board)    
            continue

#range missing
def move_directions(piece: Piece, piece_move_directions, piece_pos, piece_start_pos, chess_board: ChessBoard, move_list, move_ind, pawn):
    size = chess_board.size
    board = chess_board.board
    for ind in range(len(piece_move_directions)//3):
        go_to_x = piece_pos[0]
        go_to_y = piece_pos[1]
        direction_x = piece_move_directions[ind*3]
        direction_y = piece_move_directions[ind*3+1]
        rangee = piece_move_directions[ind*3+2]
        run = True
        count_dist = 0
        while run:
            count_dist += 1
            if count_dist > rangee:
                break 
            go_to_x += direction_x
            go_to_y += direction_y
            if not on_board(go_to_y, size) and not piece.boarder_y:
                break
            elif not on_board(go_to_x, size) and not piece.boarder_x:
                break

            go_to_y %= size 
            go_to_x %= size

            if board[go_to_x][go_to_y] * board[go_to_x][go_to_y] > 0: #same color
                break
            elif board[go_to_x][go_to_y] == 0 and not pawn:
                add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, NORMAL_MOVE, chess_board)
                continue
            elif board[go_to_x][go_to_y] == 0 and pawn:
                if piece_pos == piece_start_pos and count_dist > rangee//2:
                    add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, DOUBLE_PAWN, chess_board)
                else:
                    if (chess_board.color_to_move == 1 and go_to_y == size-1) or (chess_board.color_to_move == -1 and go_to_y == 0):
                        add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, PROMOTION, chess_board)
                    else:
                        add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, NORMAL_MOVE, chess_board)
            elif board[go_to_x][go_to_y] * board[go_to_x][go_to_y] < 0 and not pawn: #enemy
                add_move(move_list, move_ind, piece_pos[0], piece_pos[1], go_to_x, go_to_y, NORMAL_MOVE, chess_board )
                break

def add_move(move_list, move_ind, from_x, from_y, go_to_x, go_to_y, move_type, chess_board: ChessBoard):
    if move_type != PROMOTION:
        move_list[move_ind] = from_x
        move_list[move_ind+1] = from_y
        move_list[move_ind+2] = go_to_x
        move_list[move_ind+3] = go_to_y
        move_list[move_ind+4] = move_type

        move_ind += 5
    else:
        for piece_ind in range(len(chess_board.all_non_pawn_pieces)):
            move_list[move_ind] = from_x
            move_list[move_ind+1] = from_y
            move_list[move_ind+2] = go_to_x
            move_list[move_ind+3] = go_to_y
            move_list[move_ind+4] = piece_ind

            move_ind += 5

def add_castling(piece: Piece, ):


def on_board(x,size):
    return (x >= 0 and x < size)