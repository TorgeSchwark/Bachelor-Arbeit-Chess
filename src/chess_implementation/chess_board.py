import numpy as np

class ChessBoard:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.in_setup_stage = True
        self.setup_board()

    def setup_board(self):
        self.board = np.zeros(self.width* self.height)
        self.pieces = []

 
    
    


