import customtkinter as ctk
import os
from tkinter import *
from PIL import Image


class MainMenu():
    def __init__(self, master, controller):
        self.controller = controller
        self.master = master
    
        self.frame = ctk.CTkFrame(master=master, border_width=5)
        self.frame.pack_propagate(False)
        self.frame.pack(expand=True, fill="both")

        self.headline = ctk.CTkLabel(master=self.frame, text="Main Menu", font=("Arial", 25))
        self.headline.pack(pady=15)

        self.button = ctk.CTkButton(master=self.frame, text="Create New Game", command=self.delete_stuff)
        self.button.pack(padx=20, pady=10)

        self.button1 = ctk.CTkButton(master=self.frame, text="Load Game")
        self.button1.pack(padx=20, pady=10)

        self.button2 = ctk.CTkButton(master=self.frame, text="Play Game")
        self.button2.pack(padx=20, pady=10)

    def delete_stuff(self):
        self.frame.destroy()
        SetupNewGame(self.master, self.controller)


        
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
        folder_path = "src/view/images/Chess_pieces/"
        num_columns = 6
        row = 0
        col = 0
        for file in os.listdir(folder_path):
            img = ctk.CTkImage(light_image=Image.open((folder_path + file)).convert("RGBA"),
                            dark_image=Image.open((folder_path + file)).convert("RGBA"),
                            size=(30, 30))
        
            my_label = ctk.CTkLabel(self.options2, text="", image=img)
            my_label.grid(row=row, column=col, padx=5, pady=5)
            
            self.image_labels.append(my_label)
            
            my_label.bind("<Button-1>", lambda event, image_path=(folder_path + file): self.on_image_click(event, image_path))
            
            col += 1
            if col == num_columns:
                col = 0
                row += 1
    
    def on_image_click(self, event, image_path):
    
        row = self.board_size // 2
        col = self.board_size // 2

        position = self.rectangles[(row, col)]
        
        img = ctk.CTkImage(light_image=Image.open((image_path)).convert("RGBA"),
                            dark_image=Image.open((image_path)).convert("RGBA"),
                            size=(30, 30))
        
        label = ctk.CTkLabel(self.canvas, text="", image=img)
        label.place(x=(position[0]+position[2])//4, y=(position[1]+position[2])//4, anchor="center")


    

    def draw_board(self, value):
        if int(value) != self.board_size:
            self.board_size = int(value)
            print("Boardgröße:", self.board_size)

            if hasattr(self, "canvas"):
                self.canvas.destroy()

            canvas_width = self.board.winfo_width() - 50  # Abstand vom Rand
            canvas_height = self.board.winfo_height() - 50  # Abstand vom Rand
            min_canvas_size = min(canvas_width, canvas_height)

            self.canvas = ctk.CTkCanvas(master=self.board, width=min_canvas_size, height=min_canvas_size)
            self.canvas.pack(expand=True)

            cell_size = min_canvas_size / self.board_size
            print("Zellengröße:", cell_size)

            self.rectangles = {}

            for i in range(self.board_size):
                for j in range(self.board_size):
                    x1 = i * cell_size
                    y1 = j * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    if (i + j) % 2 == 1:
                        rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                        self.rectangles[(i, j)] = [x1, y1, x2, y2]
                    else:
                        rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                        self.rectangles[(i, j)] = [x1, y1, x2, y2]