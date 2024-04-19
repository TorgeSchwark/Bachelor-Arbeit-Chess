#ifndef TEST_ENGIN_H
#define TEST_ENGIN_H


#include <stdio.h>
#include "chess_board.h"
#include "find_moves.h"
#include "make_moves.h"

void undo_game(struct ChessBoard *board);

void is_check_mate(struct ChessBoard *board, float *matt);

bool three_fold_repetition(struct ChessBoard *board);

void copy_moves_and_board(struct ChessBoard *board, signed char current_board[20][20], signed char *all_moves);

bool same_move(struct ChessBoard *board, int ind, int ind_past);

void count_for_each_move(struct ChessBoard *board, int depth, long long *counts);

bool all_legal(struct ChessBoard *board, signed char *moves, short *move_count);

bool is_legal(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void test_engine(struct ChessBoard *board, int depth); 

void test_engine_all_moves(struct ChessBoard *board, int depth, long long *count);

void legal_moves(struct ChessBoard *board, short move_count, char *moves, bool *legal);

#endif
