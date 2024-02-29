import numpy as np
import copy
from chess_implementation.piece import Piece
class ChessBoard:

    def __init__(self):
        self.size = 0 #board >= 0 to < size
        self.has_king = False
        self.color_to_move = 1
        self.move_count = 0
        self.fifty_move_rule = 0
        self.all_non_pawn_pieces = np.empty(0,dtype=int)
        self.past_moves = np.empty(1000)
        self.board = np.zeros((self.size, self.size),dtype=int)
        self.white_pieces = np.zeros(0,dtype=object)
        self.black_pieces = np.zeros(0,dtype=object)

    def add_piece(self, piece_rule, offset, start_pos):  #adds a piece for white and blacks side
        if piece_rule.king:
            self.has_king = True
        new_piece = True
        for pos in start_pos:
            x = pos[0] - offset
            y = pos[1] - offset
            
            if y > self.size//2:
                raise Exception("White pieces are on the lower side!")
            
            white_piece = Piece(piece_rule)
            white_piece.position[0] = x 
            white_piece.position[1] = y 
            
            self.white_pieces = np.append(self.white_pieces, white_piece)
            self.board[x][y] = len(self.white_pieces)  #position in piece list +1
        

            black_piece_rules = copy.deepcopy(piece_rule)
            black_piece_rules.turn_black()

            black_piece = Piece(black_piece_rules)
            black_piece.position[0] = x
            black_piece.position[1] = self.size-1-y

            self.black_pieces = np.append(self.black_pieces, black_piece)
            self.board[x][self.size-1-y] = -(len(self.black_pieces))  #negative position in piece list -1
    

            if new_piece and not (piece_rule.king or piece_rule.pawn):
                new_piece = False
                self.all_non_pawn_pieces = np.append(self.all_non_pawn_pieces, len(self.white_pieces)-1) #for each unique piece save one index in piece list

    def set_size(self, size):
        self.size = size
        self.board = np.zeros((size, size))
        self.piece_board = np.zeros((size, size))

    def show_board(self):
        print("\n Board looks like this: " , self.board)
        print("\n")

        print("\n piece list white: ", self.white_pieces)
        print("\n")

        print("\n piece list black: ", self.black_pieces)
        print("\n ")

        print("\n all different pieces: ", self.all_non_pawn_pieces)

        for piece in self.white_pieces:
            piece.show_piece()
    


