from core.Controller import Controller
from core.Core import Core


class MainMenuController(Controller):
    """ The Controller for the main Menue. The implementaion is very view heavy most funkitonality is implemented there"""
    def __init__(self, master):
        self.master = master
        self.main_menu_view = self.loadView("MainMenu", master)

    def create_new_game(self):
        self.main_menu_view.destroy()
        Core.openController("SetupNewGame", self.master)

    def load_game(self):
        self.main_menu_view.destroy()
        Core.openController("LoadGame", self.master)