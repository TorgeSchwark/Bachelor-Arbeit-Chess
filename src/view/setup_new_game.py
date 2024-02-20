import customtkinter as ctk
import os
from tkinter import *
from PIL import Image, ImageTk
from view.view_variables import *
from chess_implementation.piece import Piece
from chess_implementation.chess_board import ChessBoard
from model.main_model import Model
import copy
import numpy as np
import pickle
import re


class SetupNewGame():

    #Setup main settings(main elements) 
    def __init__(self, master, controller):
        
        self.chess_board_obj = ChessBoard()

        self.board_size = 0
        self.image_labels = {}
        self.image_clicked = False
        self.controller = controller
        self.model = Model()
        self.master = master
        self.frame = ctk.CTkFrame(master=master, border_width=2)
        self.frame.pack_propagate(False)
        self.frame.pack(expand=True, fill="both")

        self.options = ctk.CTkFrame(master=self.frame, border_width=2)
        self.options.pack(side="left", expand=True, fill="both")
        self.options.pack_propagate(False)

        self.options2 = ctk.CTkFrame(master=self.frame, border_width=2)
        self.options2.pack(side="left", expand=True, fill="both")
        self.options2.pack_propagate(False)

        self.board = ctk.CTkFrame(master=self.frame, border_width=2)
        self.board.pack(side="left", expand=True, fill="both")

        self.label_options = ctk.CTkLabel(master=self.options, text="Options", font=('Arial',20))
        self.label_options.pack(expand=False, pady=10)

        self.label_board_size = ctk.CTkLabel(master=self.options, text="Board size")
        self.label_board_size.pack(expand=False, pady=5)

        self.slider = ctk.CTkSlider(master=self.options, from_=4, to=20, number_of_steps=16, command=self.draw_board, width=200)
        self.slider.pack(expand=False, padx=20, pady=5)

        self.add_piece_button = ctk.CTkButton(master=self.options, text="Add piece", command=self.load_images)
        self.add_piece_button.pack(expand=False, padx=20, pady=5)
        
        self.game_name = ctk.StringVar(value="")
        self.game_name_entry = ctk.CTkEntry(self.options, placeholder_text="Enter a name for your game", textvariable=self.game_name)
        self.game_name_entry.pack(expand=False, padx=20, pady=5)

        self.show_board_button = ctk.CTkButton(master=self.options, text="Show current board", command=self.show_current_board)
        self.show_board_button.pack(expand=False, padx=20, pady=5)

        self.save_game_button = ctk.CTkButton(master=self.options, text="Save game", command=self.save_game)
        self.save_game_button.pack(expand=False, padx=20, pady=5)

        self.main_menu_button = ctk.CTkButton(master=self.options, text="Back to Menu", command=self.main_menu)
        self.main_menu_button.pack(expand=False, padx=20, pady=5)

    #call the DB to save the Game
    def save_game(self):
        if (self.model.save_game(self.chess_board_obj, self.game_name.get())):
            print("Saved Game successful")
            self.main_menu()
        else:
            self.game_name = "Save wasnt successful"
    
    #go back to main menu
    def main_menu(self):
        from view.starting_page import MainMenu
        self.frame.destroy()
        MainMenu(self.master, self.controller)
    
    #shows how the current configuration would look like
    def show_current_board(self):

        if self.slider.cget("state") == "disabled":

            children = self.options2.winfo_children()
            for child in children:
                child.destroy()
            
            self.draw_normal_board(self.board_size//2)
            #show all white pieces
            for ind in range(len(self.chess_board_obj.white_pieces)):
                path = WHITE_PIECES_PATH+ self.chess_board_obj.white_pieces[ind].img_name
                pos = self.chess_board_obj.white_pieces_pos[ind*2],self.chess_board_obj.white_pieces_pos[ind*2+1]
                position = self.rectangles[pos]
                label_width = 0.48 * self.rectangles[(0,0)].winfo_reqwidth()
                img = ctk.CTkImage(light_image=Image.open((path)).convert("RGBA"),
                                dark_image=Image.open((path)).convert("RGBA"),
                                size=(label_width, label_width))
                label = ctk.CTkLabel(position, text="", image=img)
                label.place(relx=0.5, rely=0.5, anchor="center")
            #show all black pieces
            for ind in range(len(self.chess_board_obj.black_pieces)):
                path = BLACK_PIECES_PATH+ self.chess_board_obj.black_pieces[ind].img_name
                pos = self.chess_board_obj.black_pieces_pos[ind*2],self.chess_board_obj.black_pieces_pos[ind*2+1]
                position = self.rectangles[pos]
                label_width = 0.48 * self.rectangles[(0,0)].winfo_reqwidth()
                img = ctk.CTkImage(light_image=Image.open((path)).convert("RGBA"),
                                dark_image=Image.open((path)).convert("RGBA"),
                                size=(label_width, label_width))
                label = ctk.CTkLabel(position, text="", image=img)
                label.place(relx=0.5, rely=0.5, anchor="center")

        else:
            raise Exception("please configure one Piece first")

    #loads images to chose from for the pieces
    def load_images(self):
        self.draw_board(self.slider.get())

        if hasattr(self, "image_frame"):
            children = self.options2.winfo_children()
            for child in children:
                child.destroy()

        self.image_frame = 0

        folder_path = "src/view/images/Chess_pieces/White_pieces/"
        num_columns = 4
        row = 0
        col = 0
            
        self.image_frame = ctk.CTkScrollableFrame(self.options2, border_width=2)
        self.image_frame.pack(expand=True, padx=20)

        for file in os.listdir(folder_path):
            img = ctk.CTkImage(light_image=Image.open((folder_path + file)).convert("RGBA"),
                                dark_image=Image.open((folder_path + file)).convert("RGBA"),
                                size=(30, 30))

            my_label = ctk.CTkLabel(self.image_frame, text="", image=img)
            my_label.grid(row=row, column=col, padx=5, pady=5)

            self.image_labels[file] = my_label

            my_label.bind("<Button-1>", lambda event, image_path=(folder_path + file): self.on_image_click(event, image_path))

            col += 1
            if col == num_columns:
                col = 0
                row += 1

    #adds the options for the pieces(Pawn, King, ...)
    def add_piece_options(self):

        if hasattr(self, "piece_options_frame"):
            self.piece_options_frame.destroy()

        self.piece_options_frame = ctk.CTkFrame(self.options2,border_width=2)
        self.piece_options_frame.pack(expand=True)

        self.king_var = ctk.StringVar(value="off")
        self.king_switch = ctk.CTkSwitch(self.piece_options_frame, text="King", command=self.king_switches,
                                variable=self.king_var , onvalue="on", offvalue="off")

        self.pawn_var = ctk.StringVar(value="off")
        self.pawn_switch = ctk.CTkSwitch(self.piece_options_frame, text="Pawn", command=self.pawn_switches,
                                variable=self.pawn_var , onvalue="on", offvalue="off")

        self.castling_var = ctk.StringVar(value="off")
        self.castling_switch = ctk.CTkSwitch(self.piece_options_frame, text="Rochade",command=self.castling_switches,
                                variable=self.castling_var , onvalue="on", offvalue="off")
        
        self.boarderx_var = ctk.StringVar(value="off")
        self.boarderx_switch = ctk.CTkSwitch(self.piece_options_frame, text="Walk over x boarder",command=self.boarder_switches,
                                variable=self.boarderx_var , onvalue="on", offvalue="off")

        self.boardery_var = ctk.StringVar(value="off")
        self.boardery_switch = ctk.CTkSwitch(self.piece_options_frame, text="Walk over y boarder",command=self.boarder_switches,
                                variable=self.boardery_var , onvalue="on", offvalue="off")
        
        self.save_piece_button = ctk.CTkButton(self.piece_options_frame, text="SAVE piece", command=self.save_piece, fg_color=RED, hover_color=DARKRED)

        self.king_switch.pack(expand=False, padx=20,pady=10)
        self.pawn_switch.pack(expand=False, padx=20,pady=10)
        self.castling_switch.pack(expand=False, padx=20,pady=10)
        self.boarderx_switch.pack(expand=False, padx=20,pady=10)
        self.boardery_switch.pack(expand=False, padx=20,pady=10)
        self.save_piece_button.pack(expand=True, padx=20, pady=5)
        self.save_piece_button.pack_propagate(False)

    #searches the board to detect the settings for the piece by looking for rect colors
    def save_piece(self):
        if len(self.piece_start_pos) > 0:
            self.piece_start_pos = []
            piece = Piece()
            piece.set_boarder_x(self.boarderx_var.get() == "on")
            piece.set_boarder_y = (self.boardery_var.get() == "on")
            piece.set_king(self.king_var.get() == "on")
            piece.set_pawn(self.pawn_var.get() == "on")
            piece.set_castling(self.castling_switch.get() == "on")
            piece.set_image_path(self.piece_image_path)
            
            directions = {}
            for x in range(self.board_size):
                for y in range(self.board_size):
                    y_vec = (y-self.piece_row)
                    x_vec = (x-self.piece_col)
                    if self.piece_col-x != 0:
                        direction_x = x_vec / abs(x_vec)
                    else: 
                        direction_x = 0
                    if self.piece_row-y != 0:
                        direction_y = (y_vec) / abs(y_vec) #TODO: Division by zero problem
                    else:
                        direction_y = 0

                    if self.rectangles[(x,y)].cget("bg") == LIGHTGREEN or self.rectangles[(x,y)].cget("bg") == DARKGREEN:
                        piece.add_jump_move((x_vec,y_vec))
                    if self.rectangles[(x,y)].cget("bg") == DARKRED or self.rectangles[(x,y)].cget("bg") == LIGHTRED:
                        piece.add_direction((direction_x,direction_y,0)) #only once
                    if self.rectangles[(x,y)].cget("highlightbackground") == LIGHTYELLOW or self.rectangles[(x,y)].cget("highlightbackground") == DARKYELLOW:
                        self.piece_start_pos += [[x,y]]
                        print("hier")
                    if self.rectangles[(x,y)].cget("bg") == DARKBLUE or self.rectangles[(x,y)].cget("bg") == LIGHTBLUE:
                        if direction_y != 0:
                            if (direction_x,direction_y) in directions:
                                directions[(direction_x,direction_y)] = max(abs(y_vec),directions[(direction_x,direction_y)])
                            else: 
                                directions[(direction_x,direction_y)] = abs(y_vec)
                        else:
                            if (direction_x,direction_y) in directions:
                                directions[(direction_x,direction_y)] = max(abs(x_vec),directions[(direction_x,direction_y)])
                            else: 
                                directions[(direction_x,direction_y)] = abs(x_vec)
                        

            for key in directions:
                piece.add_direction((key[0],key[1],directions[key]))

            if self.slider.cget("state") == "normal":
                self.slider.configure(state="disabled") #board size cant be switched now
                self.chess_board_obj.set_size(self.board_size//2)

            self.chess_board_obj.add_piece(piece,self.real_board_x_min, start_pos = self.piece_start_pos ) #pos muss umgerechnet werden
            
            self.chess_board_obj.show_board()

            self.update_board_colors()
            self.piece_lable.destroy()
            if self.piece_image_path in self.image_labels:
                self.image_labels[self.piece_image_path].destroy()

            self.piece_start_pos = []
            self.piece_image_path = ""
            self.piece_lable = None
      
        else:
            print("piece needs start pos")
    
    #ensures that only valid options can be made
    def king_switches(self):
        self.castling_var.set("on")
        self.pawn_var.set("off")
        self.boarderx_var.set("off")
        self.boardery_var.set("off")

    def pawn_switches(self):
        self.castling_var.set("off")
        self.king_var.set("off")
        self.boarderx_var.set("off")
        self.boardery_var.set("off")

    def castling_switches(self):
        self.pawn_var.set("off")
        self.boarderx_var.set("off")
        self.boardery_var.set("off")

    def boarder_switches(self):
        self.pawn_var.set("off")
        self.king_var.set("off")
        self.castling_var.set("off")

    #if a picture is chosen for the piece loads image in the center
    def on_image_click(self, event, image_path):

        self.update_board_colors()  # hier muss auf das rendern gewartet werden!
        self.piece_start_pos = []

        self.image_clicked = True

        row = self.board_size // 2 
        col = self.board_size // 2 

        self.piece_row = row
        self.piece_col = col

        position = self.rectangles[(row, col)]
        label_width = 0.48 * position.winfo_width()

        img = ctk.CTkImage(light_image=Image.open((image_path)).convert("RGBA"),
                            dark_image=Image.open((image_path)).convert("RGBA"),
                            size=(label_width, label_width))

        label = ctk.CTkLabel(position, text="", image=img)
        label.place(relx=0.5, rely=0.5, anchor="center")

        self.piece_lable = label
        self.piece_image_path = os.path.basename(image_path)

        self.add_piece_options()

    #sets board colors back to default
    def update_board_colors(self):
        self.image_clicked = False
        for position, canvas_obj in self.rectangles.items():
            i, j = position
            self.change_to_normal_color(i,j)
        
        for pos in range(len(self.chess_board_obj.white_pieces_pos)//2):
                self.rectangles[(self.chess_board_obj.white_pieces_pos[pos*2]+self.real_board_x_min,self.chess_board_obj.white_pieces_pos[pos*2+1]+self.real_board_y_min)].configure(highlightthickness=self.board_cell_size//4, highlightbackground=REAL_BLACK)
        for pos in range(len(self.chess_board_obj.black_pieces_pos)//2):
            self.rectangles[(self.chess_board_obj.black_pieces_pos[pos*2]+self.real_board_x_min,self.chess_board_obj.black_pieces_pos[pos*2+1]+self.real_board_y_min)].configure(highlightthickness=self.board_cell_size//4, highlightbackground=REAL_BLACK)

    #changes one field back to original color
    def change_to_normal_color(self, x, y):
        value = self.board_value
        # of a rect has a black thickness it should stay since this is not optional and should stop one of chosing taken positions as starting position
        if self.rectangles[(x,y)].cget("highlightbackground") != REAL_BLACK:
            self.rectangles[(x,y)].configure(highlightthickness=1, highlightbackground="White")
        if (x + y) % 2 == 1:
            if (x < int(value)//2) or y < int(value)//2 or x >= int(value)//2+int(value) or y >= int(value)//2+int(value):
                self.rectangles[(x,y)].configure(bg=DARKGREY)
            else:
                self.rectangles[(x,y)].configure(bg=BLACK)
        else:
            if (x < int(value)//2) or y < int(value)//2 or x >= int(value)//2+int(value) or y >= int(value)//2+int(value):
                self.rectangles[(x,y)].configure(bg=LIGHTGREY)
            else:
                self.rectangles[(x,y)].configure(bg=WHITE)

    #detect choices made (controlled by rect colors not by states) left klicks
    def field_clicked(self, x, y): 

        if self.piece_col-x != 0:
            direction_x = (x-self.piece_col) / abs(self.piece_col-x)
        else: 
            direction_x = 0
        if self.piece_row-y != 0:
            direction_y = (y-self.piece_row) / abs(self.piece_row-y) #TODO: Division by zero problem
        else:
            direction_y = 0
        
        if self.image_clicked and not (x == self.piece_col and y == self.piece_row):
            color = self.rectangles[(x, y)].cget("bg")
            if color == WHITE or color == LIGHTGREY:
                self.rectangles[(x, y)].configure(bg=LIGHTGREEN)
            elif color == BLACK or color == DARKGREY:
                self.rectangles[(x, y)].configure(bg=DARKGREEN)

            elif color == LIGHTGREEN:
                if self.correct_direction(x,y):
                    self.rectangles[(x, y)].configure(bg=LIGHTBLUE)
                else:
                    self.change_to_normal_color(x,y)
            elif color == DARKGREEN:
                if self.correct_direction(x,y):
                    self.rectangles[(x, y)].configure(bg=DARKBLUE)
                else:
                    self.change_to_normal_color(x,y)

            elif color == LIGHTBLUE and self.is_next_to_piece(x,y):
                self.draw_direction(x,y, True)
            elif color == LIGHTBLUE and not self.is_next_to_piece(x,y):
                self.draw_direction(x,y, False)

            elif color == DARKBLUE and self.is_next_to_piece(x,y):
                self.draw_direction(x,y, True)
            elif color == DARKBLUE and not self.is_next_to_piece(x,y):
                self.draw_direction(x,y, False)

            elif color == DARKRED and self.is_next_to_piece(x,y):
                self.draw_direction(x, y, False)
            elif color == LIGHTRED and self.is_next_to_piece(x,y):
                self.draw_direction(x, y, False)

    #detect choices made (controlled by rect colors not by states) right klicks
    def field_clicked_r(self, x, y):
        color = self.rectangles[(x, y)].cget("bg")
        bg_color = self.rectangles[(x, y)].cget("highlightbackground")
        if y < (self.board_size//2) and self.image_clicked and y >= self.real_board_y_min and x >= self.real_board_x_min and x < self.real_board_x_max:
            if (x + y) % 2 == 1:
                if (color == BLACK or color == DARKRED or color == DARKBLUE or color == DARKGREEN) and bg_color != REAL_BLACK:
                    self.piece_start_pos += [[x,y]]
                    self.rectangles[(x,y)].configure(highlightthickness=self.board_cell_size//4, highlightbackground=DARKYELLOW)
                if bg_color == DARKYELLOW:
                    self.rectangles[(x,y)].configure(highlightthickness=1, highlightbackground="White")
                    self.piece_start_pos.remove([x,y])
            else:
                if (color == WHITE or color == LIGHTRED or color == LIGHTBLUE or color == LIGHTGREEN )and bg_color != REAL_BLACK:           
                    self.piece_start_pos += [[x,y]]
                    self.rectangles[(x,y)].configure(highlightthickness=self.board_cell_size//4, highlightbackground=LIGHTYELLOW)
                if bg_color == LIGHTYELLOW:
                    self.rectangles[(x,y)].configure(highlightthickness=1, highlightbackground="White")
                    self.piece_start_pos.remove([x,y])

    #checks if a field is next to the piece    
    def is_next_to_piece(self,x,y):
        return (abs(self.piece_col-x) == 1 and abs(self.piece_row-y)) == 1 or (abs(self.piece_row-y) == 0 and abs(self.piece_col-x)) == 1 or (abs(self.piece_row-y) == 1 and abs(self.piece_col-x) == 0)

    #makes sure walking directions stay connected
    def correct_direction(self,x,y):
        if self.piece_col-x != 0:
            direction_x = (self.piece_col-x) / abs(self.piece_col-x)
        else: 
            direction_x = 0
        if self.piece_row-y != 0:
            direction_y = (self.piece_row-y) / abs(self.piece_row-y) #TODO: Division by zero problem
        else:
            direction_y = 0

        if (abs(self.piece_col-x) == 1 and abs(self.piece_row-y)) == 1 or (abs(self.piece_row-y) == 0 and abs(self.piece_col-x)) == 1 or (abs(self.piece_row-y) == 1 and abs(self.piece_col-x) == 0): #next to the piece
            return True
        elif (abs(self.piece_col-x) == abs(self.piece_row-y) and abs(self.piece_col-x) != 0 ) or  (self.piece_row-y == 0 and self.piece_col-x != 0) or (self.piece_col-x == 0 and self.piece_row-y): # straight or diag move others are no directions
            if self.rectangles[(x+direction_x,y+direction_y)].cget("bg") == LIGHTBLUE or self.rectangles[(x+direction_x,y+direction_y)].cget("bg") == DARKBLUE:  # field in direction of the pice is added as well
                print((x+direction_x,y+direction_y), x,y ,self.piece_row-x, self.piece_col-y)
                return True 
        else:
            return False

    #changes colors to red for one direction
    def draw_direction(self,x,y, set): 
        if self.piece_col-x != 0:
            direction_x = (x-self.piece_col) / abs(self.piece_col-x)
        else: 
            direction_x = 0
        if self.piece_row-y != 0:
            direction_y = (y-self.piece_row) / abs(self.piece_row-y) #TODO: Division by zero problem
        else:
            direction_y = 0
        if set:
            while x >= self.real_board_x_min and x < self.real_board_y_max and y >= self.real_board_y_min and y < self.real_board_y_max:
                if (x + y) % 2 == 1:
                    self.rectangles[(x,y)].configure(bg=DARKRED)
                else:
                    self.rectangles[(x,y)].configure(bg=LIGHTRED)
                x += direction_x
                y += direction_y
        else:
            while x >= 0 and x < self.board_size and y >= 0 and y < self.board_size:
                self.change_to_normal_color(x,y)
                x += direction_x
                y += direction_y

    #draws the initial board with a frame to chose further jump moves
    def draw_board(self, value):
        if int(value) != self.board_size:
            self.image_clicked = False
            self.board_size = int(value) * 2 - (int(value) %2 == 1)
            self.board_value = value
            self.real_board_x_min = int(value)//2
            self.real_board_x_max = int(value)//2+int(value)
            self.real_board_y_min = int(value)//2
            self.real_board_y_max = int(value)//2+int(value)

            if hasattr(self, "canvas"):
                self.canvas.destroy()
 
            min_canvas_size = self.board.winfo_height() - 100  

            self.canvas = ctk.CTkCanvas(master=self.board, width=min_canvas_size, height=min_canvas_size)
            self.canvas.pack(expand=True)

            cell_size = min_canvas_size / self.board_size
            self.board_cell_size = cell_size

            self.rectangles = {}

            for i in range(self.board_size):
                for j in range(self.board_size):
                    x1 = i * cell_size
                    y1 = j * cell_size
                    canvas_obj = ctk.CTkCanvas(self.canvas, width=cell_size, height=cell_size)
        
                    canvas_obj.bind("<Button-1>", lambda event, x=i, y=j: self.field_clicked(x, y))
                    canvas_obj.bind("<Button-3>", lambda event, x=i, y=j: self.field_clicked_r(x, y))
                    self.rectangles[(i, j)] = canvas_obj
                    canvas_obj.place(x=x1, y=y1)

                    self.change_to_normal_color(i, j)
        
            for pos in range(len(self.chess_board_obj.white_pieces_pos)//2):
                self.rectangles[(self.chess_board_obj.white_pieces_pos[pos*2]+self.real_board_x_min,self.chess_board_obj.white_pieces_pos[pos*2+1]+self.real_board_y_min)].configure(highlightthickness=self.board_cell_size//4, highlightbackground=REAL_BLACK)
            for pos in range(len(self.chess_board_obj.black_pieces_pos)//2):
                self.rectangles[(self.chess_board_obj.black_pieces_pos[pos*2]+self.real_board_x_min,self.chess_board_obj.black_pieces_pos[pos*2+1]+self.real_board_y_min)].configure(highlightthickness=self.board_cell_size//4, highlightbackground=REAL_BLACK)
                  
    #draws the normal board no frame              
    def draw_normal_board(self, size): 
        if hasattr(self, "canvas"):
            self.canvas.destroy()

        min_canvas_size = self.board.winfo_height() - 100  
        cell_size = min_canvas_size / size

        self.canvas = ctk.CTkCanvas(master=self.board, width=min_canvas_size, height=min_canvas_size)
        self.canvas.pack(expand=True)
        self.board_cell_size = cell_size
        self.rectangles = {}

        for i in range(size):
            for j in range(size):
                x1 = i*cell_size
                y1 = j*cell_size 
                canvas_obj = ctk.CTkCanvas(self.canvas,width=cell_size,height=cell_size)
                self.rectangles[(i, j)] = canvas_obj
                canvas_obj.place(x=x1, y=y1)
                if (j + i) % 2 == 1:
                    self.rectangles[(i,j)].configure(bg=BLACK)
                else:
                    self.rectangles[(i,j)].configure(bg=WHITE)

