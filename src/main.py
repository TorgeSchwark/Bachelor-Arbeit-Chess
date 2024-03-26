# -*- encoding:utf-8 -*-
from core.Core import Core

"""
    Main class. Responsible for running the application.
"""
class Main:

    @staticmethod
    def run():
        try:
            app = Core.openController("Main", None)
        except Exception as e:
            print(str(e))

if __name__ == '__main__':

    Main.run()


#error in normal move or double pawn