import ctypes
from chess_board_wrapper import ChessBoard, chess_board_lib, find_moves_lib
import time
from timeit import default_timer as timer

def run():
    board = ChessBoard()

    chess_board_lib.setup_normals(ctypes.byref(board))

    chess_board_lib.create_chess(ctypes.byref(board))

    chess_board_lib.printChessBoard(ctypes.byref(board))

    array_size = 500
    array_data = [0] * array_size

    # Das Array in ein ctypes-Array umwandeln
    ctypes_array = (ctypes.c_int * array_size)(*array_data)

    # Die Funktion aufrufen und den Zeiger übergeben
    board_ptr = ctypes.byref(board)
    move_couts = ctypes.byref(ctypes.c_short(0))

    start = timer()
    find_moves_lib.find_all_moves(board_ptr, ctypes_array, move_couts)
    end = timer()

    print(end-start)

#     start = timer()
#     end = timer()

#     print(end-start)
    
run()