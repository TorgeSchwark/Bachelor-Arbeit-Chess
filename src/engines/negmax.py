from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
from chess_implementation.find_moves import find_all_moves
from chess_implementation.make_moves import make_move, undo_last_move
from engines.evaluations import basic_relative_evaluation
import ctypes
import tensorflow as tf
import numpy as np
import time

model_path = "/home/torge/Bachelor-Arbeit-Chess/models/lstm/logs/fit/lr0.001,patience20/best_model.h5"

#loaded_model = tf.keras.models.load_model(model_path)
loaded_model = None
positions = []
def test(board_pointer, depth, original_depth, alpha, beta, score, count):
    alpha_beta_basic(board_pointer, depth, original_depth, alpha, beta, score, count)
    if len(positions) > 0:
        repeated_positions = np.repeat(positions, 20)  # Jedes Element in positions wird 10 Mal wiederholt
        positions_array = np.array(repeated_positions)
        start = time.time()
        predictions = loaded_model.predict(positions_array, batch_size=5000)
        end = time.time()
        print(len(positions))
        print("this took", end-start)


def alpha_beta_basic(board_pointer, depth, original_depth, alpha, beta, score, count):
    """ Basic alpha beta engine to test the influence of Neural Networks in Alpha Beta"""
    count[0] += 1
    if depth == 0:
        NN_input  = (ctypes.c_int * 73)()
        chess_lib.board_to_NN_input(board_pointer, NN_input)
        NN_input_array = np.array(NN_input)
        positions.append(NN_input_array)
        start = time.time()
        #score[0] = loaded_model.predict(NN_input_array.reshape(1, -1))
        end = time.time()
       
        
        return 
    
    maxWert = alpha
    moves = (ctypes.c_byte * 2024)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(board_pointer, moves, ctypes.byref(move_count))
    best_move = 0
    score_next = [0]
    legal = (ctypes.c_bool * 200)()
    
    if depth == original_depth:
        chess_lib.legal_moves(board_pointer, move_count, moves, legal)

    for i in range(move_count.value //5):
        ind = i*5
        if depth == original_depth and not legal[i]:
            continue
        chess_lib.make_move(board_pointer, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4])
        alpha_beta_basic(board_pointer, depth-1, original_depth, -beta, -maxWert, score_next, count)
        chess_lib.undo_last_move(board_pointer)

        if -score_next[0] > maxWert:
            maxWert = -score_next[0]
            best_move = ind
            # if maxWert >= beta:
            #     break
    if(depth != original_depth):
        score[0] = maxWert
    else:
        print(maxWert)
        score[0] = best_move

        