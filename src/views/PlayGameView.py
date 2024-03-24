from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece_rules import PieceRules
from chess_implementation.piece import Piece
from chess_implementation.chess_variables import *
from chess_implementation.find_moves import find_all_moves
from chess_implementation.make_moves import make_move, undo_last_move
from chess_implementation.move_stack import MoveStack
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

class PlayGameView(View):
    
    def __init__(self, master, controller):
        
        self.controller = controller
        self.position = (0,0)
        self.master = master
        self.moves = MoveStack()
        
        self.chess_board_instance: ChessBoard = controller.board_instance

        self.chess_board_instance.show_board()

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

        self.board_make_random_move_button = ctk.CTkButton(master=self.settings_frame, text="make a move", command=self.make_random_move)
        self.board_make_random_move_button.pack(expand=False, padx=20, pady=5)

        self.board_castling_switch_var = ctk.StringVar(value="off")
        self.board_castling_switch = ctk.CTkSwitch(master=self.settings_frame, text="castling", variable=self.board_castling_switch_var, onvalue="on", offvalue="off")
        self.board_castling_switch.pack(expand=False, padx=20,pady=10)

        self.undo_move_button = ctk.CTkButton(master=self.settings_frame, text="Undo move", command= self.call_undo_last_move)
        self.undo_move_button.pack(expand=False, padx=20, pady=5)

        self.engine_button = ctk.CTkButton(master=self.settings_frame, text="Chess engine", command= self.call_engine)
        self.engine_button.pack(expand=False, padx=20, pady=5)


        self.draw_board()
        self.draw_pieces_on_position()


    #aply longer test
    def call_engine(self):

        num_processes = 3 #20
        depth = 2 #3
        lenght = 10 #200
        pool = Pool(num_processes)

        args_list = [(deepcopy(self.chess_board_instance), depth, lenght) for _ in range(num_processes)]
        pool.map(thread_testing, args_list)
        
        pool.close()


    def call_undo_last_move(self):
        undo_last_move(self.chess_board_instance)
        self.reset_color()
        self.draw_moves()
        self.draw_pieces_on_position()
        self.chess_board_instance.show_board()

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
                canvas_obj.bind("<Button-3>", lambda event, pos=(i,j): self.unfocus_piece())
                canvas_obj.bind("<Button-1>", lambda event, pos=(i,j): self.field_click(pos))

    def draw_pieces_on_position(self):
        if hasattr(self, "piece_images"):
            for key in self.piece_images:
                self.piece_images[key].destroy()

        
        self.piece_images = {}
        self.piece_clicked = False

        for color in range(0,2):
            for ind in range(len(self.chess_board_instance.white_pieces)):
                if color == 0:
                    piece: Piece = self.chess_board_instance.white_pieces[ind]
                    path = WHITE_PIECES_PATH + piece.rules.img_name
                    pos = piece.position[0], piece.position[1]
                else:
                    piece: Piece = self.chess_board_instance.black_pieces[ind]
                    path = BLACK_PIECES_PATH + piece.rules.img_name
                    pos = piece.position[0], piece.position[1]
                if piece.is_alive:
                    rect_of_position = self.rectangles[pos]
                    label_width = 0.48 * self.rectangles[(0,0)].winfo_reqwidth()
                    img = ctk.CTkImage(light_image=Image.open((path)).convert("RGBA"),
                                    dark_image=Image.open((path)).convert("RGBA"),
                                    size=(label_width, label_width))
                    label = ctk.CTkLabel(rect_of_position, text="", image=img)
                    label.bind("<Button-1>", lambda event, pos=pos: self.on_piece_click(pos))
                    label.bind("<Button-3>", lambda event, pos=pos: self.unfocus_piece())
                    label.place(relx=0.5, rely=0.5, anchor="center")
                    self.piece_images[pos] = label

        self.draw_moves()
    
    def make_random_move(self):
        move_ind = random.randint(0, self.moves.head//5)
        make_move(self.chess_board_instance, self.moves.stack[move_ind*5],self.moves.stack[move_ind*5+1], self.moves.stack[move_ind*5+2], self.moves.stack[move_ind*5+3], self.moves.stack[move_ind*5+4])
        self.reset_color()
        self.draw_moves()
        self.draw_pieces_on_position()
        self.chess_board_instance.show_board()

    def draw_moves(self):
        moves: MoveStack = find_all_moves(self.chess_board_instance)
        self.moves = moves
        moves.show()

        for ind in range(moves.head):
            to_x = moves.stack[ind*5+2]
            to_y = moves.stack[ind*5+3]
            if (to_x+to_y) % 2 == 1:
                self.rectangles[(to_x,to_y)].configure(bg=DARKBLUE)
            else:
                self.rectangles[(to_x,to_y)].configure(bg=LIGHTBLUE)

    def reset_color(self):
        for key in self.rectangles:
            if sum(key) % 2 == 1:
                self.rectangles[key].configure(bg=BLACK)
            else:
                self.rectangles[key].configure(bg=WHITE)

    #castling needs to be implemented
    def on_piece_click(self, position):
        if not self.piece_clicked:
            self.piece_clicked = position
            if self.is_black_field(position):
                self.piece_images[position].configure(fg_color = DARKGREEN)
            else: 
                self.piece_images[position].configure(fg_color = LIGHTGREEN)
        else:
            move = self.is_move(self.piece_clicked[0], self.piece_clicked[1], position[0], position[1])

            if move:
                make_move(self.chess_board_instance, *move)
                self.reset_color()
                self.draw_moves()
                self.draw_pieces_on_position()
                self.chess_board_instance.show_board()
            else:
                self.unfocus_piece()
            
    
    def field_click(self, position):
        if self.piece_clicked:
            move = self.is_move(self.piece_clicked[0], self.piece_clicked[1], position[0], position[1])
        else: 
            move = False
        if move:
            make_move(self.chess_board_instance, *move)
            self.reset_color()
            self.draw_moves()
            self.draw_pieces_on_position()
            self.chess_board_instance.show_board()
        else:
            self.unfocus_piece()


    def is_move(self, from_x, from_y, to_x, to_y):
        if self.board_castling_switch_var.get() == "on":
            print("yes")
            castling = True
        else:
            castling = False

        for ind in range(self.moves.head):
            if self.moves.stack[ind*5] == from_x and self.moves.stack[ind*5+1] == from_y and self.moves.stack[ind*5+2] == to_x and self.moves.stack[ind*5+3] == to_y and ((not castling and  self.moves.stack[ind*5+4] != CASTLING) or (castling and self.moves.stack[ind*5+4] == CASTLING)):
                return (self.moves.stack[ind*5],self.moves.stack[ind*5+1],self.moves.stack[ind*5+2], self.moves.stack[ind*5+3], self.moves.stack[ind*5+4])
        return False

    def unfocus_piece(self):
        if self.is_black_field(self.piece_clicked):
            self.piece_images[self.piece_clicked].configure(fg_color = BLACK)
        else: 
            self.piece_images[self.piece_clicked].configure(fg_color = WHITE)
        self.piece_clicked = False
    


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