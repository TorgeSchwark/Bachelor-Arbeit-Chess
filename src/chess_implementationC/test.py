import ctypes
from chess_board_wrapper import ChessBoard, chess_lib
import time
from timeit import default_timer as timer

def run():
    board = ChessBoard()

    chess_lib.setup_normals(ctypes.byref(board))

    chess_lib.create_chess(ctypes.byref(board))

    chess_lib.printChessBoard(ctypes.byref(board))

    value = get_fen_string(board)

    print(value)
    #board_ptr = ctypes.byref(board)
   
    # start = time.time()
    # chess_lib.test_engine(board_ptr, ctypes.c_int(8))
    # end = time.time()
    # print("time:", end-start)
 

def get_fen_string(board):
    # Erzeuge einen Puffer für den FEN-String (angenommen maximal 256 Zeichen lang)
    fen_buffer = ctypes.create_string_buffer(256)
    
    chess_lib.board_to_fen(ctypes.byref(board), fen_buffer)
    
    # Gib den FEN-String als Python-String zurück
    return fen_buffer.value.decode('utf-8')  # Dekodiere den C-String in Python-String


def python_chess_engine():
    games = 100

    board = ChessBoard()

    chess_lib.setup_normals(ctypes.byref(board))

    chess_lib.create_chess(ctypes.byref(board))

    


run()

