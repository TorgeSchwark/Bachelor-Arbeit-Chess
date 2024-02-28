from chess_implementation.piece_rules import PieceRules
import numpy as np 

class Piece:

    def __init__(self, piece_rules: PieceRules):

        self.rules = piece_rules
        self.is_alive = True
        self.position =  np.empty(2)
        self.first_move = 0
        