import ctypes
from chess_board_wrapper import ChessBoard, chess_lib
import time
from timeit import default_timer as timer
import struct
import random

def run():
    board = ChessBoard()

    chess_lib.setup_normals(ctypes.byref(board))

    chess_lib.create_chess(ctypes.byref(board))

    chess_lib.printChessBoard(ctypes.byref(board))

    run_test_games(10, board)


def run_test_games(amount, board):
    play_test_game(board)
    # moves_buffer = ctypes.create_string_buffer(1024)
    # moves_count = ctypes.c_short(0)

    # chess_lib.find_all_moves(ctypes.byref(board), moves_buffer, ctypes.byref(moves_count))

    # moves_list = struct.unpack(f'{moves_count.value}b', moves_buffer.raw[:moves_count.value])

    # # chess_lib.make_move(ctypes.byref(board), moves_buffer[0], moves_buffer[1], moves_buffer[2], moves_buffer[3], moves_buffer[4] )
    # for i in range(amount):
    #     play_test_game(board)

    # print("Gefundene Züge als signed char:")
    # for move_value in moves_list:
    #     print(move_value)

    # chess_lib.make_move(ctypes.byref(board), ctypes.c_byte(moves_list[0]), ctypes.c_byte(moves_list[1]), ctypes.c_byte(moves_list[2]), ctypes.c_byte(moves_list[3]), ctypes.c_byte(moves_list[4]))

    # chess_lib.printChessBoard(ctypes.byref(board))

def play_test_game(board):
    
    moves_buffer = (ctypes.c_char * 1024)()
    
    moves_count = ctypes.c_short(0)

    chess_lib.find_all_moves(ctypes.byref(board), ctypes.byref(moves_buffer), ctypes.byref(moves_count))

    moves_list = struct.unpack(f'{moves_count.value}b', moves_buffer.raw[:moves_count.value])
    
    legal_list = (ctypes.c_bool * (moves_count.value//5))()

    chess_lib.legal_moves(ctypes.byref(board), moves_count.value, moves_buffer, legal_list)
    random_move_ind = generate_random_true_index(legal_list)
    print(moves_list[1])

    while random_move_ind != None:
        chess_lib.make_move(ctypes.byref(board), ctypes.c_byte(moves_list[random_move_ind*5]), ctypes.c_byte(moves_list[random_move_ind*5+1]), ctypes.c_byte(moves_list[random_move_ind*5+2]), ctypes.c_byte(moves_list[random_move_ind*5+3]), ctypes.c_byte(moves_list[random_move_ind*5+4]))
        moves_count = ctypes.c_short(0)

        chess_lib.find_all_moves(ctypes.byref(board), ctypes.byref(moves_buffer), ctypes.byref(moves_count))

        moves_list = struct.unpack(f'{moves_count.value}b', moves_buffer.raw[:moves_count.value])
        
        legal_list = (ctypes.c_bool * moves_count.value)()

        chess_lib.legal_moves(ctypes.byref(board), moves_count.value, moves_buffer, legal_list )
        random_move_ind = generate_random_true_index(legal_list)

    
    chess_lib.printChessBoard(ctypes.byref(board))
    chess_lib.find_all_moves(ctypes.byref(board), ctypes.byref(moves_buffer), ctypes.byref(moves_count))
    print("moves1 \n", moves_count.value)
    legal_list = (ctypes.c_bool * moves_count.value)()
    chess_lib.legal_moves(ctypes.byref(board), moves_count.value, moves_buffer, legal_list)
    for i in legal_list:
        print(i)
    print("moves2 \n", moves_count.value)
    print(get_fen_string(board))
    print("finished game")
    
    



def generate_random_true_index(bool_list):
    # Erstelle eine Liste der Indizes, bei denen der Wert True ist
    #print(bool_list)
    true_indices = [i for i, value in enumerate(bool_list) if value]
    #print(true_indices)
    # Überprüfe, ob es überhaupt True-Werte gibt
    if not true_indices:
        return None  # Rückgabe None, wenn keine True-Werte vorhanden sind

    # Wähle einen zufälligen Index aus der Liste der True-Indizes
    random_index = random.choice(true_indices)
    return random_index


def get_fen_string(board):
    # Erzeuge einen Puffer für den FEN-String (angenommen maximal 256 Zeichen lang)
    fen_buffer = ctypes.create_string_buffer(256)
    
    chess_lib.board_to_fen(ctypes.byref(board), fen_buffer)
    
    # Gib den FEN-String als Python-String zurück
    return fen_buffer.value.decode('utf-8')  # De

run()