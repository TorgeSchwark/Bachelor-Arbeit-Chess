#ifndef EVALUATION_H
#define EVALUATION_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "chess_board.h"
#include "find_moves.h"
#include "find_captures.h"
#include "make_moves.h"
#include "test_engin.h"

#define PAWN   0
#define KNIGHT 1
#define BISHOP 2
#define ROOK   3
#define QUEEN  4
#define KING   5

#define WHITE  0
#define BLACK  1

#define RANDOMNESS 20
#define WHITE_PAWN      (2 * PAWN + WHITE)
#define BLACK_PAWN      (2 * PAWN + BLACK)
#define WHITE_KNIGHT    (2 * KNIGHT + WHITE)
#define BLACK_KNIGHT    (2 * KNIGHT + BLACK)
#define WHITE_BISHOP    (2 * BISHOP + WHITE)
#define BLACK_BISHOP    (2 * BISHOP + BLACK)
#define WHITE_ROOK      (2 * ROOK + WHITE)
#define BLACK_ROOK      (2 * ROOK + BLACK)
#define WHITE_QUEEN     (2 * QUEEN + WHITE)
#define BLACK_QUEEN     (2 * QUEEN + BLACK)
#define WHITE_KING      (2 * KING + WHITE)
#define BLACK_KING      (2 * KING + BLACK)
#define EMPTY           (BLACK_KING + 1)

/* A PeSTO like evaluation funktion that only uses pieces tables with aditional information about pawn structure and double bishop/knight */
void eval(struct ChessBoard *pos_board, int *score);

/* checking for any repititions is coputationaly expensive therefor this function checks if the last 3 moves where a direct repetition wich is mutch faster */
bool direct_repetition(struct ChessBoard *board);

/* returns the piece type (number) in the pesto tables since they can be in a abitrary order in the ChessBoard struct */
int piece_black(signed char ind, struct ChessBoard *pos_board);

/* returns the piece type (number) in the pesto tables since they can be in a abitrary order in the ChessBoard struct */
int piece_white(signed char ind, struct ChessBoard *pos_board);

void eval_without_extra(struct ChessBoard *pos_board, int *score);

void quiesce(struct ChessBoard *pos_board, int alpha, int beta, int *score, int *count);

void quiesce_best_move_list(struct ChessBoard *pos_board, int alpha, int beta, int *score, int *count, int* best_moves, int best_moves_ind);

#endif