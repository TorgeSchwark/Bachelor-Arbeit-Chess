import numpy as np

class Piece:

    def __init__(self):
        self.move_directions = np.array()  #Triplets (x_direction,y_direction,how_far) how_far = 0 if no limits
        self.jump_moves = np.array()
        self.id = 0
        self.boarder_x = False
        self.boarder_y = False 
        self.king = False 
        self.pawn = False 
        self.castling = False

    #recommended to use set_functions for 

    def set_boarder_x(self, value):
        if not (self.king or self.pawn or self.castling):
            self.boarder_x = value
        else: 
            raise Exception
    
    def set_boarder_y(self, value):
        if not (self.king or self.pawn or self.castling):
            self.boarder_y = value
        else: 
            raise Exception

    def set_king(self, value):
        if not (self.pawn or self.boarder_x or self.boarder_y):
            self.king = value
        else: 
            raise Exception

    def set_pawn(self, value):
        if not (self.king or self.boarder_x or self.boarder_y):
            self.pawn = value
        else: 
            raise Exception

    def set_castling(self, value):
        if not (self.boarder_x or self.boarder_y or self.pawn):
            self.castling = value
        else:
            raise Exception
        
    

