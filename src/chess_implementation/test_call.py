from chess_implementation.chess_board import ChessBoard
import chess_implementation.chess as chess

def run():
    chess_board_python = ChessBoard()
    chess_board_python.size = 3
    chess.convert(chess_board_python)
    