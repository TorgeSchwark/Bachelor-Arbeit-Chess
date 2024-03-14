cimport numpy as np  # Importieren der C-API von NumPy


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


cdef int set_up_chess_board(ChessBoard chess_board):
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

    for i n range(len(chess_board.captured_pieces)):
        chess_board.captured_pieces[i] = 0
    
    for i in range(chess_board.size):
        for m in range(chess_board.size):
            chess_board[i][m] = 0

    for i in range(len(chess_board.white_pieces)):
        chess_board.white_pieces[i] = 0
        chess_board.black_pieces[i] = 0

    
    
    return 0





