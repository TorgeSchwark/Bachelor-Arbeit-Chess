#ifndef STANDARD_ENGINES_H
#define STANDARD_ENGINES_H

#include <stdio.h>
#include "chess_board.h"
#include "find_moves.h"
#include "make_moves.h"
#include "evaluation.h"
#include "test_engin.h"
#include "../NNUE/nnue_eval.h"

/* this is a standard implementation of the negmax algorithm */
void neg_max(struct ChessBoard *board, int depth, int original_depth, int *score, int *count);

/* basic alpha beta implementation gives back the index of the best move in highest depth otherwise the best score */
void alpha_beta_basic(struct ChessBoard *board, int depth,int original_depth, int alpha, int beta, int *score,  int *count);

/* this is a optimisation of the alpha beta algorithm wich sorts the moves by the evaluation before executing them wich gains speed due to more cutoffs*/
void advanced_apha_beta_engine(struct ChessBoard *board, int depth,int original_depth, int alpha, int beta, int *score,  int *count);

/* puts the index of the moves sorted by the evaluation of the move in the sorted_ind array */
void sort_moves(struct ChessBoard *board, char *moves, short move_count, int *sorted_ind, bool acurate, int *count);

void alpha_beta_basic_other_eval(struct ChessBoard *board, int depth,int original_depth, int alpha, int beta, int *score);

void alpha_beta_basic_NN(struct ChessBoard *board, int depth, int original_depth, int alpha, int beta, int *score,  int *count);

void alpha_beta_basic_best_move_list(struct ChessBoard *board, int depth, int original_depth, int alpha, int beta, int *score, int *count, int *best_moves, int best_move_ind);

#endif