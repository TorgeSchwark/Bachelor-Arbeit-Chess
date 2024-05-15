# from chess_implementation.chess_board import ChessBoard
# from chess_implementation.piece_rules import PieceRules
# from chess_implementation.piece import Piece
from chess_implementation.chess_variables import *
# from chess_implementation.find_moves import find_all_moves
# from chess_implementation.make_moves import make_move, undo_last_move
# from chess_implementation.move_stack import MoveStack
from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
import ctypes
from supervised_engines.enige_compare import compare_engines, compare_engines_thread
from supervised_engines.fill_db import to_str
from engines.negmax import alpha_beta_basic, test
from testing.play_game_testing import play_game_test
from engines.mcts import monte_carlo_tree_search
from supervised_engines.fill_db import fill_dbs_by_stock, thread_call
from views.View import View
import customtkinter as ctk
from views.view_variables import *
from PIL import Image
import random
from copy import deepcopy
import time
from multiprocessing import Pool
from copy import deepcopy
from testing.play_setup import play_game
import struct
from stockfish import Stockfish
from engines.get_engine_elo import find_out_elo

stockfish = Stockfish(path=".\src\chess_implementationC\Stockfish\stockfish-windows-x86-64.exe")
stockfish.set_elo_rating(1300)

class PlayGameView(View):
    """ this is the view to play a game currently unsed for debugging """

    
    def __init__(self, master, controller):
        chess_lib.init_tables()
        self.legal_moves_c = (ctypes.c_char * 2048)()
        self.move_count = ctypes.c_short(0)
        self.moves_list = struct.unpack(f'{self.move_count.value}b', self.legal_moves_c.raw[:self.move_count.value])
        
        self.first_click = (-1,-1)
        self.second_click = (-1,-1)
        self.controller = controller
        self.position = (0,0)
        self.master = master
        
        self.chess_board_instance: ChessBoard = controller.board_instance
        test = ctypes.c_int(0)
        chess_lib.eval(ctypes.byref(self.chess_board_instance),ctypes.byref(test))

        print("hier", test.value)

        self.place_main_objects()

    def place_main_objects(self):
        self.main_frame = ctk.CTkFrame(master=self.master, border_width=2)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(expand=True, fill="both")
        self.min_canvas_size = self.master.winfo_height() - 100

        self.settings_frame = ctk.CTkFrame(master=self.main_frame, border_width=2)
        self.settings_frame.pack(side="left", expand=True, fill="both")
        self.settings_frame.pack_propagate(False)

        self.board_frame = ctk.CTkFrame(master=self.main_frame, border_width=2)
        self.board_frame.pack(side="left", expand=True, fill="both")

        self.board_castling_switch_var = ctk.StringVar(value="off")
        self.board_castling_switch = ctk.CTkSwitch(master=self.settings_frame, text="castling", variable=self.board_castling_switch_var, onvalue="on", offvalue="off")
        self.board_castling_switch.pack(expand=False, padx=20,pady=10)

        self.neg_max = ctk.CTkButton(master=self.settings_frame, text="Neg Max Engine", command=self.neg_max_engine)
        self.neg_max.pack(expand=False, padx=20, pady=5)

        self.stockfish_button = ctk.CTkButton(master=self.settings_frame, text="stockfish", command=self.stockfish_go)
        self.stockfish_button.pack(expand=False, padx=20, pady=5)

        self.main_menu_button = ctk.CTkButton(master=self.settings_frame, text="Back to Menu", command=self.controller.main_menu)
        self.main_menu_button.pack(expand=False, padx=20, pady=5)

        self.mcts = ctk.CTkButton(master=self.settings_frame, text="MCTS", command=self.mcts_engine)
        self.mcts.pack(expand=False, padx=20, pady=5)

        self.super_engine = ctk.CTkButton(master=self.settings_frame, text="supervised_engine", command=self.supervised_engine)
        self.super_engine.pack(expand=False, padx=20, pady=5)

        self.compare_engine = ctk.CTkButton(master=self.settings_frame, text="compare_engine", command=self.compare_engines)
        self.compare_engine.pack(expand=False, padx=20, pady=5)

        self.play_game = ctk.CTkButton(master=self.settings_frame, text="play_game", command=self.get_elo)
        self.play_game.pack(expand=False, padx=20, pady=5)

        self.fill_db_button = ctk.CTkButton(master=self.settings_frame, text="fill db", command=self.fill_db_button)
        self.fill_db_button.pack(expand=False, padx=20, pady=5)

        self.initial_setup()

    def initial_setup(self):
        chess_lib.find_all_moves(ctypes.byref(self.chess_board_instance),self.legal_moves_c, ctypes.byref(self.move_count))
        self.moves_list = struct.unpack(f'{self.move_count.value}b', self.legal_moves_c.raw[:self.move_count.value])
        self.draw_board()
        self.draw_moves_on_board()
        self.draw_pieces_on_position()
    
    def fill_db_button(self):
        thread_call()

    def compare_engines(self):
        compare_engines_thread(self.chess_board_instance, self)

    def supervised_engine(self):
        fen = get_fen_string(self.chess_board_instance)
        string = to_str(self.chess_board_instance, fen)
        print(string)
        print(fen)
        score = [0]
        count = [0]
        start = time.time()
        move = test(ctypes.byref(self.chess_board_instance), 3, 3, -99999, 99999, score, count)
        end = time.time()
        
        print("hier", score[0]," ", end-start, " for ", count[0], " moves")
        self.make_move([], score[0])

    def mcts_engine(self):
        move =  monte_carlo_tree_search(self.chess_board_instance)
        self.make_move([], move)

    def get_elo(self):
        find_out_elo(self.chess_board_instance)
        # chess_lib.printChessBoard(ctypes.byref(self.chess_board_instance))
        # for i in range(8):
        #     stockfish.set_elo_rating(2000 +100*i)
        #     won_games = 0
        #     for m in range(50):
        #         value = self.play_game_stock()
        #         print("game ended",value)
        #         chess_lib.undo_game(ctypes.byref(self.chess_board_instance))
        #         won_games += value
        #     print("elo ", 2000+100*i ," won ", won_games, " form " , 10)

    def play_game_stock(self):
        chess_lib.find_all_moves(ctypes.byref(self.chess_board_instance),self.legal_moves_c, ctypes.byref(self.move_count))
        self.moves_list = struct.unpack(f'{self.move_count.value}b', self.legal_moves_c.raw[:self.move_count.value])

        fen = get_fen_string(self.chess_board_instance)
        matt = ctypes.c_float(0)
        while stockfish.is_fen_valid(fen):
            
            self.neg_max_engine()
            self.master.update()

            chess_lib.is_check_mate(ctypes.byref(self.chess_board_instance), ctypes.byref(matt) )
            if(matt.value != 0):
                return matt.value 
           
            self.stockfish_go()
            self.master.update()
            chess_lib.is_check_mate(ctypes.byref(self.chess_board_instance), ctypes.byref(matt) )
            if matt.value != 0:
                return 1-matt.value 
            
            fen = get_fen_string(self.chess_board_instance)

        print("wrong fen", fen)
        self.reset_color()
        #self.draw_moves_on_board()
        self.draw_pieces_on_position()
        return 0.5


    def neg_max_engine(self):
        num = ctypes.c_int(0)
        score2 = ctypes.c_int(0)
        #chess_lib.neg_max(ctypes.byref(self.chess_board_instance),ctypes.c_int(5),ctypes.c_int(5), ctypes.byref(score))
        chess_lib.advanced_apha_beta_engine(ctypes.byref(self.chess_board_instance),ctypes.c_int(6), ctypes.c_int(6), ctypes.c_int(-999999), ctypes.c_int(999999), ctypes.byref(score2))
        self.make_move([],score2.value)

    def stockfish_go(self):
        fen = get_fen_string(self.chess_board_instance)
        if(stockfish.is_fen_valid(fen)):
            
            stockfish.set_fen_position(fen)
            stockfish.get_board_visual(fen)
        else:
            print("wrong")
            print(fen)
        
        move = stockfish.get_best_move()
        ind = self.find_real_move(move)
        self.make_move([],ind)
    
    def find_real_move(self, move):
        piece = ctypes.create_string_buffer(2)
        piece[1] = b'\x00'
        piece[0] = 'x'.encode('utf-8')
        from_x = 7-(ord(move[0])- ord('a'))
        from_y = int(move[1]) -1

        to_x = 7-(ord(move[2])- ord('a'))
        to_y = int(move[3])-1
        if(len(move) > 4):
            piece[0] = move[4].encode('utf-8')
        ind = ctypes.c_int(0)
        
        chess_lib.real_move(ctypes.byref(self.chess_board_instance), ctypes.c_byte(from_x), ctypes.c_byte(from_y), ctypes.c_byte(to_x), ctypes.c_byte(to_y), piece, self.legal_moves_c, self.move_count, ctypes.byref(ind))
        
        return ind.value


    def draw_moves_on_board(self):
        for ind in range(self.move_count.value//5):
            if (self.moves_list[ind*5+2] + self.moves_list[ind*5+3]) % 2 == 1:
                self.rectangles[(self.moves_list[ind*5+2],self.moves_list[ind*5+3])].configure(bg=DARKRED)
            else:
                self.rectangles[(self.moves_list[ind*5+2],self.moves_list[ind*5+3])].configure(bg=LIGHTRED)
            

    def make_move(self, move, ind): 
        if ind < 0:
            chess_lib.make_move(ctypes.byref(self.chess_board_instance), ctypes.c_byte(move[0]),ctypes.c_byte(move[1]), ctypes.c_byte(move[2]),ctypes.c_byte(move[3]), ctypes.c_byte(-1))
        else:
            chess_lib.make_move(ctypes.byref(self.chess_board_instance), ctypes.c_byte(self.moves_list[ind]),ctypes.c_byte(self.moves_list[ind+1]), ctypes.c_byte(self.moves_list[ind+2]),ctypes.c_byte(self.moves_list[ind+3]),ctypes.c_byte(self.moves_list[ind+4]))
        chess_lib.find_all_moves(ctypes.byref(self.chess_board_instance),self.legal_moves_c, ctypes.byref(self.move_count))
        self.moves_list = struct.unpack(f'{self.move_count.value}b', self.legal_moves_c.raw[:self.move_count.value])
        
        self.reset_color()
        #self.draw_moves_on_board()
        self.draw_pieces_on_position()

    def draw_board(self):
        
        cell_size = self.min_canvas_size / self.chess_board_instance.size 

        self.canvas = ctk.CTkCanvas(master=self.board_frame, width=self.min_canvas_size, height=self.min_canvas_size)
        self.canvas.pack(expand=True)
        self.board_cell_size = cell_size
        self.rectangles = {}


        for i in range(self.chess_board_instance.size):
            for j in range(self.chess_board_instance.size):
                x1 = i*cell_size
                y1 = j*cell_size 
                canvas_obj = ctk.CTkCanvas(self.canvas,width=cell_size,height=cell_size)
                self.rectangles[(i, j)] = canvas_obj
                canvas_obj.place(x=x1, y=y1)
                if (j + i) % 2 == 1:
                    self.rectangles[(i,j)].configure(bg=BLACK)
                else:
                    self.rectangles[(i,j)].configure(bg=WHITE)
                self.rectangles[(i,j)].bind("<Button-1>", lambda event, pos=(i,j): self.on_piece_click(pos))
                self.rectangles[(i,j)].bind("<Button-3>", lambda event, pos=(i,j): self.unfocus_piece())

    def draw_pieces_on_position(self):
        if hasattr(self, "piece_images"):
            for key in self.piece_images:
                self.piece_images[key].destroy()

        
        self.piece_images = {}
        self.piece_clicked = False

        for color in range(0,2):
                for ind in range(self.chess_board_instance.piece_count):
                    if (color == 0 and self.chess_board_instance.white_piece_alive[ind]) or (color == 1 and self.chess_board_instance.black_piece_alive[ind]):
                        ind_pos = ind*2
                        if color == 0:
                            path = WHITE_PIECES_PATH + str(self.chess_board_instance.white_piece_img[ind]) +".png"
                            pos = self.chess_board_instance.white_piece_pos[ind_pos] ,self.chess_board_instance.white_piece_pos[ind_pos+1]
                        else: 
                            path = BLACK_PIECES_PATH + str(self.chess_board_instance.black_piece_img[ind]) +".png"
                            pos = self.chess_board_instance.black_piece_pos[ind_pos] ,self.chess_board_instance.black_piece_pos[ind_pos+1]
                        rect_of_position = self.rectangles[pos[0],pos[1]]
                        label_width = 0.48 * self.rectangles[(0,0)].winfo_reqwidth()
                        img = ctk.CTkImage(light_image=Image.open((path)).convert("RGBA"),
                                            dark_image=Image.open((path)).convert("RGBA"),
                                            size=(label_width, label_width))
                        label = ctk.CTkLabel(rect_of_position, text="", image=img)
                        label.bind("<Button-1>", lambda event, pos=pos: self.on_piece_click(pos))
                        label.bind("<Button-3>", lambda event, pos=pos: self.unfocus_piece())
                        label.place(relx=0.5, rely=0.5, anchor="center")
                        self.piece_images[pos] = label

    def on_piece_click(self, pos):
        if self.first_click == (-1,-1):
            self.first_click = pos
        else:
            self.second_click = pos
            print(self.is_move())
            print(self.first_click, self.second_click)
            if self.is_move() == 1:
                self.make_move([self.first_click[0],self.first_click[1],self.second_click[0], self.second_click[1],1], self.find_move_ind(1))
            elif self.is_move() > 1: 
                self.make_move([self.first_click[0],self.first_click[1],self.second_click[0], self.second_click[1],1], self.find_move_ind(1))
                
            self.first_click = (-1,-1)
            self.second_click = (-1,-1)
                
            
    def find_move_ind(self, num): #finds the ith move wich is from x,y to x,y
        move_count = 0
        for ind in range(self.move_count.value//5):
            if self.moves_list[ind*5] == self.first_click[0] and self.moves_list[ind*5+1] == self.first_click[1] and self.moves_list[ind*5+2] == self.second_click[0] and self.moves_list[ind*5+3] == self.second_click[1]:
                move_count += 1
            if move_count == num:
                return ind*5
        

    def is_move(self):
        move_count = 0
        for ind in range(self.move_count.value//5):
            if self.moves_list[ind*5] == self.first_click[0] and self.moves_list[ind*5+1] == self.first_click[1] and self.moves_list[ind*5+2] == self.second_click[0] and self.moves_list[ind*5+3] == self.second_click[1]:
                move_count += 1
        return move_count
        

    def reset_color(self):
        for key in self.rectangles:
            if sum(key) % 2 == 1:
                self.rectangles[key].configure(bg=BLACK)
            else:
                self.rectangles[key].configure(bg=WHITE)

    
    def is_black_field(self,position):
        if (position[0]+ position[1]) % 2 == 1:
            return True
        return False
    
    def destroy(self):
        return self.main_frame.destroy()
    


def thread_testing(args):
    play_game_test(args[0],args[1],args[2])

def get_fen_string(board):
    
    fen_buffer = ctypes.create_string_buffer(556)
    
    chess_lib.board_to_fen(ctypes.byref(board), fen_buffer)
    
    return fen_buffer.value.decode('utf-8')  