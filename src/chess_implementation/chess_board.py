import copy

import numpy as np

from chess_implementation.piece import Piece
from chess_implementation.piece_rules import PieceRules


class ChessBoard:

    def __init__(self):
        self.size = 0 #board >= 0 to < size
        self.has_king = False
        self.white_king_pos = np.empty(3, dtype=int)
        self.white_king_pos[2] = -1
        self.black_king_pos = np.empty(3, dtype=int)
        self.white_king_pos[2] = -1
        self.color_to_move = 1
        self.move_count = 0
        self.fifty_move_rule = 0
        self.all_non_pawn_pieces = np.zeros(0,dtype=int)
        self.past_moves = np.zeros(1000, dtype= int)
        self.board = np.zeros((self.size, self.size),dtype=int)
        self.white_pieces = np.zeros(0,dtype=object)
        self.black_pieces = np.zeros(0,dtype=object)


    def add_piece(self, piece_rule: PieceRules, offset, start_pos):  #adds a piece for white and blacks side
        if (piece_rule.king and self.has_king) or (piece_rule.king and len(start_pos) > 1) :
            print("game already has a king or can only have one king !")

        elif piece_rule.castling and not (self.has_king or piece_rule.king):
            print("add king before castling pieces")
        else:
            
            if piece_rule.castling and not piece_rule.king:
                for ind in range(len(start_pos)):
                    print(start_pos[ind], self.white_king_pos[1])
                    if start_pos[ind][1]-offset != self.white_king_pos[1]:
                        print("castling pieces mus be in the same row as the king")
                        return 

            new_piece = True
            for pos in start_pos:
                print(offset, "offset")
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

                if piece_rule.king:
                    self.white_king_pos[0] = x
                    self.white_king_pos[1] = y 
                    self.black_king_pos[0] = x 
                    self.black_king_pos[1] = self.size-1-y
                    self.has_king = True

                if new_piece and not (piece_rule.king or piece_rule.pawn):
                    new_piece = False
                    self.all_non_pawn_pieces = np.append(self.all_non_pawn_pieces, len(self.white_pieces)-1) #for each unique piece save one index in piece list


    def set_size(self, size):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)


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
    


