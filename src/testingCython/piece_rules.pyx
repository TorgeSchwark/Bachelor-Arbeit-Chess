cdef struct PieceRules:
    signed char move_direction[27]

    unsigned char jump_move_head
    signed char jump_moves[100]

    bint boarder_x
    bint boarder_y
    bint king
    bint pawn
    bint castling


cdef void set_up_piece_rules(PieceRules piece_rules):
    for i in range(27):
        piece_rules.move_direction[i] = 0 
    
    piece_rules.jump_move_head = 0

    for i in range(100):
        piece_rules.jump_moves[i] = 0

    piece_rules.boarder_x = False
    piece_rules.boarder_y = False
    piece_rules.king = False
    piece_rules.pawn = False
    piece_rules.castling = False
    


cdef void show_piece_rules(PieceRules piece_rules):
    print("Piece Rules:")
    print("Move direction:", [piece_rules.move_direction[i] for i in range(27)])
    print("Jump move head:", piece_rules.jump_move_head)
    print("Jump moves:", [piece_rules.jump_moves[i] for i in range(100)])
    print("Boarder x:", piece_rules.boarder_x)
    print("Boarder y:", piece_rules.boarder_y)
    print("King:", piece_rules.king)
    print("Pawn:", piece_rules.pawn)
    print("Castling:", piece_rules.castling)