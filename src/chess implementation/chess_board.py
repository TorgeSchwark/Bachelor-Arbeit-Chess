import numpy as np

class chessBoard:

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__in_setup_stage = True

    def setup_board(self):
        self.__board = np.zeros(self.__width* self.height)
        self.pieces = np.array()

 
    
    


