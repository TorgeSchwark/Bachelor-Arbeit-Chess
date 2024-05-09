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

num_threads = 12
entries_per_thread = 1

DB_SF = ".\src\supervised_engines\stockfish_depth16_DB.db"
DB_AB = ".\src\supervised_engines\lpha_beta_DB.db"

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
    
    # conn_ab = sqlite3.connect(DB_AB)
    # cursor_ab = conn_ab.cursor()
    conn_sf = sqlite3.connect(DB_SF)
    cursor_sf = conn_sf.cursor()

    stockfish = Stockfish(path=".\src\chess_implementationC\Stockfish\stockfish-windows-x86-64.exe")
    stockfish.set_depth(16)
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
    ab_values = []
    boards = []
    depths = []
    
    while amount > 0:
        #print("amount", amount)
        chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt)) 
        count = 0
        randomnes = 5
        
        while matt.value == 0:
            count += 1
            fen = get_fen_string(board)
           
            if True:
                
                stockfish.set_fen_position(fen)
                
                sf_val = stockfish.get_evaluation()['value']
                
                #score = ctypes.c_int(0)
                #chess_lib.alpha_beta_basic(ctypes.byref(board),ctypes.c_int(3), ctypes.c_int(3), ctypes.c_int(-999999), ctypes.c_int(999999), ctypes.byref(score))
                    
                sf_values.append(sf_val)
                #ab_values.append(score.value)
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

        # cursor_ab.executemany('''
        #     INSERT INTO ChessData (board, value, depth)
        #     VALUES (?, ?, ?)
        # ''', zip(boards, ab_values, depths))

        conn_sf.commit()
        # conn_ab.commit()

    except Exception as e:
        print("Fehler beim Einfügen in die Datenbank:", e)


def fill_dbs_random(amount):
    """ Fills the two databases one with positions and evaluations from the AB engine one with the evaluations of SF the positions are created via random play"""
    
    conn_ab = sqlite3.connect(DB_AB)
    cursor_ab = conn_ab.cursor()

    conn_sf = sqlite3.connect(DB_SF)
    cursor_sf = conn_sf.cursor()
    
    stockfish = Stockfish(path=".\src\chess_implementationC\Stockfish\stockfish-windows-x86-64.exe")
    stockfish.set_depth(8)
    create_database()
    #setup the chessBoard
    board = ChessBoard()
    chess_lib.setup_normals(ctypes.byref(board))
    chess_lib.create_chess(ctypes.byref(board)) 
    chess_lib.init_tables()
    fen = get_fen_string(board)
    to_str(board, fen)
    
    chess_lib.printChessBoard(ctypes.byref(board))
    
    matt = ctypes.c_float(0)
    count = 0

    # List to store the values to be inserted
    ab_values = []
    sf_values = []
    boards = []
    depths = []
    fens = []
    
    while amount > 0:
        
        chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt)) 
        count = 0
        while matt.value == 0:
            count += 1
            fen = get_fen_string(board)
                
            stockfish.set_fen_position(fen)
            sf_val = stockfish.get_evaluation()['value']
            score = ctypes.c_int(0)
            chess_lib.alpha_beta_basic(ctypes.byref(board),ctypes.c_int(3), ctypes.c_int(3), ctypes.c_int(-999999), ctypes.c_int(999999), ctypes.byref(score))
                
            sf_values.append(sf_val)
            ab_values.append(score.value)
            boards.append(to_str(board, fen))
            depths.append(board.move_count)
            fens.append(fen)

            moves = (ctypes.c_byte * 2024)()
            move_count = ctypes.c_short(0)
            chess_lib.find_all_moves(ctypes.byref(board), moves, ctypes.byref(move_count))

            legal_list = (ctypes.c_bool * move_count.value)()
            chess_lib.legal_moves(ctypes.byref(board), move_count.value, moves, legal_list )
            random_move_ind = generate_random_true_index(legal_list)
            
            chess_lib.make_move(ctypes.byref(board), moves[random_move_ind*5], moves[random_move_ind*5+1], moves[random_move_ind*5+2], moves[random_move_ind*5+3], moves[random_move_ind*5+4])
            chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt)) 

        chess_lib.undo_game(ctypes.byref(board))
        
        # Decrement amount
        amount -= 1
    
    # Use executemany to insert multiple values at once
    try:
        cursor_sf.executemany('''
            INSERT INTO ChessData (board, value, depth)
            VALUES (?, ?, ?)
        ''', zip(boards, sf_values, depths))

        cursor_ab.executemany('''
            INSERT INTO ChessData (board, value, depth)
            VALUES (?, ?, ?)
        ''', zip(boards, ab_values, depths))

        conn_sf.commit()
        conn_ab.commit()

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
                castling[i] == 1
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
    db_file2 = DB_AB
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
    if not os.path.exists(DB_AB):
        conn = sqlite3.connect(db_file2)
        cursor = conn.cursor()

        # Tabelle erstellen, falls sie noch nicht existiert
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ChessData (
                board TEXT,
                value REAL,
                depth INTEGER
            )
        ''')