import numpy as np


#contains piece information that wont be changed
class PieceRules:

    def __init__(self):
        self.move_directions = np.empty(0)  #Triplets (x_direction,y_direction,how_far) how_far = 0 if no limits
        self.jump_moves = np.empty(0)
        self.boarder_x = False
        self.boarder_y = False 
        self.king = False 
        self.pawn = False 
        self.castling = False
        self.img_name = ""

    #recommended to use set_functions for inserting
    def set_boarder_x(self, value):
        if not (self.king or self.pawn or self.castling):
            self.boarder_x = value
    
    def set_boarder_y(self, value):
        if not (self.king or self.pawn or self.castling):
            self.boarder_y = value


    def set_king(self, value):
        if not (self.pawn or self.boarder_x or self.boarder_y):
            self.king = value
    

    def set_pawn(self, value):
        if not (self.king or self.boarder_x or self.boarder_y):
            self.pawn = value

        
    def set_start_pos(self, list):
        self.start_pos = list

    def set_castling(self, value):
        if not (self.boarder_x or self.boarder_y or self.pawn):
            self.castling = value

        
    def add_direction(self,tupel):
        add = True
        for ind in range(0,int(len(self.move_directions)/3)):
            if self.move_directions[ind*3] == tupel[0] and self.move_directions[ind*3+1] == tupel[1] and self.move_directions[ind*3+2] == tupel[2]:
                if add == False:
                    raise Exception("duplicate found")
                add = False
        if add:
            self.move_directions = np.append(self.move_directions,tupel)

    def add_jump_move(self, tupel):
        self.jump_moves = np.append(self.jump_moves, tupel)

    def set_image_path(self, image_path):
        self.img_name = image_path

    def show_piece(self):
        print("\n Move directions: ", self.move_directions)
        print("\n Jump Moves: ", self.jump_moves)
        print("\n Boarder_x, Boarder_y, King, Pawn, castling, img_path", self.boarder_x, self.boarder_y, self.king, self.pawn, self.castling, self.img_name)
    
    def turn_black(self):
        for i in range(len(self.move_directions)//3):
            self.move_directions[i*3] = -self.move_directions[i*3]
            self.move_directions[i*3+1] = -self.move_directions[i*3+1]
        for i in range(len(self.jump_moves)):
            self.jump_moves[i] = -self.jump_moves[i]


