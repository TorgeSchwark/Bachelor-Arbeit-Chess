cimport numpy as np  # Importieren der C-API von NumPy
import sqlite3
import pickle

cdef struct ChessBoard:

    unsigned char size 
    bint  has_king 

    signed char white_king_pos[3]
    signed char black_king_pos[3]

    signed char color_to_move 
    int move_count 
    signed char fifty_move_rule[3000]

    unsigned char all_non_pawn_pieces[50]
    unsigned char all_non_pawn_pieces_head

    unsigned char white_pawn
    unsigned char black_pawn

    signed char past_moves[3000]
    signed char captured_pieces[3000]
    signed char board[20][20]

    unsigned char piece_count
    signed char white_pieces[50]
    signed char black_pieces[50]


cpdef int set_up_chess_board(ChessBoard chess_board):

    chess_board.size = 0
    chess_board.has_king = False
    chess_board.white_king_pos[2] = -1
    chess_board.black_king_pos[2] = -1
    chess_board.color_to_move = 1
    chess_board.move_count = 0
    chess_board.white_pawn = 0
    chess_board.black_pawn = 0
    chess_board.piece_count = 0
    chess_board.all_non_pawn_pieces_head = 0

    for i in range(len(chess_board.fifty_move_rule)):
        chess_board.fifty_move_rule[i] = 0

    for i in range(len(chess_board.white_king_pos)):
        chess_board.white_king_pos[i] = 0
        chess_board.black_king_pos[i] = 0
    
    for i in range(len(chess_board.all_non_pawn_pieces)):
        chess_board.all_non_pawn_pieces[i] = 0

    for i in range(len(chess_board.past_moves)):
        chess_board.past_moves[i] = 0

    for i in range(len(chess_board.captured_pieces)):
        chess_board.captured_pieces[i] = 0
    
    for i in range(chess_board.size):
        for m in range(chess_board.size):
            chess_board.board[i][m] = 0

    for i in range(len(chess_board.white_pieces)):
        chess_board.white_pieces[i] = 0
        chess_board.black_pieces[i] = 0
    
    return 0



cdef class ChessBoardd:
    cdef ChessBoard chess_board

    def __init__(self):
        set_up_chess_board(self.chess_board)
    
    @property
    def print_board(self):
        print("Size:", self.chess_board.size)
        print("Has king:", self.chess_board.has_king)
        print("White king position:", [self.chess_board.white_king_pos[i] for i in range(3)])
        print("Black king position:", [self.chess_board.black_king_pos[i] for i in range(3)])
        print("Color to move:", self.chess_board.color_to_move)
        print("Move count:", self.chess_board.move_count)
        print("Fifty move rule:", [self.chess_board.fifty_move_rule[i] for i in range(3000)])
        print("All non-pawn pieces:", [self.chess_board.all_non_pawn_pieces[i] for i in range(50)])
        print("All non-pawn pieces head:", self.chess_board.all_non_pawn_pieces_head)
        print("White pawn:", self.chess_board.white_pawn)
        print("Black pawn:", self.chess_board.black_pawn)
        print("Past moves:", [self.chess_board.past_moves[i] for i in range(3000)])
        print("Captured pieces:", [self.chess_board.captured_pieces[i] for i in range(3000)])
        print("Piece count:", self.chess_board.piece_count)
        print("White pieces:", [self.chess_board.white_pieces[i] for i in range(50)])
        print("Black pieces:", [self.chess_board.black_pieces[i] for i in range(50)])
        print("Board:")
        for i in range(len(self.chess_board.board)):
            for j in range(len(self.chess_board.board)):
                print(self.chess_board.board[i][j], end=" ")
            print()

