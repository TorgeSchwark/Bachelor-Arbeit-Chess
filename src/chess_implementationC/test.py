import ctypes
from chess_implementationC.chess_board_wrapper import ChessBoard, clibrary


def run():
    board = ChessBoard()

    clibrary.setup_normals(ctypes.byref(board))

    clibrary.printChessBoard(ctypes.byref(board))