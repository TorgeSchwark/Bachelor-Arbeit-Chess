#ifndef STANDARD_ENGINES_H
#define STANDARD_ENGINES_H

#include <stdio.h>
#include "chess_board.h"
#include "find_moves.h"
#include "make_moves.h"
#include "evaluation.h"
#include "test_engin.h"

void neg_max(struct ChessBoard *board, int depth, int original_depth, int *score);

void alpha_beta_basic(struct ChessBoard *board, int depth,int original_depth, int alpha, int beta, int *score);

void advanced_apha_beta_engine(struct ChessBoard *board, int depth,int original_depth, int alpha, int beta, int *score);

void sort_moves(struct ChessBoard *board, char *moves, short move_count, int *sorted_ind, bool acurate);

void new_alphaBeta(struct ChessBoard *board, int depth, int original_depth, int alpha, int beta, int *score);

#endif