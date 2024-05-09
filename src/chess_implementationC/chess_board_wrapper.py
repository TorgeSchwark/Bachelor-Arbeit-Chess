import ctypes

# Definition der Konstanten
MAX_MOVES = 10000
MAX_PIECES = 32
MAX_MOVE_DIRECTIONS = 32
MAX_JUMP_MOVES = 32
MAX_FIFTY_MOVE_RULE = 2048
BOARD_SIZE = 20

# Definition der ctypes-Datentypen für den ChessBoard-Wrapper
class ChessBoard(ctypes.Structure):
    """ The warpper class for the c Struct ChessBoard contains the same attributes with equal data types"""
    _fields_ = [
        ("color_to_move", ctypes.c_byte),  # signed char
        ("size", ctypes.c_ubyte),          # unsigned char
        ("has_king", ctypes.c_bool),       # bool
        ("king_pos", ctypes.c_byte),       # signed char
        ("move_count", ctypes.c_short),    # short
        ("fifty_move_rule", ctypes.c_ubyte * MAX_FIFTY_MOVE_RULE),
        ("non_pawn_pieces", ctypes.c_ubyte * MAX_PIECES),
        ("past_moves", ctypes.c_byte * MAX_MOVES),
        ("captured_piece", ctypes.c_byte * MAX_FIFTY_MOVE_RULE),
        ("board", (ctypes.c_byte * BOARD_SIZE) * BOARD_SIZE),
        
        ("white_piece_pos", ctypes.c_ubyte * (2 * MAX_PIECES)),
        ("white_piece_alive", ctypes.c_bool * MAX_PIECES),
        ("white_piece_jump_moves", (ctypes.c_byte * (MAX_JUMP_MOVES * 2)) * MAX_PIECES),
        ("white_piece_move_directions", (ctypes.c_byte * MAX_MOVE_DIRECTIONS) * MAX_PIECES),
        ("white_piece_first_move", ctypes.c_short * MAX_PIECES),
        ("white_piece_img", ctypes.c_ubyte * MAX_PIECES),
        ("white_pawn", ctypes.c_bool * MAX_PIECES),

        ("black_piece_pos", ctypes.c_ubyte * (2 * MAX_PIECES)),
        ("black_piece_alive", ctypes.c_bool * MAX_PIECES),
        ("black_piece_jump_moves", (ctypes.c_byte * (MAX_JUMP_MOVES * 2)) * MAX_PIECES),
        ("black_piece_move_directions", (ctypes.c_byte * MAX_MOVE_DIRECTIONS) * MAX_PIECES),
        ("black_piece_first_move", ctypes.c_short * MAX_PIECES),
        ("black_piece_img", ctypes.c_ubyte * MAX_PIECES),
        ("black_pawn", ctypes.c_bool * MAX_PIECES),

        ("piece_count", ctypes.c_ubyte),
        ("boarder_x", ctypes.c_bool * MAX_PIECES),
        ("boarder_y", ctypes.c_bool * MAX_PIECES),
        ("king", ctypes.c_bool * MAX_PIECES),
        ("castling", ctypes.c_bool * MAX_PIECES)
    ]

chess_lib = ctypes.CDLL("./src/chess_implementationC/chess_library.so")

