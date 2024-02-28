from core.Controller import Controller
from core.Core import Core
from model.main_model import Model

class LoadGameController(Controller):

    def __init__(self, master):
        self.master = master
        self.model = Model()
        self.load_game_view = self.loadView("LoadGame", master)
    
    
    def select_game(self, game_name):
        print(f"Das ausgewählte Spiel ist: ", game_name)
        return self.model.load_game(game_name)

    def delete_game(self, game_name):
        self.model.delete_file(game_name)
        self.load_game_view.destroy()
        Core.openController("LoadGame", self.master)

    def get_all_games(self):
        return self.model.get_all_games()

    def main_menu(self):
        self.load_game_view.destroy()
        Core.openController("MainMenu", self.master)