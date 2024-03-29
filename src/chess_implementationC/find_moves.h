#ifndef FIND_MOVES_H
#define FIND_MOVES_H

#include "chess_board.h"


void find_all_moves(struct ChessBoard *board, signed char *moves, short *moves_count);

void find_jump_moves(struct ChessBoard *board,unsigned char* color_pos, signed char* piece_jump_moves, signed char *moves, short *moves_count, unsigned char piece_ind);

void find_move_directions(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions, signed char *moves, short *move_counts, unsigned char piece_ind);

void add_move(signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type, signed char* moves, short *moves_count);

bool on_board(signed char x, unsigned char size);

void test_find_all_moves();



#endif /* FIND_MOVES_H */
