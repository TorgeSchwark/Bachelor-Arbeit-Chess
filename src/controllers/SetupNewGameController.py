from core.Controller import Controller
from core.Core import Core
from chess_implementation.chess_board import ChessBoard
from views.view_variables import *
from model.main_model import Model

class SetupNewGameController(Controller):

    def __init__(self, master):
        self.master = master
        self.setup_new_game_view = self.loadView("SetupNewGame", master)
        self.model = Model()
    
    def main_menu(self):
        self.setup_new_game_view.destroy()
        Core.openController("MainMenu", self.master)

    #call the DB to save the Game
    def save_game(self):
        if (self.model.save_game(self.setup_new_game_view.chess_board_instance, self.setup_new_game_view.game_name_var.get())):
            print("Saved Game successful")
            self.main_menu()
        else:
            self.game_name = "Save wasnt successful"

    def king_switches(self):
        self.setup_new_game_view.castling_var.set("on")
        self.setup_new_game_view.pawn_var.set("off")
        self.setup_new_game_view.boarderx_var.set("off")
        self.setup_new_game_view.boardery_var.set("off")

    def pawn_switches(self):
        self.setup_new_game_view.castling_var.set("off")
        self.setup_new_game_view.king_var.set("off")
        self.setup_new_game_view.boarderx_var.set("off")
        self.setup_new_game_view.boardery_var.set("off")

    def castling_switches(self):
        self.setup_new_game_view.pawn_var.set("off")
        self.setup_new_game_view.boarderx_var.set("off")
        self.setup_new_game_view.boardery_var.set("off")

    def boarder_switches(self):
        self.setup_new_game_view.pawn_var.set("off")
        self.setup_new_game_view.king_var.set("off")
        self.setup_new_game_view.castling_var.set("off")


