import os
import importlib
from config import APP_PATH
import abc


"""
    Responsible for the communication between views and models in addiction to
    being responsible for the behavior of the program.
"""
class Controller(metaclass=abc.ABCMeta):
    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    
    """
        Given a view name, return an instance of it
    
        @param viewName:string View to be opened
    """
    def loadView(self, viewName, master):
        response = None
        
        # Set view name
        viewName += "View"
        
        # Check if file exists
        if os.path.exists(APP_PATH+"/views/"+viewName+".py"):
            
            module = importlib.import_module("views."+viewName)
            class_ = getattr(module, viewName)
            response = class_(master, self)
    
        return response
    