#ifndef FEATURES_H
#define FEATURES_H

#include "chess_board.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int get_piece_type_KA(int piece, struct ChessBoard *board);
void test_start(float* features_white, float* features_black);


#endif