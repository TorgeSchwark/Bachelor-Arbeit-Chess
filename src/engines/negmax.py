from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
from chess_implementation.find_moves import find_all_moves
from chess_implementation.make_moves import make_move, undo_last_move
from engines.evaluations import basic_relative_evaluation
import ctypes



def alpha_beta_basic(board_pointer, depth, original_depth, alpha, beta, score):
    if depth == 0:
        return chess_lib.eval(board_pointer)
    
    maxWert = alpha
    moves = (ctypes.c_byte * 2024)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(board_pointer, moves, ctypes.byref(move_count))
    best_move = 0
    score_next = [0]
    legal = (ctypes.c_bool * 200)
    
    if depth == original_depth:
        chess_lib.lega_moves(board_pointer, move_count, moves, legal)

    for i in range(move_count//5):
        ind = i*5
        if depth == original_depth and not legal[i]:
            continue
        chess_lib.make_move(board_pointer, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4])
        alpha_beta_basic(board_pointer, depth-1, original_depth, -beta, -maxWert, score_next)
        chess_lib.undo_last_move(board_pointer)

        if -score_next[0] > maxWert:
            maxWert = -score_next[0]
            best_move = ind
            if maxWert >= beta:
                break

    score[0] = maxWert

        