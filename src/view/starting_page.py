import customtkinter as ctk
import os
from tkinter import *
from PIL import Image, ImageTk
from view.setup_new_game import SetupNewGame
from view.load_game import LoadGame 

class MainMenu():
    def __init__(self, master, controller):
        self.controller = controller
        self.master = master
    
        self.frame = ctk.CTkFrame(master=master, border_width=5)
        self.frame.pack_propagate(False)
        self.frame.pack(expand=True, fill="both")

        self.headline = ctk.CTkLabel(master=self.frame, text="Main Menu", font=("Arial", 25))
        self.headline.pack(pady=15)

        self.button = ctk.CTkButton(master=self.frame, text="Create New Game", command=self.create_new_game)
        self.button.pack(padx=20, pady=10)

        self.button1 = ctk.CTkButton(master=self.frame, text="Load Game",command=self.load_game)
        self.button1.pack(padx=20, pady=10)

        self.button2 = ctk.CTkButton(master=self.frame, text="Play Game")
        self.button2.pack(padx=20, pady=10)

    def create_new_game(self):
        self.frame.destroy()
        SetupNewGame(self.master, self.controller)

    def load_game(self):
        self.frame.destroy()
        LoadGame(self.master, self.controller)

