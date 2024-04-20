#ifndef EVALUATION_H
#define EVALUATION_H

#include <stdio.h>
#include "chess_board.h"
#include "find_moves.h"
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

void eval(struct ChessBoard *pos_board, int *score);

bool direct_repetition(struct ChessBoard *board);

int piece_black(signed char ind, struct ChessBoard *pos_board);

int piece_white(signed char ind, struct ChessBoard *pos_board);

#endif