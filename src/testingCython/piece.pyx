cimport piece_rules

cdef struct Piece:
    piece_rules.PieceRules piece_rule
    bint is_alive
    unsigned char position[2]
    int first_move 

cdef void set_up_piece(Piece piece):
    piece.is_alive = True
    piece.position[0] = 0
    piece.position[1] = 0
    piece.first_move = -1
    piece_rules.show_piece_rules(piece.piece_rule)
    #piece_rules.set_up_piece_rules(piece.piece_rule)

cdef void show_piece(Piece piece):
    print("Piece:")
   # piece_rules.show_piece_rules(piece.piece_rules)  # Korrekte Verwendung von piece_rule statt piece_rules
    print("Is alive:", piece.is_alive)
    print("Position: ({}, {})".format(piece.position[0], piece.position[1]))
    print("First move:", piece.first_move)



