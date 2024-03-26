from chess_implementation.chess_board import ChessBoard
from chess_implementation.find_moves import find_all_moves
from chess_implementation.make_moves import make_move, undo_last_move
from engines.evaluations import basic_relative_evaluation


def negmax(chess_board: ChessBoard, depth, count):
    """
        this is a standart minmax engine 
        :param chess_board: the board information
        :depth the analys depth in half moves
    """
    count[0] += 1
    move = [0,0,0,0,0]
    if depth != 0:
        max = -99999999
        moves = find_all_moves(chess_board)
        for ind in range(moves.head):
            pos_ind = ind*5
            make_move(chess_board, moves.stack[pos_ind], moves.stack[pos_ind+1], moves.stack[pos_ind+2], moves.stack[pos_ind+3], moves.stack[pos_ind+4])
            score = -negmax(chess_board, depth-1, count)[0]
            undo_last_move(chess_board)
            if score > max:
                max = score
                move = [moves.stack[pos_ind], moves.stack[pos_ind+1], moves.stack[pos_ind+2], moves.stack[pos_ind+3], moves.stack[pos_ind+4]]
        
    else:
        max = basic_relative_evaluation(chess_board)
    return max, move
            
            

