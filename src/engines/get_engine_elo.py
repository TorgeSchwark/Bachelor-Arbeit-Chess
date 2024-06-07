from chess_implementationC.chess_board_wrapper import chess_lib, ChessBoard
import ctypes
from stockfish import Stockfish
from multiprocessing import Pool
import concurrent.futures
import sys

def find_out_elo_thread(game_amount, num_threads, min_elo, max_elo):
    while min_elo < max_elo:
        results = []
        
        with Pool(processes=num_threads) as pool:
            # Generate arguments for all tasks
            tasks = [(min_elo,) for _ in range(game_amount)]
            
            try:
                # Distribute tasks to the pool and wait for completion
                results = pool.starmap(enine_vs_stockfish, tasks)
            except KeyboardInterrupt:
                print("Caught KeyboardInterrupt, terminating workers")
                pool.terminate()
                pool.join()
                sys.exit(1)

        total_wins = sum(results)
        print(f"In ELO: {min_elo}, won {total_wins} out of {game_amount}")
        min_elo += 100

    return

def enine_vs_stockfish(elo):
    stockfish = Stockfish(path="/home/torge/Bachelor-Arbeit-Chess/src/chess_implementationC/Stockfish/stockfish/stockfish-ubuntu-x86-64-avx2")
    stockfish.set_elo_rating(elo)
    chess_lib.init_tables() #importand!
    chess_board_instance = ChessBoard()
    chess_lib.setup_normals(ctypes.byref(chess_board_instance))
    chess_lib.create_chess(ctypes.byref(chess_board_instance))
    avgs = [[0,0],[0,0],[0,0],[0,0]]
    
    fen = get_fen_string(chess_board_instance)
    matt = ctypes.c_float(0)
    valid = True
    while valid:
        carry_out_engine(chess_board_instance, avgs)
        chess_lib.is_check_mate(ctypes.byref(chess_board_instance), ctypes.byref(matt))

        if matt.value != 0:
            print(avgs, "won, ", matt.value)
            return matt.value
        fen = get_fen_string(chess_board_instance)
        if not stockfish.is_fen_valid(fen):
            break
        
        make_move_stockfish(chess_board_instance, stockfish)
        chess_lib.is_check_mate(ctypes.byref(chess_board_instance), ctypes.byref(matt))
        if matt.value != 0:
            print(avgs, "lost: ", matt.value)
            return 1 - matt.value
        
        fen = get_fen_string(chess_board_instance)
        valid = stockfish.is_fen_valid(fen)

    print("Wrong FEN", fen)
    return 0.5

def carry_out_engine(chess_board_instance, avgs):
    score2 = ctypes.c_int(0)
    
    count_quisque = ctypes.c_int(0)

    score2 = ctypes.c_int(0)
    chess_lib.alpha_beta_basic_quiesce(ctypes.byref(chess_board_instance),ctypes.c_int(6), ctypes.c_int(6), ctypes.c_int(-999999), ctypes.c_int(999999), ctypes.byref(score2), ctypes.byref(count_quisque))

    moves = (ctypes.c_byte * 2048)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(ctypes.byref(chess_board_instance), moves, ctypes.byref(move_count))
    make_move_by_ind(chess_board_instance, moves, score2.value)

def make_move_stockfish(chess_board, stockfish):
    
    fen = get_fen_string(chess_board)
    if(stockfish.is_fen_valid(fen)):
        stockfish.set_fen_position(fen)
    else:
        print(fen)
        
    moves = (ctypes.c_byte * 2048)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(ctypes.byref(chess_board), moves, ctypes.byref(move_count))
        
    move = stockfish.get_best_move()
    ind = find_real_move(chess_board, moves, move_count, move)
    make_move_by_ind(chess_board, moves, ind)

def make_move_by_ind(chess_board, moves, move_ind):
    chess_lib.make_move(ctypes.byref(chess_board), ctypes.c_byte(moves[move_ind]),ctypes.c_byte(moves[move_ind+1]), ctypes.c_byte(moves[move_ind+2]),ctypes.c_byte(moves[move_ind+3]),ctypes.c_byte(moves[move_ind+4]))

def find_real_move(chess_board, moves, move_count, move):
    piece = ctypes.create_string_buffer(2)
    piece[1] = b'\x00'
    piece[0] = 'x'.encode('utf-8')
    from_x = 7-(ord(move[0])- ord('a'))
    from_y = int(move[1]) -1

    to_x = 7-(ord(move[2])- ord('a'))
    to_y = int(move[3])-1
    if(len(move) > 4):
        piece[0] = move[4].encode('utf-8')
    ind = ctypes.c_int(0)
        
    chess_lib.real_move(ctypes.byref(chess_board), ctypes.c_byte(from_x), ctypes.c_byte(from_y), ctypes.c_byte(to_x), ctypes.c_byte(to_y), piece, moves, move_count, ctypes.byref(ind))
        
    return ind.value

def get_fen_string(board):
    fen_buffer = ctypes.create_string_buffer(556)
    chess_lib.board_to_fen(ctypes.byref(board), fen_buffer)
    return fen_buffer.value.decode('utf-8')  