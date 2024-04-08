#ifndef TEST_ENGIN_H
#define TEST_ENGIN_H


#include <stdio.h>
#include "chess_board.h"
#include "find_moves.h"
#include "make_moves.h"

bool all_legal(struct ChessBoard *board, signed char *moves, short *move_count);

bool is_legal(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void test_engine(struct ChessBoard *board, int depth); // Kein Semikolon hier

void test_engine_all_moves(struct ChessBoard *board, int depth, int *count);

#endif
