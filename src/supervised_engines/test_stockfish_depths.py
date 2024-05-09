from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
import ctypes
from stockfish import Stockfish
import random
import sqlite3
import json 
import os
import sqlite3
import threading
import time
import traceback
from fill_db import *

num_threads = 5
entries_per_thread = 2

DB_SF = ".\src\supervised_engines\stockfish_depth16_DB.db"
DB_AB = ".\src\supervised_engines\lpha_beta_DB.db"

def test_stock_difference():
    """" This function testst the avg difference in centipawns between sf elo 5-15 against the evaluation of elo 16"""
    for i in range(4,16):
        val = thread_call(i)
        print("difference between depth", i, " and " , 16 , " is ", val)
        

def thread_call(depth):
    create_database()
    threads = []
    results = []  

    for _ in range(num_threads):
        thread = threading.Thread(target=thread_task_with_retry, args=(depth, results,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    average_result = sum(results) / len(results)
    return average_result
    
def thread_task_with_retry(depth, results_list):
    while True:
        try:
            result = fill_dbs_by_stock(entries_per_thread, depth)
            results_list.append(result)  
            return  
        except Exception as e:
            time.sleep(1)
            continue

def fill_dbs_by_stock(amount, sf_depth):
    """ Plays games doing one of the top three moves of stockfish Every position+ evaluation isinserted into the DB. Also compares SF in two different elos"""
    conn_sf = sqlite3.connect(DB_SF)
    cursor_sf = conn_sf.cursor()

    stockfish = Stockfish(path=".\src\chess_implementationC\Stockfish\stockfish-windows-x86-64.exe")
    stockfish.set_depth(16)
    create_database()
    board = ChessBoard()
    chess_lib.setup_normals(ctypes.byref(board))
    chess_lib.create_chess(ctypes.byref(board)) 
    chess_lib.init_tables()
    fen = get_fen_string(board)
    matt = ctypes.c_float(0)
   

   
    sf_values = []
    boards = []
    depths = []
    eval_test = 0
    eval_count = 0
    
    while amount > 0:
        
        chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt)) 
        count = 0
        randomnes = 5
        
        while matt.value == 0:
            count += 1
            eval_count += 1
            fen = get_fen_string(board)
           
            if True:
            
                stockfish.set_fen_position(fen)
                stockfish.set_depth(sf_depth)
                sf_val_short = stockfish.get_evaluation()['value']
                stockfish.set_depth(16)
                sf_val = stockfish.get_evaluation()['value']
                eval_test += abs(sf_val_short-sf_val)
        
                sf_values.append(sf_val)
                
                boards.append(to_str(board, fen))
                depths.append(board.move_count)

                moves = (ctypes.c_byte * 2024)()
                move_count = ctypes.c_short(0)
                chess_lib.find_all_moves(ctypes.byref(board), moves, ctypes.byref(move_count))

                moves_dict = stockfish.get_top_moves(randomnes)
                
                move_ind = random.randint(0,len(moves_dict)-1)

                move = moves_dict[move_ind]['Move']
                ind = find_real_move(move, board, move_count, moves)
                chess_lib.make_move(ctypes.byref(board), moves[ind],  moves[ind+1],  moves[ind+2],  moves[ind+3],  moves[ind+4])
               
                chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt))
                
        chess_lib.undo_game(ctypes.byref(board))
        amount -= 1
    
    
    try:
        cursor_sf.executemany('''
            INSERT INTO ChessData (board, value, depth)
            VALUES (?, ?, ?)
        ''', zip(boards, sf_values, depths))

        conn_sf.commit()


    except Exception as e:
        print("Fehler beim Einfügen in die Datenbank:", e)

    return eval_test/eval_count


