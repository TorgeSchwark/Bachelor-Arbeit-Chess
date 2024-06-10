import tensorflow as tf
import numpy as np
import time
import ctypes
from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
from supervised_engines.fill_db import to_str

model_path = "/home/stu236894/Desktop/Bachelor-Arbeit-Chess/logs/fast_small/test_smal_model/best_model.keras"
loaded_model = tf.keras.models.load_model(model_path)

def nn_engine_ab(board, depth, original_depth, alpha, beta):
    
    if depth == 0:
        
        NN_input  = (ctypes.c_int * 73)()

        chess_lib.board_to_NN_input(board, NN_input)
        
        NN_input_array = np.array(NN_input)
        score = loaded_model(NN_input_array.reshape(1, -1))
        float_value = score.numpy()[0][0]
        print(float_value)
        return float_value

    moves = (ctypes.c_byte * 2000)()
    moves_count = ctypes.c_short(0)
    leagal = (ctypes.c_bool * 200)()
    sorted_ind = (ctypes.c_int * 200)()
    chess_lib.find_all_moves(board, moves, ctypes.byref(moves_count))
    maxWert = alpha
    
    chess_lib.legal_moves(board, moves_count, moves, leagal)
    
    for i in range(moves_count.value//5):
        if leagal[i] == False:
            continue
        ind = i*5
    
        chess_lib.make_move(board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4])
        eval = -nn_engine_ab(board, depth-1, original_depth, -beta, -maxWert)
        chess_lib.undo_last_move(board)

        if eval > maxWert:
            maxWert = eval
            best_move = ind
            if maxWert >= beta:
                break

    if depth != original_depth:
        return maxWert
    else:
        return best_move
        
        


