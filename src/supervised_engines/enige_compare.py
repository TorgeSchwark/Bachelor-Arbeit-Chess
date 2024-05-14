from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
import ctypes
import time
from copy import deepcopy
from multiprocessing import Pool

board_all = None

def compare_engines_thread(chess_board_instance, games_amount=5000):
      # Erstelle einen Pool von Threads
    num_threads = 20  # Anzahl der Threads
    pool = Pool(4)
    board_all = chess_board_instance
    print(type(board_all))
    # Funktion, die in jedem Thread ausgeführt wird
    def compare_engines_in_thread(_):
        compare_engines( games_amount)

    # Starte die Threads
    pool.map(compare_engines,range(num_threads))

    # Schließe den Pool
    pool.close()
    pool.join()

def compare_engines(games_amount=100):
    games_amount= 500
    chess_board_instance = ChessBoard()
    chess_lib.setup_normals(ctypes.byref(chess_board_instance))
    chess_lib.create_chess(ctypes.byref(chess_board_instance))
    
    players = [0,0]
    for i in range(games_amount):
        result = play_game_engines(ctypes.byref(chess_board_instance))
        if(result[0] == 0):
            players[0] += result[1]
            players[1] += 1-result[1]
        else:
            players[1] += result[1]
            players[0] += 1-result[1]
        chess_lib.undo_game(ctypes.byref(chess_board_instance))
        

    print(players)

def play_game_engines(chess_board_instance):
    is_over = 0
    while not is_over:
        
        score2 = ctypes.c_int(0)
        chess_lib.alpha_beta_basic(chess_board_instance,ctypes.c_int(2), ctypes.c_int(2), ctypes.c_int(-999999), ctypes.c_int(999999), ctypes.byref(score2))
        make_move(score2.value, chess_board_instance)

        matt = ctypes.c_float(0)
        chess_lib.is_check_mate(chess_board_instance, ctypes.byref(matt))
        
        if matt.value != 0:
            return (0, matt.value)

        score2 = ctypes.c_int(0)
        chess_lib.alpha_beta_basic(chess_board_instance ,ctypes.c_int(2), ctypes.c_int(2), ctypes.c_int(-999999), ctypes.c_int(999999), ctypes.byref(score2))
        make_move(score2.value, chess_board_instance)

        matt = ctypes.c_float(0)
        chess_lib.is_check_mate(chess_board_instance, ctypes.byref(matt))
        if matt.value != 0:
            return (1, matt.value)
        
        


def make_move(move, chess_board_instance):
    legal_moves_c = (ctypes.c_byte * 2024)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(chess_board_instance, legal_moves_c, ctypes.byref(move_count))
    chess_lib.make_move(chess_board_instance , legal_moves_c[move], legal_moves_c[move+1], legal_moves_c[move+2], legal_moves_c[move+3], legal_moves_c[move+4])
