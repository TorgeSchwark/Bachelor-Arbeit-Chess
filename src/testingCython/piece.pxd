# piece.pxd

cimport piece_rules

cdef struct Piece:
    piece_rules.PieceRules piece_rule
    bint is_alive
    unsigned char position[2]
    int first_move 

cdef void set_up_piece(Piece piece)

cdef void show_piece(Piece piece)
