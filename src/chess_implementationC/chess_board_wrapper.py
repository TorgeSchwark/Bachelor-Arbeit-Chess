import ctypes

class ChessBoard(ctypes.Structure):
    _fields_ = [("size", ctypes.c_ubyte),
                ("has_king", ctypes.c_bool),
                ("king_pos", ctypes.c_byte),
                ("move_count", ctypes.c_short),
                ("fifty_move_rule", ctypes.c_ubyte * 500),
                ("non_pawn_pieces", ctypes.c_ubyte * 30),
                ("past_moves", ctypes.c_ubyte * 2500),
                ("captured_piece", ctypes.c_ubyte * 500),
                ("board", ctypes.c_byte * 400),
                ("white_piece_pos", ctypes.c_ubyte * 60),
                ("white_piece_alive", ctypes.c_bool * 30),
                ("white_piece_jump_moves", (ctypes.c_byte * 30) * 30),
                ("white_piece_move_directions", (ctypes.c_byte * 28) * 30),
                ("white_piece_fist_move", ctypes.c_int * 30),
                ("white_piece_img", ctypes.c_byte  * 30),
                ("black_piece_pos", ctypes.c_ubyte * 60),
                ("black_piece_alive", ctypes.c_bool * 30),
                ("black_piece_jump_moves", (ctypes.c_byte * 30) * 30),
                ("black_piece_move_directions", (ctypes.c_byte * 28) * 30),
                ("black_piece_fist_move", ctypes.c_int * 30),
                ("black_piece_img", ctypes.c_byte * 30),
                ("piece_count", ctypes.c_ubyte),
                ("boarder_x", ctypes.c_bool * 30),
                ("boarder_y", ctypes.c_bool * 30),
                ("king", ctypes.c_bool * 30),
                ("pawn", ctypes.c_bool * 30),
                ("castling", ctypes.c_bool * 30),]
    images = []  #because of ugly c array of srings

chess_board_lib = ctypes.CDLL("./src/chess_implementationC/chess_board.so")

find_moves_lib = ctypes.CDLL("./src/chess_implementationC/find_moves.so")

make_moves_lib = ctypes.CDLL("./src/chess_implementationC/make_moves.so")