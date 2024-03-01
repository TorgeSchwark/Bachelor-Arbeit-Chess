from chess_implementation.chess_board import ChessBoard
from chess_implementation.piece_rules import PieceRules
from chess_implementation.piece import Piece
from chess_implementation.find_moves import find_all_moves
from chess_implementation.move_stack import MoveStack
from views.View import View
import customtkinter as ctk
from views.view_variables import *
from PIL import Image

class PlayGameView(View):
    
    def __init__(self, master, controller):
        
        self.controller = controller
        self.master = master
        
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

        self.draw_board()
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

    def draw_pieces_on_position(self):
        if hasattr(self, "piece_labels"):
            for piece_label in self.pice_labels:
                piece_label.destroy()
        
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
                rect_of_position = self.rectangles[pos]
                label_width = 0.48 * self.rectangles[(0,0)].winfo_reqwidth()
                img = ctk.CTkImage(light_image=Image.open((path)).convert("RGBA"),
                                dark_image=Image.open((path)).convert("RGBA"),
                                size=(label_width, label_width))
                label = ctk.CTkLabel(rect_of_position, text="", image=img)
                label.bind("<Button-1>", lambda event, pos=pos: self.on_piece_click(pos))
                label.bind("<Button-3>", lambda event, pos=pos: self.defocus_piece(pos))
                label.place(relx=0.5, rely=0.5, anchor="center")
                self.piece_images[pos] = label

        self.draw_moves()
    
    def draw_moves(self):
        moves: MoveStack = find_all_moves(self.chess_board_instance)
        print(moves.stack)

        for ind in range(moves.head):
            to_x = moves.stack[ind*5+2]
            to_y = moves.stack[ind*5+3]
            if (to_x+to_y) % 2 == 1:
                self.rectangles[(to_x,to_y)].configure(bg=DARKBLUE)
            else:
                self.rectangles[(to_x,to_y)].configure(bg=LIGHTBLUE)


    def on_piece_click(self, position):
        if not self.piece_clicked:
            self.piece_clicked = position
            if self.is_black_field(position):
                self.piece_images[position].configure(fg_color = DARKGREEN)
            else: 
                self.piece_images[position].configure(fg_color = LIGHTGREEN)
        else:
            pass

            # self.piece_clicked = [-1,-1] nichts geklicked
            # wenn irgendwo linksklick -> [-1,-1]
            # wenn rechts klick und figur -> [posx, posy]
            # wenn rechts klick und feld in legal_moves der figur -> mache zug 

    def defocus_piece(self, position):
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