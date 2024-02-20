import os
import pickle
import re

DATA_PATH = "src/model/games"

class Model():
    def __init__(self):
        pass

    def save_game(self, instance, file_name):
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
        games_dict = {}
        for file_name in os.listdir(DATA_PATH):
            if file_name.endswith(".pickle"):
                game_name = os.path.splitext(file_name)[0]  # Entferne die Erweiterung
                file_path = os.path.join(DATA_PATH, file_name)
                print(file_path)
                with open(file_path, "rb") as f:
                    game_instance = pickle.load(f)
                games_dict[game_name] = game_instance
        return games_dict

    