from model.main_model import Model
from view.starting_page import MainMenu
import customtkinter as ctk

class Controller():
    def __init__(self):
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

        
        
        self.model = Model()
        # Pass to view links on root frame and controller object
        self.view = MainMenu(self.root, self)
        # self.root.deiconify()
        self.root.mainloop()


