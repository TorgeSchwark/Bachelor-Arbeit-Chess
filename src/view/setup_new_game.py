import customtkinter as ctk
import os
from tkinter import *
from PIL import Image, ImageTk



class SetupNewGame():
    def __init__(self, master, controller):
        self.board_size = 0
        self.image_labels = []
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
        self.figure_options_frame.pack(expand=False)

        self.king_var = ctk.StringVar(value="off")
        self.king_switch = ctk.CTkSwitch(self.figure_options_frame, text="King", command=self.king_switches,
                                variable=self.king_var , onvalue="on", offvalue="off")

        self.pawn_var = ctk.StringVar(value="off")
        self.pawn_switch = ctk.CTkSwitch(self.figure_options_frame, text="Pawn", command=self.pawn_switches,
                                variable=self.pawn_var , onvalue="on", offvalue="off")

        self.rochade_var = ctk.StringVar(value="off")
        self.rochade_switch = ctk.CTkSwitch(self.figure_options_frame, text="Rochade",command=self.rochade_switches,
                                variable=self.rochade_var , onvalue="on", offvalue="off")

        self.king_switch.pack(expand=False, padx=20,pady=10)
        self.pawn_switch.pack(expand=False, padx=20,pady=10)
        self.rochade_switch.pack(expand=False, padx=20,pady=10)

    def king_switches(self):
        self.rochade_var.set("on")
        self.pawn_var.set("off")

    def pawn_switches(self):
        self.rochade_var.set("off")
        self.king_var.set("off")
    
    def rochade_switches(self):
        self.pawn_var.set("off")


    def on_image_click(self, event, image_path):
    
        row = self.board_size // 2
        col = self.board_size // 2

        position = self.rectangles[(row, col)]
        label_width = 0.48 * position.winfo_width()

        img = ctk.CTkImage(light_image=Image.open((image_path)).convert("RGBA"),
                            dark_image=Image.open((image_path)).convert("RGBA"),
                            size=(label_width, label_width))
        
        

        label = ctk.CTkLabel(position, text="", image=img)
        label.place(relx=0.5, rely=0.5, anchor="center")

        self.add_figure_options()
    

    def draw_board(self, value):
        if int(value) != self.board_size:

            self.board_size = int(value)

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
                    if (i + j) % 2 == 1:
                        #print("Hea", cell_size)
                        canvas_obj = ctk.CTkCanvas(self.canvas, width=cell_size, height=cell_size, bg="black")
                        canvas_obj.place(x=x1, y=y1)
                    else:
                        canvas_obj = ctk.CTkCanvas(self.canvas, width=cell_size, height=cell_size, bg="white")
                        canvas_obj.place(x=x1, y=y1)
                        
                    self.rectangles[(i, j)] = canvas_obj