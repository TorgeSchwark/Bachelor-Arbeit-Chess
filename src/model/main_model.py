import os
import pickle
import re

DATA_PATH = "./src/model/games"

class Model():
    """ the model to manage the pickle "database" """
    def __init__(self):
        pass
    
    
    def save_game(self, instance, file_name):
        """ saves the game in database under a given file name wich needs to be valid """
        if not instance.has_king:
            print("game need king")
            return False
        file_name += ".pickle"
        if not self.is_valid_filename(file_name):
            print("wrong name")
            return False

        file_path = os.path.join(DATA_PATH, file_name)
        if os.path.exists(file_path):
            print("name is not available")
            return False

        with open(file_path, "wb") as f:
            pickle.dump(instance, f)
            return True

    def is_valid_filename(self, filename):
        """ Checks if a filename is valid """
        if not filename:
            return False
        if len(filename) > 260:
            return False
        if re.search(r"[\\/:*?\"<>|]", filename):
            return False
        if filename.startswith(".") or filename.endswith(".") or filename.startswith(" ") or filename.endswith(" "):
            return False
        if re.match(r"(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$", filename.upper()):
            return False
        return True
    
    def get_all_games(self):
        """ queries and all games in the Database and returns them in a dict with the name and the class object"""
        games_dict = {}
        for file_name in os.listdir(DATA_PATH):
            if file_name.endswith(".pickle"):
                game_name = os.path.splitext(file_name)[0]  
                file_path = os.path.join(DATA_PATH, file_name)
                with open(file_path, "rb") as f:
                    game_instance = pickle.load(f)
                games_dict[game_name] = game_instance
        return games_dict

    #gets Game name and loads it
    def load_game(self, game_name):
        """ only loads one game returns the game instance """
        game_name += ".pickle"
        file_path = os.path.join(DATA_PATH, game_name)
        if self.is_valid_filename(game_name) and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                print(file_path)
                game_instance = pickle.load(f)
            return game_instance
        else:
            print(f"Error: File '{file_path}' does not exist.")
            return None

    #deletes file with certain file_name
    def delete_file(self, game_name):
        """ delets a game from the Database"""
        game_name += ".pickle"
        file_path = os.path.join(DATA_PATH, game_name)
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{game_name}' has been deleted.")
        else:
            print(f"Error: File '{game_name}' does not exist.")

    