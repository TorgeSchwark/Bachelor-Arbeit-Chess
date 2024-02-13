import numpy as np

class chessBoard:

    def __init__(self):
        self.__move_directions = np.array()
        self.__attack_directions = np.array()
        self.__jumps = False
        self.__id = 0
        
    #adds a move possibility
    def add_move_direction(self, move_direction):
        if not move_direction in  self.__move_directions:
            self.__move_directions = np.append(self.__move_directions, move_direction)
    
    #adds multiple move directions at once
    def add_move_directions(self, move_directions):
        for move_direction in move_directions:
            if not move_directions in self.move_directions:
                self.__move_directions = np.concatenate(self.__move_directions, move_direction)

    #adds a attack possibility
    def add_attack_directions(self, attack_direction):
        if not attack_direction in  self.__move_directions:
            self.__attack_directions = np.append(self.__attack_directions, attack_direction)
    
    #adds multiple move directions at once
    def add_attack_directions(self, attack_directions):
        for attack_direction in attack_directions:
            if not attack_direction in self.move_directions:
                self.__attack_directions = np.concatenate(self.__attack_directions, attack_direction)
    
    def change_jumprights(self, value):
        self.__jumps = value

