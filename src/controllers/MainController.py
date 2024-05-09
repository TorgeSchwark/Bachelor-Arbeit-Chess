import customtkinter as ctk
from core.Controller import Controller
from core.Core import Core

class MainController(Controller):
    """ The main controller sets up the main window and starts the MainMenue"""
    def __init__(self, master):

        widget_scale = 2
        ctk.set_widget_scaling(widget_scale)  # widget dimensions and text size
        ctk.set_window_scaling(1)  # window geometry dimensions
        ctk.deactivate_automatic_dpi_awareness()
        ctk.set_appearance_mode("dark")

        self.root = ctk.CTk()

        self.root.title("Game Engine")
        self.root.geometry('1920x1080')

        self.root.size_x = 1920
        self.root.size_y = 1080
        self.root.widget_scale = widget_scale

        
        Core.openController("MainMenu", self.root)
       
        self.root.mainloop()

    

