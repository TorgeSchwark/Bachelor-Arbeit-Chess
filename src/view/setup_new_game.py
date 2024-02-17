import customtkinter as ctk
import os
from tkinter import *
from PIL import Image, ImageTk
from view.view_variables import *
from chess_implementation.piece import Piece
from chess_implementation.chess_board import ChessBoard

class SetupNewGame():

    def __init__(self, master, controller):
        
        self.chess_board_obj = ChessBoard()

        self.board_size = 0
        self.image_labels = []
        self.image_clicked = False
        self.controller = controller
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

        self.add_figure_button = ctk.CTkButton(master=self.options, text="Add figure", command=self.load_images)
        self.add_figure_button.pack(expand=False, padx=20, pady=5)
            
    def load_images(self):
        if not hasattr(self, "image_frame"):
            folder_path = "src/view/images/Chess_pieces/"
            num_columns = 4
            row = 0
            col = 0
            
            # Erstelle den Frame für die Bilder
            self.image_frame = ctk.CTkScrollableFrame(self.options2, border_width=2)
            self.image_frame.pack(expand=True, padx=20)

            for file in os.listdir(folder_path):
                img = ctk.CTkImage(light_image=Image.open((folder_path + file)).convert("RGBA"),
                                dark_image=Image.open((folder_path + file)).convert("RGBA"),
                                size=(30, 30))

                my_label = ctk.CTkLabel(self.image_frame, text="", image=img)
                my_label.grid(row=row, column=col, padx=5, pady=5)

                self.image_labels.append(my_label)

                my_label.bind("<Button-1>", lambda event, image_path=(folder_path + file): self.on_image_click(event, image_path))

                col += 1
                if col == num_columns:
                    col = 0
                    row += 1

    def add_figure_options(self):

        if hasattr(self, "figure_options_frame"):
            self.figure_options_frame.destroy()

        self.figure_options_frame = ctk.CTkFrame(self.options2,border_width=2)
        self.figure_options_frame.pack(expand=True)

        self.king_var = ctk.StringVar(value="off")
        self.king_switch = ctk.CTkSwitch(self.figure_options_frame, text="King", command=self.king_switches,
                                variable=self.king_var , onvalue="on", offvalue="off")

        self.pawn_var = ctk.StringVar(value="off")
        self.pawn_switch = ctk.CTkSwitch(self.figure_options_frame, text="Pawn", command=self.pawn_switches,
                                variable=self.pawn_var , onvalue="on", offvalue="off")

        self.castling_var = ctk.StringVar(value="off")
        self.castling_switch = ctk.CTkSwitch(self.figure_options_frame, text="Rochade",command=self.castling_switches,
                                variable=self.castling_var , onvalue="on", offvalue="off")
        
        self.boarderx_var = ctk.StringVar(value="off")
        self.boarderx_switch = ctk.CTkSwitch(self.figure_options_frame, text="Walk over x boarder",command=self.boarder_switches,
                                variable=self.boarderx_var , onvalue="on", offvalue="off")

        self.boardery_var = ctk.StringVar(value="off")
        self.boardery_switch = ctk.CTkSwitch(self.figure_options_frame, text="Walk over y boarder",command=self.boarder_switches,
                                variable=self.boardery_var , onvalue="on", offvalue="off")
        
        self.save_figure_button = ctk.CTkButton(self.figure_options_frame, text="SAVE FIGURE", command=self.save_figure, fg_color=RED, hover_color=DARKRED)

        self.king_switch.pack(expand=False, padx=20,pady=10)
        self.pawn_switch.pack(expand=False, padx=20,pady=10)
        self.castling_switch.pack(expand=False, padx=20,pady=10)
        self.boarderx_switch.pack(expand=False, padx=20,pady=10)
        self.boardery_switch.pack(expand=False, padx=20,pady=10)
        self.save_figure_button.pack(expand=True, padx=20, pady=5)
        self.save_figure_button.pack_propagate(False)

    def save_figure(self):
        piece = Piece()
        piece.set_boarder_x(self.boarderx_var.get() == "on")
        piece.set_boarder_y = (self.boardery_var.get() == "on")
        piece.set_king(self.king_var.get() == "on")
        piece.set_pawn(self.pawn_var.get() == "on")
        piece.set_castling(self.castling_switch.get() == "on")
        
        directions = {}
        for x in range(self.board_size):
            for y in (self.board_size):
                y_vec = (y-self.figure_row)
                x_vec = (x-self.figure_col)
                if self.figure_col-x != 0:
                    direction_x = y_vec / abs(y_vec)
                else: 
                    direction_x = 0
                if self.figure_row-y != 0:
                    direction_y = (x_vec) / abs(x_vec) #TODO: Division by zero problem
                else:
                    direction_y = 0

                if self.rectangles[(x,y)].cget("bg") == LIGHTGREEN or self.rectangles[(x,y)].cget("bg") == DARKGREEN:
                    piece.add_jump_move((x_vec,y_vec))
                elif self.rectangles[(x,y)].cget("bg") == DARKRED or self.rectangles[(x,y)].cget("bg") == LIGHTRED:
                    piece.add_direction((direction_x,direction_y,0))
                elif self.rectangles[(x,y)].cget("bg") == DARKBLUE or self.rectangles[(x,y)].cget("bg") == LIGHTBLUE:
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

    def on_image_click(self, event, image_path):

        self.update_board_colors()

        self.image_clicked = True

        row = self.board_size // 2 
        col = self.board_size // 2 

        self.figure_row = row
        self.figure_col = col

        position = self.rectangles[(row, col)]
        label_width = 0.48 * position.winfo_width()

        img = ctk.CTkImage(light_image=Image.open((image_path)).convert("RGBA"),
                            dark_image=Image.open((image_path)).convert("RGBA"),
                            size=(label_width, label_width))

        label = ctk.CTkLabel(position, text="", image=img)
        label.place(relx=0.5, rely=0.5, anchor="center")

        self.add_figure_options()

    def update_board_colors(self):
        value = self.board_value
        for position, canvas_obj in self.rectangles.items():
            i, j = position
            self.change_to_normal_color(i,j)

    def change_to_normal_color(self, x, y):
        value = self.board_value
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

    def field_clicked(self, x, y): 

        if self.figure_col-x != 0:
            direction_x = (x-self.figure_col) / abs(self.figure_col-x)
        else: 
            direction_x = 0
        if self.figure_row-y != 0:
            direction_y = (y-self.figure_row) / abs(self.figure_row-y) #TODO: Division by zero problem
        else:
            direction_y = 0
        
        if self.image_clicked and not (x == self.figure_col and y == self.figure_row):
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

            elif color == LIGHTBLUE and self.is_next_to_figure(x,y):
                self.draw_direction(x,y, True)
            elif color == LIGHTBLUE and not self.is_next_to_figure(x,y):
                self.draw_direction(x,y, False)

            elif color == DARKBLUE and self.is_next_to_figure(x,y):
                self.draw_direction(x,y, True)
            elif color == DARKBLUE and not self.is_next_to_figure(x,y):
                self.draw_direction(x,y, False)

            elif color == DARKRED and self.is_next_to_figure(x,y):
                self.draw_direction(x, y, False)
            elif color == LIGHTRED and self.is_next_to_figure(x,y):
                self.draw_direction(x, y, False)

    def is_next_to_figure(self,x,y):
        return (abs(self.figure_col-x) == 1 and abs(self.figure_row-y)) == 1 or (abs(self.figure_row-y) == 0 and abs(self.figure_col-x)) == 1 or (abs(self.figure_row-y) == 1 and abs(self.figure_col-x) == 0)

    def correct_direction(self,x,y):
        if self.figure_col-x != 0:
            direction_x = (self.figure_col-x) / abs(self.figure_col-x)
        else: 
            direction_x = 0
        if self.figure_row-y != 0:
            direction_y = (self.figure_row-y) / abs(self.figure_row-y) #TODO: Division by zero problem
        else:
            direction_y = 0

        if (abs(self.figure_col-x) == 1 and abs(self.figure_row-y)) == 1 or (abs(self.figure_row-y) == 0 and abs(self.figure_col-x)) == 1 or (abs(self.figure_row-y) == 1 and abs(self.figure_col-x) == 0): #next to the figure
            return True
        elif (abs(self.figure_col-x) == abs(self.figure_row-y) and abs(self.figure_col-x) != 0 ) or  (self.figure_row-y == 0 and self.figure_col-x != 0) or (self.figure_col-x == 0 and self.figure_row-y): # straight or diag move others are no directions
            if self.rectangles[(x+direction_x,y+direction_y)].cget("bg") == LIGHTBLUE or self.rectangles[(x+direction_x,y+direction_y)].cget("bg") == DARKBLUE:  # field in direction of the pice is added as well
                print((x+direction_x,y+direction_y), x,y ,self.figure_row-x, self.figure_col-y)
                return True 
        else:
            return False

    def draw_direction(self,x,y, set):  # figure needs to be updated
        if self.figure_col-x != 0:
            direction_x = (x-self.figure_col) / abs(self.figure_col-x)
        else: 
            direction_x = 0
        if self.figure_row-y != 0:
            direction_y = (y-self.figure_row) / abs(self.figure_row-y) #TODO: Division by zero problem
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

    def draw_board(self, value):
        if int(value) != self.board_size:

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

            self.rectangles = {}

            for i in range(self.board_size):
                for j in range(self.board_size):
                    x1 = i * cell_size
                    y1 = j * cell_size
                    canvas_obj = ctk.CTkCanvas(self.canvas, width=cell_size, height=cell_size)
        
                    canvas_obj.bind("<Button-1>", lambda event, x=i, y=j: self.field_clicked(x, y))
                    canvas_obj.bind("<Button-2>", lambda event, x=i, y=j: self.field_clicked_r(x, y))
                    self.rectangles[(i, j)] = canvas_obj
                    canvas_obj.place(x=x1, y=y1)

                    self.change_to_normal_color(i, j)
                        
                        
                    