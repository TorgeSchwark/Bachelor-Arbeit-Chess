import customtkinter as ctk
from model.main_model import Model
from views.View import View
from views.view_variables import RED, DARKRED

class LoadGameView(View):
    """ this is the view for the load game Menue where you can chose wich of the created games you want to play """
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        self.game_dict =  self.controller.get_all_games()

        self.main_frame = ctk.CTkFrame(self.master, border_width=2)
        self.main_frame.pack(expand=True, fill="both")

        self.game_scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.game_scrollable_frame.pack(expand=True, fill="both")

        self.other_options_frame = ctk.CTkFrame(self.main_frame)
        self.other_options_frame.pack(expand=True, fill="both")

        self.back_to_menu_button = ctk.CTkButton(self.other_options_frame, text="Back to menu", command=self.controller.main_menu)
        self.back_to_menu_button.pack(expand=False, padx=20, pady=5)

        for game_name in self.game_dict:
            button_frame = ctk.CTkFrame(self.game_scrollable_frame)
            button_frame.pack(fill="x", padx=10, pady=5)
            button_game = ctk.CTkButton(button_frame, text=game_name, command=lambda name=game_name: self.controller.select_game(name))
            button_game.pack(expand=True,side="left", fill="x")
            button_delete = ctk.CTkButton(button_frame, text=f"Delete {game_name}", command=lambda name=game_name: self.controller.delete_game(name), fg_color=RED, hover_color=DARKRED)
            button_delete.pack(expand=True,side="right", fill="x")

    def destroy(self):
        return self.main_frame.destroy()
