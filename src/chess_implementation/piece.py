from chess_implementation.piece_rules import PieceRules
import numpy as np 

class Piece:

    def __init__(self, piece_rules: PieceRules):

        self.rules = piece_rules
        self.is_alive = True
        self.position =  np.zeros(2, dtype=int)
        self.first_move = -1
        
    def show_piece(self):
        print("\n is_alive : ", self.is_alive)
        print("\n postion : ", self.position)
        print("\n first_move : ", self.first_move)
        self.rules.show_piece()