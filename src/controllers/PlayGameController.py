from core.Controller import Controller
from core.Core import Core
from model.main_model import Model



class PlayGameController(Controller):
    """ The Play Game controller """
    def __init__(self, master, game_name):
        self.master = master
        self.game_name = game_name
        self.model = Model()
        self.board_instance = self.load_game(game_name)

        self.play_game_view = self.loadView("PlayGame", master)

    def load_game(self, game_name):
        return self.model.load_game(game_name)
    
    def main_menu(self):
        self.play_game_view.destroy()
        Core.openController("MainMenu", self.master)