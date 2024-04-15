# from chess_implementation.chess_board import ChessBoard
# from chess_implementation.piece_rules import PieceRules
# from chess_implementation.piece import Piece
from chess_implementation.chess_variables import *
# from chess_implementation.find_moves import find_all_moves
# from chess_implementation.make_moves import make_move, undo_last_move
# from chess_implementation.move_stack import MoveStack
from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
import ctypes

from testing.testing_chess_impl import test_engine
from testing.play_game_testing import play_game_test
from views.View import View
import customtkinter as ctk
from views.view_variables import *
from PIL import Image
import random
from copy import deepcopy
import time
from multiprocessing import Pool
from testing.play_setup import play_game
from engines.negmax import negmax
import struct

class PlayGameView(View):
    
    def __init__(self, master, controller):

        self.legal_moves_c = (ctypes.c_char * 2024)()
        self.move_count = ctypes.c_short(0)
        self.moves_list = struct.unpack(f'{self.move_count.value}b', self.legal_moves_c.raw[:self.move_count.value])
        
        self.first_click = (-1,-1)
        self.second_click = (-1,-1)
        self.controller = controller
        self.position = (0,0)
        self.master = master
        
        self.chess_board_instance: ChessBoard = controller.board_instance

        print("hier", chess_lib.eval(ctypes.byref(self.chess_board_instance)))


        chess_lib.printChessBoard(ctypes.byref(self.chess_board_instance))

        self.place_main_objects()

    def place_main_objects(self):
        self.main_frame = ctk.CTkFrame(master=self.master, border_width=2)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(expand=True, fill="both")
        self.min_canvas_size = self.master.winfo_height() - 100

        self.settings_frame = ctk.CTkFrame(master=self.main_frame, border_width=2)
        self.settings_frame.pack(side="left", expand=True, fill="both")
        self.settings_frame.pack_propagate(False)

        self.board_frame = ctk.CTkFrame(master=self.main_frame, border_width=2)
        self.board_frame.pack(side="left", expand=True, fill="both")

        self.board_castling_switch_var = ctk.StringVar(value="off")
        self.board_castling_switch = ctk.CTkSwitch(master=self.settings_frame, text="castling", variable=self.board_castling_switch_var, onvalue="on", offvalue="off")
        self.board_castling_switch.pack(expand=False, padx=20,pady=10)

        self.main_menu_button = ctk.CTkButton(master=self.settings_frame, text="Back to Menu", command=self.controller.main_menu)
        self.main_menu_button.pack(expand=False, padx=20, pady=5)

        self.initial_setup()

    def initial_setup(self):
        chess_lib.find_all_moves(ctypes.byref(self.chess_board_instance),self.legal_moves_c, ctypes.byref(self.move_count))
        self.moves_list = struct.unpack(f'{self.move_count.value}b', self.legal_moves_c.raw[:self.move_count.value])
        self.draw_board()
        self.draw_moves_on_board()
        self.draw_pieces_on_position()
        
        
    def draw_moves_on_board(self):
        for ind in range(self.move_count.value//5):
            if (self.moves_list[ind*5+2] + self.moves_list[ind*5+3]) % 2 == 1:
                self.rectangles[(self.moves_list[ind*5+2],self.moves_list[ind*5+3])].configure(bg=DARKRED)
            else:
                self.rectangles[(self.moves_list[ind*5+2],self.moves_list[ind*5+3])].configure(bg=LIGHTRED)
            

    def make_move(self, move): #not done
        chess_lib.make_move(ctypes.byref(self.chess_board_instance), ctypes.c_byte(move[0]),ctypes.c_byte(move[1]), ctypes.c_byte(move[2]),ctypes.c_byte(move[3]), -1)
        chess_lib.find_all_moves(ctypes.byref(self.chess_board_instance),self.legal_moves_c, ctypes.byref(self.move_count))
        self.moves_list = struct.unpack(f'{self.move_count.value}b', self.legal_moves_c.raw[:self.move_count.value])
        
        self.reset_color()
        self.draw_moves_on_board()
        self.draw_pieces_on_position()

    def draw_board(self):
        
        cell_size = self.min_canvas_size / self.chess_board_instance.size 

        self.canvas = ctk.CTkCanvas(master=self.board_frame, width=self.min_canvas_size, height=self.min_canvas_size)
        self.canvas.pack(expand=True)
        self.board_cell_size = cell_size
        self.rectangles = {}


        for i in range(self.chess_board_instance.size):
            for j in range(self.chess_board_instance.size):
                x1 = i*cell_size
                y1 = j*cell_size 
                canvas_obj = ctk.CTkCanvas(self.canvas,width=cell_size,height=cell_size)
                self.rectangles[(i, j)] = canvas_obj
                canvas_obj.place(x=x1, y=y1)
                if (j + i) % 2 == 1:
                    self.rectangles[(i,j)].configure(bg=BLACK)
                else:
                    self.rectangles[(i,j)].configure(bg=WHITE)
                self.rectangles[(i,j)].bind("<Button-1>", lambda event, pos=(i,j): self.on_piece_click(pos))
                self.rectangles[(i,j)].bind("<Button-3>", lambda event, pos=(i,j): self.unfocus_piece())

    def draw_pieces_on_position(self):
        if hasattr(self, "piece_images"):
            for key in self.piece_images:
                self.piece_images[key].destroy()

        
        self.piece_images = {}
        self.piece_clicked = False

        for color in range(0,2):
                for ind in range(self.chess_board_instance.piece_count):
                    if (color == 0 and self.chess_board_instance.white_piece_alive[ind]) or (color == 1 and self.chess_board_instance.black_piece_alive[ind]):
                        ind_pos = ind*2
                        if color == 0:
                            path = WHITE_PIECES_PATH + str(self.chess_board_instance.white_piece_img[ind]) +".png"
                            pos = self.chess_board_instance.white_piece_pos[ind_pos] ,self.chess_board_instance.white_piece_pos[ind_pos+1]
                        else: 
                            path = BLACK_PIECES_PATH + str(self.chess_board_instance.black_piece_img[ind]) +".png"
                            pos = self.chess_board_instance.black_piece_pos[ind_pos] ,self.chess_board_instance.black_piece_pos[ind_pos+1]
                        rect_of_position = self.rectangles[pos[0],pos[1]]
                        label_width = 0.48 * self.rectangles[(0,0)].winfo_reqwidth()
                        img = ctk.CTkImage(light_image=Image.open((path)).convert("RGBA"),
                                            dark_image=Image.open((path)).convert("RGBA"),
                                            size=(label_width, label_width))
                        label = ctk.CTkLabel(rect_of_position, text="", image=img)
                        label.bind("<Button-1>", lambda event, pos=pos: self.on_piece_click(pos))
                        label.bind("<Button-3>", lambda event, pos=pos: self.unfocus_piece())
                        label.place(relx=0.5, rely=0.5, anchor="center")
                        self.piece_images[pos] = label

    def on_piece_click(self, pos):
        if self.first_click == (-1,-1):
            self.first_click = pos
        else:
            self.second_click = pos
            print(self.is_move())
            print(self.first_click, self.second_click)
            if self.is_move() == 1:
                self.make_move([self.first_click[0],self.first_click[1],self.second_click[0], self.second_click[1],1])
                print("hey")
            elif self.is_move() > 1: 
                self.make_move([self.first_click[0],self.first_click[1],self.second_click[0], self.second_click[1],1]) # HIER MUSS STATT DER 1 ein engabefeld hin
                print("hey")
            self.first_click = (-1,-1)
            self.second_click = (-1,-1)
                

    def is_move(self):
        move_count = 0
        for ind in range(self.move_count.value//5):
            if self.moves_list[ind*5] == self.first_click[0] and self.moves_list[ind*5+1] == self.first_click[1] and self.moves_list[ind*5+2] == self.second_click[0] and self.moves_list[ind*5+3] == self.second_click[1]:
                move_count += 1
        return move_count
        

    def reset_color(self):
        for key in self.rectangles:
            if sum(key) % 2 == 1:
                self.rectangles[key].configure(bg=BLACK)
            else:
                self.rectangles[key].configure(bg=WHITE)

    
    def is_black_field(self,position):
        if (position[0]+ position[1]) % 2 == 1:
            return True
        return False
    
    def destroy(self):
        return self.main_frame.destroy()
    


def thread_engine(args):
    move_count = [-1]
    test_engine(args[0], args[1], move_count)
    return move_count

def thread_testing(args):
    play_game_test(args[0],args[1],args[2])