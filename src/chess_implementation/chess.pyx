# piece_rules.pyx
cdef struct PieceRules:
    int[27] move_directions
    int[50] jump_moves
    bint boarder_x
    bint boarder_y
    bint king
    bint pawn
    bint castling
    char string[20]

# piece.pyx
cdef struct Piece:
    PieceRules rules
    bint is_alive
    int[2] position
    int first_move

# chess_board.pyx
cdef struct ChessBoard:
    unsigned char size 
    bint has_king 
    signed char white_king_pos[3]
    signed char black_king_pos[3]
    signed char color_to_move 
    int move_count 
    signed char fifty_move_rule[1000]
    unsigned char all_non_pawn_pieces[50]
    unsigned char all_non_pawn_pieces_head
    unsigned char white_pawn
    unsigned char black_pawn
    signed char past_moves[1000]
    signed char captured_pieces[1000]
    signed char board[20][20]
    unsigned char piece_count
    Piece white_pieces[50]
    Piece black_pieces[50]

cdef show_chess_board(ChessBoard chess_board):
    print("size: ",chess_board.size)
    print("has_king: ", chess_board.has_king)
    for i in range(3):
        print(chess_board.white_king_pos[i])
    


cpdef convert(chess_board_py):
    cdef ChessBoard board_c = ChessBoard()
    board_c.size = chess_board_py.size
    board_c.has_king = chess_board_py.has_king
    for i in range(len(chess_board_py.white_king_pos)):
        board_c.white_king_pos[i] = chess_board_py.white_king_pos[i]

    show_chess_board(board_c)

    return board_c

