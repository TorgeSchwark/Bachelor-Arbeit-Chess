from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
# from engines.get_engine_elo import find_real_move
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

num_threads = 20
entries_per_thread = 2

DB_SF = "stockfish_depth9_DB.db"
DB_AB = ".\src\supervised_engines\lpha_beta_DB.db"
DB_SIMPLE = "simple.db"
DB_HALFKP = "half_kp.db"

SIZE_X = 64
SIZE_Y = 6
SIZE_Z = 2

def thread_call():
    """ Calls the funktion to fill the database on multiple threads """
    create_database()
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=thread_task_with_retry)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    print("Alle Threads haben ihre Arbeit abgeschlossen.")

def thread_task_with_retry():
    """ starts to fill the Database on multiple threads if a thread dies starts again"""
    while True:
        try:
            fill_dbs_by_stock(entries_per_thread)
        except Exception as e:
            print("Fehler in Thread:", e)
            print(traceback.format_exc()) 
            time.sleep(1)
            continue

def fill_dbs_by_stock(amount):
    """ Fills the two databases one with positions and evaluations from the AB engine one with the evaluations of SF the positions are created via chosing one of the top SF moves"""
    
    conn_simple = sqlite3.connect(DB_SIMPLE)
    cursor_simple = conn_simple.cursor()

    conn_sf = sqlite3.connect(DB_SF)
    cursor_sf = conn_sf.cursor()

    stockfish = Stockfish(path="./src/chess_implementationC/Stockfish/stockfish/stockfish-ubuntu-x86-64-avx2")
    stockfish.set_depth(9)
    #setup the chessBoard
    create_database()
    board = ChessBoard()
    chess_lib.setup_normals(ctypes.byref(board))
    chess_lib.create_chess(ctypes.byref(board)) 
    chess_lib.init_tables()
    fen = get_fen_string(board)
    matt = ctypes.c_float(0)
    #chess_lib.printChessBoard(ctypes.byref(board))

    # List to store the values to be inserted
    sf_values = []
    simple_input = []
    boards = []
    depths = []
    
    while amount > 0:
        chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt)) 
        count = 0
        randomnes = 5
        
        while matt.value == 0:
            count += 1
            fen = get_fen_string(board)
            
            if True:
                stockfish.set_fen_position(fen)
                sf_val = stockfish.get_evaluation()['value']
                board_simple = (ctypes.c_bool * (SIZE_X*SIZE_Y*SIZE_Z))(*([False] * (SIZE_X*SIZE_Y*SIZE_Z)))
                chess_lib.board_to_simple(ctypes.byref(board), board_simple)

                sf_values.append(sf_val)
                boards.append(to_str(board, fen))
                simple_input.append(bytearray(board_simple))
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
                
            else:
                print(fen)
                break
    
        chess_lib.undo_game(ctypes.byref(board))
        amount -= 1
    
    # Use executemany to insert multiple values at once
    try:
        cursor_sf.executemany('''
            INSERT INTO ChessData (board, value, depth)
            VALUES (?, ?, ?)
        ''', zip(boards, sf_values, depths))

        cursor_simple.executemany('''
             INSERT INTO ChessData (board, value, depth)
             VALUES (?, ?, ?)
         ''', zip(simple_input, sf_values, depths))

        conn_sf.commit()
        conn_simple.commit()

    except Exception as e:
        print("Fehler beim Einfügen in die Datenbank:", e)

def get_fen_string(board):
    
    fen_buffer = ctypes.create_string_buffer(556)
    chess_lib.board_to_fen(ctypes.byref(board), fen_buffer)
    return fen_buffer.value.decode('utf-8') 

def generate_random_true_index(bool_list):
    
    true_indices = [i for i, value in enumerate(bool_list) if value]
    if not true_indices:
        return None  
    random_index = random.choice(true_indices)
    return random_index

def to_str(board, fen):
    row_strings = []
   
    for row in range(board.size):
        row_values = []
        for col in range(board.size):
            cell_value = board.board[row][col]
            if cell_value != 0:
                piece_num = ctypes.c_int(cell_value)
                if cell_value > 0:
                    color = 1
                else:
                    color = -1
                chess_lib.get_piece_type_for_db(ctypes.byref(board), ctypes.byref(piece_num),color)
                row_values.append(str(piece_num.value))
            else: 
                row_values.append(str(0))
            row_str = " ".join(row_values)
        row_strings.append(row_str)
    board_string = " ".join(row_strings)
    row_strings = board_string
    row_strings += " "+ str(board.color_to_move)

    spaces = 0
    castling = {"K":0, "Q":0, "k":0, "q":0}
    chars = "hgfedcba"
    nums = "12345678"
    doublex = -1
    doubley = -1

    moves_count_fifty = ""
    moves_count = ""

    
    for i in fen:
        if i == ' ':
            spaces += 1
        elif spaces == 2:
            if i in castling:
                castling[i] = 1
        elif spaces == 3:
            if i in chars:
                doublex = chars.index(i)
            if i in nums:
                doubley = int(i)-1
        elif spaces == 4:
            moves_count_fifty += i 
        elif spaces == 5:
            moves_count += i
    
    for key in castling:
        row_strings += " " +str(castling[key])

    
    row_strings += " "+ str(doublex)
    row_strings += " "+ str(doubley)
    row_strings += " "+ str(moves_count_fifty)
    row_strings += " "+ str(moves_count)
   
    return row_strings
    
def find_real_move(move, board, move_count, moves):
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
        
    chess_lib.real_move(ctypes.byref(board), ctypes.c_byte(from_x), ctypes.c_byte(from_y), ctypes.c_byte(to_x), ctypes.c_byte(to_y), piece, moves, move_count, ctypes.byref(ind))
        
    return ind.value
    
def create_database():
    db_file = DB_SF
    sb_siple = DB_SIMPLE
 
    # Verbindung zur SQLite-Datenbank herstellen oder eine neue erstellen
    if not os.path.exists(DB_SF):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Tabelle erstellen, falls sie noch nicht existiert
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ChessData (
                board TEXT,
                value REAL,
                depth INTEGER
            )
        ''')

    if not os.path.exists(DB_SIMPLE):
        conn = sqlite3.connect(sb_siple)
        cursor = conn.cursor()

        # Tabelle erstellen, falls sie noch nicht existiert
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ChessData (
                board TEXT,
                value REAL,
                depth INTEGER
            )
        ''')