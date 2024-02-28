import abc


"""
    Responsible for the program interface.
"""
class View(metaclass=abc.ABCMeta):
  
    """
        Closes the interface. It is called when the window is closed.
    """
    @abc.abstractmethod
    def destroy(self):
        return