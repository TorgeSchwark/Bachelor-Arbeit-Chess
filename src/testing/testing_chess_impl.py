from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece_rules import PieceRules
from chess_implementation.piece import Piece
from chess_implementation.chess_variables import *
from chess_implementation.find_moves import find_all_moves
from chess_implementation.make_moves import make_move, undo_last_move
from chess_implementation.move_stack import MoveStack
from model.main_model import Model
import copy
import time

def test_engine(chess_board: ChessBoard, depth, count):
        count[0] += 1
        if depth > 0:
            #start_time = time.time()  # Timer starten
            moves = find_all_moves(chess_board)
            #find_moves_duration = time.time() - start_time  # Zeit für find_all_moves berechnen
            #test_sum[0] += find_moves_duration
            #print("find_all_moves duration:", find_moves_duration)
            for ind in range(moves.head):
                # chess_board_before = copy.deepcopy(chess_board)
               # start_time = time.time()  # Timer starten
                ind_pos = ind*5
                make_move(chess_board, moves.stack[ind_pos],moves.stack[ind_pos+1], moves.stack[ind_pos+2], moves.stack[ind_pos+3], moves.stack[ind_pos+4])
                #move_duration = time.time() - start_time  # Zeit für make_move berechnen

                #print("make_move duration:", move_duration , "  move_type  ", moves.stack[ind_pos+4])

                test_engine(chess_board, depth-1, count)
                
                #start_time = time.time()  # Timer starten
                undo_last_move(chess_board)
                #undo_duration = time.time() - start_time  # Zeit für undo_last_move berechnen
                #print("undo_last_move duration:", undo_duration, "  move_type  ", moves.stack[ind_pos+4])

                # if not chess_board.equals(chess_board_before):
                #     chess_board.show_board()
                #     chess_board_before.show_board()
                #     print("first error")
                #     print(moves.stack[ind*5],moves.stack[ind*5+1], moves.stack[ind*5+2], moves.stack[ind*5+3], moves.stack[ind*5+4])



