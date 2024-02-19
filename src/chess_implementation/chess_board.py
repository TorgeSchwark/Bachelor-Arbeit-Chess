import numpy as np

class ChessBoard:

    def __init__(self):
        self.size = 0 #board >= 0 to < size
        self.in_setup_stage = True
        self.setup_board()

    def setup_board(self): #the boards are [[colo][col][col]]
        self.board = np.zeros((self.size, self.size),dtype=int) # board contains black piece_list_pos in negative numbers -1 and white piece pos in pos numbers +1

        self.white_pieces = np.empty(0,dtype=object)  # [pawn_rules,bishop_rules, ...]
        self.white_pieces_pos = np.empty(0,dtype=int) # [2,1,3,1,...] 2coordinates for each piece
        self.white_pieces_state = np.empty(0, dtype=bool) 

        self.black_pieces = np.empty(0,dtype=object)
        self.black_pieces_pos = np.empty(0,dtype=int)
        self.black_pieces_state = np.empty(0,dtype=bool)

        self.all_non_pawn_pieces = np.empty(0,dtype=int)

    def add_piece(self, piece, offset, start_pos, color):  #adds a piece for white and blacks side
        new_piece = True
        for pos in start_pos:
            x = pos[0] - offset
            y = pos[1] - offset
            print(x,y,offset)
            if y > self.size//2:
                raise Exception("White pieces are on the lower side!")
            
            self.white_pieces = np.append(self.white_pieces, piece)
            self.board[x][y] = len(self.white_pieces)  #position in piece list +1
            self.white_pieces_pos = np.append(self.white_pieces_pos,[x,y]) 
            self.white_pieces_state = np.append(self.white_pieces_state, True)

            self.black_pieces = np.append(self.black_pieces, piece)
            self.board[x][self.size-1-y] = -(len(self.black_pieces))  #negative position in piece list -1
            self.black_pieces_pos = np.append(self.black_pieces_pos,[x,self.size-1-y])
            self.black_pieces_state = np.append(self.black_pieces_state, True)

            if new_piece:
                new_piece = False
                self.all_non_pawn_pieces = np.append(self.all_non_pawn_pieces, len(self.white_pieces)-1) #for each unique piece save one index in piece list
                #when promoting later a move can be represented as (from,to,piece_ind)



    def set_size(self, size):
        self.size = size
        self.board = np.zeros((size, size))
        self.piece_board = np.zeros((size, size))

    def show_board(self):
        print("\n Board looks like this: " , self.board)
        print("\n")

        print("\n piece list white: ", self.white_pieces)
        print("\n piece_state white: ", self.white_pieces_state)
        print("\n piece_pos white: ", self.white_pieces_pos)
        print("\n")

        print("\n piece list black: ", self.black_pieces)
        print("\n piece_state black: ", self.black_pieces_state)
        print("\n piece_pos black: ", self.black_pieces_pos)
        print("\n ")

        print("\n all different pieces: ", self.all_non_pawn_pieces)

        for piece in self.white_pieces:
            piece.show_piece()
    


