import customtkinter as ctk
from model.main_model import Model

class LoadGame():

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        self.model = Model()
        self.game_dict =  self.model.get_all_games()

        self.scrollable_frame = ctk.CTkScrollableFrame(self.master)
        self.scrollable_frame.pack(expand=True, fill="both")

        for game_name in self.game_dict:
            button = ctk.CTkButton(self.scrollable_frame, text=game_name, command=self.select_game)
            button.pack(fill="x", padx=10, pady=5)

    def select_game(self):
        #selected_game = self.model.get_selected_game()  # Hier musst du die entsprechende Methode in deinem Controller aufrufen, um das ausgewählte Spiel zu erhalten
        print(f"Das ausgewählte Spiel ist: ")