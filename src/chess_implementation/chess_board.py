import numpy as np

class ChessBoard:

    def __init__(self):
        self.figure_ind_black = 1
        self.figure_ind_white = 2
        self.size = 0
        self.in_setup_stage = True
        self.setup_board()

    def setup_board(self): #the boards are [[colo][col][col]]
        self.board = np.zeros(self.size* self.size)
        self.figure_board = np.zeros(self.size*self.size)
        self.white_pieces = np.empty(0,dtype=object)
        self.black_pieces = np.empty(0,dtype=object)

    def add_figure(self, piece, offset, start_pos, color):  #adds a piece for white and blacks side

        for pos in start_pos:
            x = pos[0] - offset
            y = pos[1] - offset
            print(x,y,offset)
            if y > self.size//2:
                raise Exception("White pieces are on the lower side!")
            
            self.white_pieces = np.append(self.white_pieces, piece)
            self.board[x][y] = self.figure_ind_white
            self.figure_board[x][y] = len(self.white_pieces)*2
            self.figure_ind_white += 2

            self.black_pieces = np.append(self.black_pieces, piece)
            self.board[x][self.size-y] = self.figure_ind_black
            self.figure_board[x][self.size-1-y] = len(self.black_pieces)*2-1
            self.figure_ind_black += 2
            print("hallo")



    def set_size(self, size):
        self.size = size
        self.board = np.zeros((size, size))
        self.figure_board = np.zeros((size, size))

    def show_board(self):
        print("\n Board looks like this: " , self.board)
        print("\n figure_board looks like this " , self.figure_board)
        print("\n figure list white: ", self.white_pieces)
        print("\n figure list black: ", self.black_pieces)
    


