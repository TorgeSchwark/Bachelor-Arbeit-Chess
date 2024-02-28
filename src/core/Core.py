import os
import importlib
from config import APP_PATH


"""
    Class responsible for opening controllers
"""
class Core:   
    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    """
        Given a controller name, return an instance of it
    
        @param controller:string Controller to be opened
    """
    @staticmethod
    def openController(controller, root, has_game=False,game_name=None):
        response = None

        # Set controller name
        controller_name = controller+  "Controller"
        
        # Check if file exists
        if os.path.exists(APP_PATH+"/controllers/"+controller_name+".py"):
            
            module = importlib.import_module("controllers."+controller_name)
            if not has_game:
                class_ = getattr(module, controller_name)
                response = class_(root)
            else:
                class_ = getattr(module, controller_name, game_name)
                response = class_(root, game_name)
        
        return response