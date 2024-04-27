# -*- encoding:utf-8 -*-
from core.Core import Core
# from chess_implementationC.test import run
from supervised_engines.fill_db import thread_call

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
    #run()
    thread_call()


#error in normal move or double pawn