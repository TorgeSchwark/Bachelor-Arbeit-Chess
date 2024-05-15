from chess_implementationC.chess_board_wrapper import chess_lib, ChessBoard
import ctypes
from stockfish import Stockfish
from multiprocessing import Pool

stockfish = Stockfish(path=".\src\chess_implementationC\Stockfish\stockfish-windows-x86-64.exe")
stockfish.set_elo_rating(1300)

def find_out_elo_thread(game_amount, num_threads, min_elo, max_elo):
    if game_amount%num_threads == 0:
        while min_elo < max_elo:
            
            itterations = game_amount/num_threads
            pool = Pool(num_threads)
            results = []
            
            for i in range(itterations):
                pool.map(enine_vs_stockfish, range(num_threads), min_elo)

                pool.close()
                pool.join()

            print("in elo: ", min_elo, " won ", results, " out of ", game_amount)
            min_elo += 100

def find_out_elo(chess_board_instance):
    chess_lib.printChessBoard(ctypes.byref(chess_board_instance))
    for i in range(8):
        stockfish.set_elo_rating(2000 +100*i)
        won_games = 0
        for m in range(50):
            value = enine_vs_stockfish(chess_board_instance)
            print("game ended",value)
            chess_lib.undo_game(ctypes.byref(chess_board_instance))
            won_games += value
        print("elo ", 2000+100*i ," won ", won_games, " form " , 10)


def enine_vs_stockfish(elo):
    stockfish = Stockfish(path=".\src\chess_implementationC\Stockfish\stockfish-windows-x86-64.exe")
    stockfish.set_elo_rating(elo)

    chess_board_instance = ChessBoard()
    chess_lib.setup_normals(ctypes.byref(chess_board_instance))
    chess_lib.create_chess(ctypes.byref(chess_board_instance))
        
    fen = get_fen_string(chess_board_instance)
    matt = ctypes.c_float(0)
    while stockfish.is_fen_valid(fen):
            
        carry_out_engine(chess_board_instance)
        chess_lib.is_check_mate(ctypes.byref(chess_board_instance), ctypes.byref(matt))
        if(matt.value != 0):
            return matt.value 
           
        make_move_stockfish(chess_board_instance)
        chess_lib.is_check_mate(ctypes.byref(chess_board_instance), ctypes.byref(matt))
        if matt.value != 0:
            return 1-matt.value 
            
        fen = get_fen_string(chess_board_instance)

    print("wrong fen", fen)
    return 0.5


def carry_out_engine(chess_board_instance):
    score2 = ctypes.c_int(0)
    chess_lib.advanced_apha_beta_engine(ctypes.byref(chess_board_instance),ctypes.c_int(5), ctypes.c_int(5), ctypes.c_int(-999999), ctypes.c_int(999999), ctypes.byref(score2))

    moves = (ctypes.c_byte * 2048)()
    move_count = ctypes.c_short(0)
    chess_lib.find_all_moves(chess_board_instance, moves, ctypes.byref(move_count))
    make_move_by_ind(chess_board_instance, moves, score2.value)

def make_move_stockfish(chess_board):
        fen = get_fen_string(chess_board)
        if(stockfish.is_fen_valid(fen)):
            stockfish.set_fen_position(fen)
        else:
            print(fen)
        
        moves = (ctypes.c_byte * 2048)()
        move_count = ctypes.c_short(0)
        chess_lib.find_all_moves(chess_board, moves, ctypes.byref(move_count))
        
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