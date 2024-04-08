import ctypes
from chess_board_wrapper import ChessBoard, chess_lib
import time
from timeit import default_timer as timer

def run():
    board = ChessBoard()

    chess_lib.setup_normals(ctypes.byref(board))

    chess_lib.create_chess(ctypes.byref(board))

    chess_lib.printChessBoard(ctypes.byref(board))

    array_size = 500
    array_data = [0] * array_size

    # Das Array in ein ctypes-Array umwandeln
    ctypes_array = (ctypes.c_byte * array_size)(*array_data)

    # Die Funktion aufrufen und den Zeiger übergeben
    board_ptr = ctypes.byref(board)
    
    # start = timer()
    # chess_lib.find_all_moves(board_ptr, ctypes_array, ctypes.byref(move_couts))
    # end = timer()

    # print(end-start)

    # print(ctypes_array[0])

    # print("ctypes_array:")
    # for ind in range(move_couts.value//5):
    #     print("(",ctypes_array[ind*5],",", ctypes_array[ind*5+1],") -> (",ctypes_array[ind*5+2],",",ctypes_array[ind*5+3],")",ctypes_array[ind*5+4])
    #chess_lib.printChessBoard(ctypes.byref(board))
    start = time.time()
    chess_lib.test_engine(board_ptr, ctypes.c_int(7))
    end = time.time()
    print("time:", end-start)
    #chess_lib.printChessBoard(ctypes.byref(board))

    #außen 1*2 + innen 2*6 + dame 2+ läufer 2*2*3  springer weiß 4 = 2+ 12+ 1+ 24 +4 = 34
    # make_moves_lib.make_move(board_ptr, ctypes_array[0],ctypes_array[1],ctypes_array[2],ctypes_array[3],ctypes_array[4])
    # chess_board_lib.printChessBoard(board_ptr)


#     start = timer()
#     end = timer()

#     print(end-start)

def test(board_ptr, depth):
    start = time.time()
    chess_lib.test_engine(board_ptr, ctypes.c_int(depth))
    end = time.time()
    print("time:", end-start)
    #chess_lib.printChessBoard(board_ptr)

run()