from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece import Piece
from chess_implementation.chess_variables import *
from chess_implementation.find_moves import find_all_moves

def basic_relative_evaluation(chess_board: ChessBoard):
    """
        A basic relative evaluation which gives 4 points for knight 4.5 for a bishop 6 for a rook 9 for a queen and 1 for a Pawn
        also uses find_all_moves to evaluate a mobility score.
    """
    materialScore = 0

    for piece in chess_board.white_pieces:
        if piece.is_alive:
            if piece.rules.pawn:
                materialScore += 1
            elif piece.rules.king:
                materialScore += 100
            else:
                materialScore += len(piece.rules.jump_moves)/8*4
                for ind in range(len(piece.rules.move_directions)//3):
                    ind_pos = ind*3
                    move_range = piece.rules.move_directions[ind_pos] 
                    if move_range == 0:
                        materialScore += 9/8
                    else:
                        materialScore += move_range//chess_board.size*1.5
                if piece.rules.castling:
                    materialScore += 1.5

    for piece in chess_board.black_pieces:
        if piece.is_alive:
            if piece.rules.pawn:
                materialScore -= 1
            elif piece.rules.king:
                materialScore -= 100
            else:
                materialScore -= len(piece.rules.jump_moves)/8*4
                for ind in range(len(piece.rules.move_directions)//3):
                    ind_pos = ind*3
                    move_range = piece.rules.move_directions[ind_pos] 
                    if move_range == 0:
                        materialScore -= 9/8
                    else:
                        materialScore -= move_range//chess_board.size*1.5
                if piece.rules.castling:
                    materialScore -= 1.5

    save_color = chess_board.color_to_move
    chess_board.color_to_move = WHITE
    white_moves = find_all_moves(chess_board)
    chess_board.color_to_move = BLACK
    black_moves = find_all_moves (chess_board)
    chess_board.color_to_move = save_color

    mobility_score = (white_moves.head- black_moves.head) * 0.1

    return (materialScore)*chess_board.color_to_move
        
                