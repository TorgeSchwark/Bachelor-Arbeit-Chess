from chess_implementationC.chess_board_wrapper import ChessBoard, chess_lib 
import ctypes
from stockfish import Stockfish
import random
import sqlite3
import json 
import os
import sqlite3

DB_SF = ".\src\supervised_engines\stockfish_DB.db"
DB_AB = ".\src\supervised_engines\lpha_beta_DB.db"
stockfish = Stockfish(path=".\src\chess_implementationC\Stockfish\stockfish-windows-x86-64.exe")
stockfish.set_depth(8)


def fill_dbs(amount):
    #setup the chessBoard
    create_database()

    board = ChessBoard()
    chess_lib.setup_normals(ctypes.byref(board))
    chess_lib.create_chess(ctypes.byref(board)) 
    fen = get_fen_string(board)
    to_str(board, fen)
    matt = ctypes.c_float(0)
    while amount > 0:
        chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt)) 
        
        while matt.value == 0:
            


            moves = (ctypes.c_byte * 2024)()
            move_count = ctypes.c_short(0)
            chess_lib.find_all_moves(ctypes.byref(board), moves, ctypes.byref(move_count))
            fen = get_fen_string(board)
            if True:
                stockfish.set_fen_position(fen)
                sf_val = stockfish.get_evaluation()['value']
                score = ctypes.c_int(0)
                chess_lib.alpha_beta_basic(ctypes.byref(board),ctypes.c_int(3), ctypes.c_int(3), ctypes.c_int(-999999), ctypes.c_int(999999), ctypes.byref(score))
            
            insert_data(board, sf_val, score.value, board.move_count, fen)

            legal_list = (ctypes.c_bool * move_count.value)()
            chess_lib.legal_moves(ctypes.byref(board), move_count.value, moves, legal_list )
            random_move_ind = generate_random_true_index(legal_list)
            chess_lib.make_move(ctypes.byref(board), moves[random_move_ind*5], moves[random_move_ind*5+1], moves[random_move_ind*5+2], moves[random_move_ind*5+3], moves[random_move_ind*5+4])

            chess_lib.is_check_mate(ctypes.byref(board), ctypes.byref(matt)) 
        chess_lib.undo_game(ctypes.byref(board))
        amount -= 1

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
    board_string = ""
    row_strings = []
    for row in range(board.size):
        row_values = []
        for col in range(board.size):
            cell_value = board.board[row][col]
            
            row_values.append(str(cell_value))
        
        row_str = " ".join(row_values)
        row_strings.append(row_str)
    row_strings = " ".join(row_strings)

    board.color_to_move 
    row_strings += " "+ str(board.color_to_move)

    spaces = 0
    castling = {"K":0, "Q":0, "k":0, "q":0}
    chars = "hgfedcba"
    nums = "12345678"
    doublex = -1
    doubley = -1

    moves_count_fifty = 0
    moves_count = 0
    
    for i in fen:
        if i == ' ':
            spaces += 1
        elif spaces == 2:
            castling[i] == 1
        elif spaces == 3:
            if i in chars:
                doublex = chars.index(i)
            if i in nums:
                doubley = int(i)-1
        elif spaces == 4:
            moves_count_fifty = i 
        elif spaces == 5:
            moves_count = i
    
    for key in castling:
        row_strings += " " +str(castling[key])
    
    row_strings += " "+ str(doublex)
    row_strings += " "+ str(doubley)
    row_strings += " "+ moves_count_fifty
    row_strings += " "+ moves_count

    return row_strings
    
def insert_data(board, sf_value, ab_val, depth, fen):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(DB_SF)
    cursor = conn.cursor()

    board_str = to_str(board, fen)

    # Daten in die Datenbank einfügen
    cursor.execute('''
        INSERT INTO ChessData (board, value, depth)
        VALUES (?, ?, ?)
    ''', (board_str, sf_value, depth))

    # Änderungen bestätigen und Verbindung schließen
    conn.commit()
    conn.close()

    conn = sqlite3.connect(DB_AB)
    cursor = conn.cursor()

    board_str = to_str(board, fen)

    # Daten in die Datenbank einfügen
    cursor.execute('''
        INSERT INTO ChessData (board, value, depth)
        VALUES (?, ?, ?)
    ''', (board_str, ab_val, depth))

    # Änderungen bestätigen und Verbindung schließen
    conn.commit()
    conn.close()

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