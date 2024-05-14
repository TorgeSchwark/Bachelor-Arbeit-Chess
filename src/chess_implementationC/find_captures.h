#ifndef FIND_CAPTURES_H
#define FIND_CAPTURES_H

#include "chess_board.h"
#include "find_moves.h"


void find_all_captures(struct ChessBoard *board, signed char *moves, short *moves_count);

void find_jump_captures(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_jump_moves, signed char *moves, short *moves_count, unsigned char piece_ind);

void find_pawn_captures(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions,short *color_first_moves, signed char *moves, short *moves_count, unsigned char piece_ind);

void find_captures_directions(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions, signed char *moves, short *move_counts, unsigned char piece_ind);

#endif