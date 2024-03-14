

cdef struct PieceRules:
    signed char move_direction[27]

    unsigned char jump_move_head
    signed char jump_moves[100]

    bint boarder_x
    bint boarder_y
    bint king
    bint pawn
    bint castling

cdef void set_up_piece_rules(PieceRules piece_rules)
cdef void show_piece_rules(PieceRules piece_rules)
