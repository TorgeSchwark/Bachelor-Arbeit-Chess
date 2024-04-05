#ifndef TEST_ENGIN_H
#define TEST_ENGIN_H


#include <stdio.h>
#include <windows.h>
#include "chess_board.h"
#include "find_moves.h"
#include "make_moves.h"
#define NUM_THREADS 1



void test_engine(struct ChessBoard *board, int depth); // Kein Semikolon hier

void test_engine_all_moves(struct ChessBoard *board, int depth, int *count);

#endif
