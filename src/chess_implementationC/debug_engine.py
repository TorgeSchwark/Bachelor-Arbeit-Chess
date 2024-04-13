import ctypes
from chess_board_wrapper import ChessBoard, chess_lib
import time
from timeit import default_timer as timer
import struct
import random
from stockfish import Stockfish

stockfish = Stockfish(path=".\src\chess_implementationC\Stockfish\stockfish-windows-x86-64.exe")

def perft_debug():
    board = ChessBoard()

    chess_lib.setup_normals(ctypes.byref(board))

    chess_lib.create_chess(ctypes.byref(board)) 

    chess_lib.test_engine(ctypes.byref(board), ctypes.c_int(6))

def run():
    board = ChessBoard()

    chess_lib.setup_normals(ctypes.byref(board))

    chess_lib.create_chess(ctypes.byref(board))

    # chess_lib.printChessBoard(ctypes.byref(board))

    run_test_games(1, board)


def run_test_games(amount, board):


    for i in range(amount):
        play_test_game(board)
        chess_lib.undo_game(ctypes.byref(board))

    # chess_lib.printChessBoard(ctypes.byref(board))

def play_test_game(board):
    
    moves_buffer = (ctypes.c_char * 2024)()

    move_count = 0
    
    moves_count = ctypes.c_short(0)

    chess_lib.find_all_moves(ctypes.byref(board), ctypes.byref(moves_buffer), ctypes.byref(moves_count))

    moves_list = struct.unpack(f'{moves_count.value}b', moves_buffer.raw[:moves_count.value])
    
    legal_list = (ctypes.c_bool * (moves_count.value//5))()

    chess_lib.legal_moves(ctypes.byref(board), moves_count.value, moves_buffer, legal_list)
    random_move_ind = generate_random_true_index(legal_list)

    while random_move_ind != None and move_count < 50:
        move_count += 1
        fen = get_fen_string(board)
        counts_buffer = (ctypes.c_longlong * 400)()
        chess_lib.count_for_each_move(ctypes.byref(board), 3, ctypes.byref(counts_buffer))

        # for i in range(moves_count.value//5):
        #     print(counts_buffer[i])
        
        # if not stockfish.is_fen_valid(fen):
        #     chess_lib.printChessBoard(ctypes.byref(board))
        #     print("SOCKFISH NOT VALID ")
        #     print(fen)
        

        chess_lib.make_move(ctypes.byref(board), ctypes.c_byte(moves_list[random_move_ind*5]), ctypes.c_byte(moves_list[random_move_ind*5+1]), ctypes.c_byte(moves_list[random_move_ind*5+2]), ctypes.c_byte(moves_list[random_move_ind*5+3]), ctypes.c_byte(moves_list[random_move_ind*5+4]))
        moves_count = ctypes.c_short(0)

        chess_lib.find_all_moves(ctypes.byref(board), ctypes.byref(moves_buffer), ctypes.byref(moves_count))

        moves_list = struct.unpack(f'{moves_count.value}b', moves_buffer.raw[:moves_count.value])
        
        legal_list = (ctypes.c_bool * moves_count.value)()

        chess_lib.legal_moves(ctypes.byref(board), moves_count.value, moves_buffer, legal_list )
        random_move_ind = generate_random_true_index(legal_list)


    print(get_fen_string(board),"\n")
    chess_lib.count_for_each_move(ctypes.byref(board), 6, ctypes.byref(counts_buffer))
    chess_lib.printChessBoard(ctypes.byref(board))
    # for i in range(moves_count.value//5):
    #     print(counts_buffer[i])
   
    
    
def generate_random_true_index(bool_list):
    
    true_indices = [i for i, value in enumerate(bool_list) if value]
    
    if not true_indices:
        return None  

    random_index = random.choice(true_indices)
    return random_index


def get_fen_string(board):
    
    fen_buffer = ctypes.create_string_buffer(556)
    
    chess_lib.board_to_fen(ctypes.byref(board), fen_buffer)
    
    return fen_buffer.value.decode('utf-8')  

run()
#perft_debug()